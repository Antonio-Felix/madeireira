from django.urls import path
from .views import ClienteListView, ClienteDetailView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView
from .views import FunciUpdateView, CompraCreateView, CompraDetailView, CompraDeleteView
from .views import ProdutoCreateView, ProdutoDeleteView, ProdutoUpdateView
from .views import registro_funcionario, login_funcionario

urlpatterns = [
    #login e cadastro para logar, é para o funcionario.
    path('login/', login_funcionario, name='login'),
    path('registro/', registro_funcionario, name='registro'),
    
    #Página home
    path('', ClienteListView.as_view(), name='cliente'),

    #Editaveis do funcionario sobre a tabela Cliente
    path('clientes/<str:pk>', ClienteDetailView.as_view(), name="cliente-detalhe"),
    path('clientes/novo/', ClienteCreateView.as_view(), name="cliente-criar"),
    path('clientes/<str:pk>/atualiza/', ClienteUpdateView.as_view(), name="cliente-atualiza"),
    path('clientes/<str:pk>/apaga', ClienteDeleteView.as_view(), name= "cliente-apaga"),
    
    #Editar dados funcionario
    path('funcionarios/<str:pk>/atualiza/', FunciUpdateView.as_view(), name= "funcionario-atualiza"),

    #Editaveis do funcionario sobre a tabela Compra
    path('compra/nova/', CompraCreateView.as_view(), name='compra-nova'),
    path('compra/<int:pk>/', CompraDetailView.as_view(), name='compra-detalhe'),
    path('compra/<int:pk>/apaga', CompraDeleteView.as_view(), name='compra-apaga'),

    #Editaveis do funcionario sobre a tabela Produto
    path('produto/novo/', ProdutoCreateView.as_view(), name='produto-novo'),
    path('produto/<int:pk>/apaga', ProdutoDeleteView.as_view(), name= "produto-apaga"),
    path('produto/<int:pk>/atualiza/', ProdutoUpdateView.as_view(), name="produto-atualiza"),
]
