from django.db import models

# Create your models here.

class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha_hash = models.CharField(max_length=150)
    cargo = models.CharField(max_length=50)
    permissao = models.CharField(max_length=50)

class Historico(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)

class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, blank=True)
    cnpj = models.CharField(max_length=18, blank=True)
    telefone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

class Fornecedores(models.Model):
    cnpj = models.CharField(max_length=18)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

class Produtos(models.Model):
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    codigo = models.IntegerField()
    categoria = models.CharField(max_length=50)
    quantidade_estoque = models.IntegerField()
    validade = models.DateField()
    localizacao = models.CharField(max_length=100)
    preco_custo = models.IntegerField()
    preco_venda = models.IntegerField()

class Movimentacoes(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20)
    quantidade = models.IntegerField()
    data_movimentacao = models.DateField(auto_now_add=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)
    preco_unitario = models.FloatField()
    valor_total = models.FloatField()


