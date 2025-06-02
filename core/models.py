from django.db import models
from django.contrib.auth.models import User

class Funcionario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    numero = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    cpf = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=100)
    numero = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome_produto = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome_produto
    
class Compra(models.Model):
    cod = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, through='ItemCompra')
    valor_total_dos_produtos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data = models.DateTimeField(auto_now=True)

    def calcular_valor_total(self):
        total = 0
        for item in self.itemcompra_set.all():
            total += item.produto.valor * item.quantidade
        self.valor_total_dos_produtos = total
        self.save(update_fields=['valor_total_dos_produtos'])

    def __str__(self):
        return f'Compra #{self.cod} - Cliente: {self.cliente.nome}'

class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def subtotal(self):
        return self.produto.valor * self.quantidade