from .models import (
    Usuarios, Historico, Clientes, Fornecedores, Produtos,
    Movimentacoes, NotaFiscal, ItemNotaFiscal
)
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
import re


def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

def validar_cnpj(cnpj):
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14 or cnpj in (cnpj[0] * 14 for _ in range(10)):
        return False

    def calcular_digito(cnpj_parcial, pesos):
        soma = sum(int(digito) * peso for digito, peso in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    # 1º dígito
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digito_1 = calcular_digito(cnpj[:12], pesos_1)

    # 2º dígito
    pesos_2 = [6] + pesos_1
    digito_2 = calcular_digito(cnpj[:12] + digito_1, pesos_2)

    return cnpj[-2:] == digito_1 + digito_2


### Formularios ###

class UsuarioForm(forms.ModelForm):
    senha_hash = forms.CharField(widget=forms.PasswordInput())
    CARGO_CHOICES = [
        ('Funcionario', 'Funcionário'),
        ('Gerente', 'Gerente'),
    ]

    cargo = forms.ChoiceField(choices=CARGO_CHOICES)
    
    class Meta:
        model = Usuarios
        fields = '__all__'

    def clean_senha_hash(self):
        senha = self.cleaned_data.get('senha_hash')
        return make_password(senha)
    
    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if Usuarios.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já é cadastrado')
        
        return email
    
class HistoricoForm(forms.ModelForm):
    class Meta:
        model = Historico
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = '__all__'

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf_limpo = re.sub(r'\D', '', cpf)

        if not validar_cpf(cpf) and len(cpf_limpo) != 11:
            raise ValidationError('CPF inválido')
        
        if Clientes.objects.filter(cpf=cpf_limpo).exists():
            raise ValidationError('CPF já é cadastrado')
        
        return cpf_limpo
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj_limpo = re.sub('\D', '', cnpj)

        if not validar_cnpj(cnpj):
            raise ValidationError('CNPJ inválido')

        if Clientes.objects.filter(cnpj=cnpj_limpo):
            raise ValidationError('Este CNPJ já é cadastrado')

        return cnpj_limpo
    
    def clean_telefone(self):
        telefone = self.changed_data['telefone']
        telefone = re.sub('\D', '', telefone)

        return telefone

    def clean_email(self):
        email = self.cleaned_data['email']

        if Clientes.objects.filter(email=email).exists():
            raise ValidationError('Este e-mail já é cadastrado')
        
        return email
    

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedores
        fields = '__all__'

    def clean_cnpj(self):
        cnpj = self.cleaned_data['cnpj']
        cnpj_limpo = re.sub('\D', '', cnpj)

        if not validar_cnpj(cnpj):
            raise ValidationError('CNPJ inválido')

        if Clientes.objects.filter(cnpj=cnpj_limpo):
            raise ValidationError('Este CNPJ já é cadastrado')

        return cnpj_limpo

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        telefone = re.sub('\D', '', telefone)

        return telefone
        

class ProdutoForm(forms.ModelForm):
    validade = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Produtos
        fields = '__all__'

class MovimentacaoForm(forms.ModelForm):
    data_movimentacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Movimentacoes
        fields = '__all__'

class NotaFiscalForm(forms.ModelForm):
    data_emissao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = NotaFiscal
        fields = '__all__'

class ItemNotaFiscalForm(forms.ModelForm):
    class Meta:
        model = ItemNotaFiscal
        fields = '__all__'