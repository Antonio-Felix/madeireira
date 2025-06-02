from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Cliente, Funcionario, Compra, Produto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import FuncionarioRegisterForm, CompraForm, ItemCompraFormSet
from .models import Funcionario

def sua_view(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    compras = Compra.objects.all()

    if data_inicio and data_fim:
        compras = compras.filter(data__range=[data_inicio, data_fim])

    context = {
        'compras': compras,
    }
    return render(request, 'home.html', context)

def registro_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = FuncionarioRegisterForm()
    return render(request, 'registros/registro.html', {'form': form})

def login_funcionario(request):
    erro = ''
    if request.method == 'POST':
        cpf = request.POST['cpf']
        senha = request.POST['senha']
        user = authenticate(username=cpf, password=senha)
        if user:
            login(request, user)
            return redirect('cliente')
        else:
            erro = 'CPF ou senha inválidos.'
    return render(request, 'registros/login.html', {'erro': erro})
# Funcionalidades da tabela Cliente

from django.core.paginator import Paginator

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'home.html'
    context_object_name = 'clientes'
    paginate_by = 4
    
    def get_queryset(self):
        queryset = super().get_queryset()
        termo_busca = self.request.GET.get('buscar_cliente', '')
        if termo_busca:
            queryset = queryset.filter(nome__icontains=termo_busca)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario_logado = self.request.user.funcionario
        context['funcionario_logado'] = funcionario_logado

        compras = Compra.objects.filter(funcionario=funcionario_logado)
        termo_produto = self.request.GET.get('buscar_produto', '')

        produtos = Produto.objects.all()
        if termo_produto:
            produtos = produtos.filter(nome_produto__icontains=termo_produto)

        compras_paginator = Paginator(compras, 2)
        produtos_paginator = Paginator(produtos, 4)

        compra_page_number = self.request.GET.get('compras_page')
        produto_page_number = self.request.GET.get('produtos_page')

        context['compras'] = compras_paginator.get_page(compra_page_number)
        context['produtos'] = produtos_paginator.get_page(produto_page_number)

        # Para manter o valor no campo busca do template
        context['buscar_produto'] = termo_produto

        return context


class ClienteDetailView(LoginRequiredMixin,DetailView):
    model = Cliente
    template_name = "cliente/detalhes_cliente.html"

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ['cpf', 'nome', 'numero']
    template_name = "cliente/cliente.html"
    success_url = reverse_lazy('cliente')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['cpf', 'nome', 'numero']
    template_name = "cliente/atualiza_cliente.html"
    success_url = reverse_lazy('cliente')
    
class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = "cliente/apagar.html"
    success_url = reverse_lazy('cliente')

# Funcionalidades da tabela Funcionario

class FunciUpdateView(LoginRequiredMixin, UpdateView):
    model = Funcionario
    fields = ['cpf', 'nome','idade', 'numero','email']
    template_name = "funcionario/atualiza_funci.html"
    success_url = reverse_lazy('cliente')

# Funcionalidades da tabela Produto

class ProdutoCreateView(LoginRequiredMixin, CreateView):
    model = Produto
    fields = ['nome_produto', 'valor']
    template_name = "produto/produto_novo.html"
    success_url = reverse_lazy('cliente')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    model = Produto
    fields = ['nome_produto','valor']
    template_name = "produto/atualiza_produto.html"
    success_url = reverse_lazy('cliente')

class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    model = Produto
    template_name = "produto/apagar_produto.html"
    success_url = reverse_lazy('cliente')

class CompraCreateView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/compra_form.html'
    success_url = reverse_lazy('cliente')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ItemCompraFormSet(self.request.POST)
        else:
            data['formset'] = ItemCompraFormSet()
        return data
    
    def form_valid(self, form):
        form.instance.funcionario = self.request.user.funcionario
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            self.object.calcular_valor_total()

            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CompraDetailView(DetailView):
    model = Compra
    template_name = 'compras/compra_detalhes.html'
    context_object_name = 'compra'

class CompraDeleteView(LoginRequiredMixin, DeleteView):
    model = Compra
    template_name = "compras/apagar_compra.html"
    success_url = reverse_lazy('cliente')