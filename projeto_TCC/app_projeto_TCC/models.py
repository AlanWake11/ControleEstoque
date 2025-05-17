from django.db import models

# Create your models here.

# Entidades #

class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha_hash = models.CharField(max_length=150)
    cargo = models.CharField(max_length=50)
    permissao = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Historico(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    acao = models.CharField(max_length=255)
    data_hora = models.DateTimeField(auto_now_add=True)

class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Fornecedores(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Produtos(models.Model):
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    codigo = models.PositiveBigIntegerField(unique=True)
    categoria = models.CharField(max_length=50, choices=[('Tecnologia','Tecnologia')])
    quantidade_estoque = models.PositiveIntegerField(default=0)
    validade = models.DateField()
    localizacao = models.CharField(max_length=100)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=20, default='Unidade' ,choices=[('Unidade', 'Unidade'), ('Kg','Kg'), ])

    def __str__(self):
        return self.nome    

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

class NotaFiscal(models.Model):
    numero = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=[('Entrada', 'Entrada'), ('Saída', 'Saída')])
    operacao = models.CharField(max_length=20, choices=[('Perda_Estrago', 'Perda/Estrago'), ('Transf.Emprestimo','Transf.Empréstimo'),('Transf.Retorno','Transf.Retorno'),('Transferencia','Transferência'),('Venda_Atacado','Venda Atacado'),('Venda_Varejo','Venda Varejo'),])
    status = models.CharField(max_length=20, choices=[('Ativo','Ativo'),('Cancelado','Cancelado'),('Pendente','Pendente')] ,default='Ativo')
    data_emissao = models.DateField()
    remetente = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    deposito = models.CharField(max_length=100)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.remetente

class ItemNotaFiscal(models.Model):
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nota_fiscal
