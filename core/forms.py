from django import forms
from django.contrib.auth.models import User
from .models import Funcionario
from django.forms import inlineformset_factory
from .models import Compra, ItemCompra

class FuncionarioRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Funcionario
        fields = ['cpf', 'nome', 'idade', 'numero', 'email']

    def save(self, commit=True):
        funcionario = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['cpf'],
            password=self.cleaned_data['password']
        )
        funcionario.user = user
        if commit:
            user.save()
            funcionario.save()
        return funcionario
    
    
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['cliente']

ItemCompraFormSet = inlineformset_factory(
    Compra,
    ItemCompra,
    fields=('produto', 'quantidade'),
    extra=10,
    can_delete=False
)