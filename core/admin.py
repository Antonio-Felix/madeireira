from django.contrib import admin
from .models import Cliente, Funcionario, Compra, Produto

admin.site.register(Cliente)
admin.site.register(Funcionario)
admin.site.register(Compra)
admin.site.register(Produto)
