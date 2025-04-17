from django.db import models

# Create your models here.

# Cliente que faz pedidos
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.TextField()

    def __str__(self):
        return self.nome

# Produto que será transportado
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    peso = models.FloatField(help_text="Peso em kg")
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

# Pedido feito por um cliente
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('Pendente', 'Pendente'),
        ('Em Transporte', 'Em Transporte'),
        ('Entregue', 'Entregue'),
        ('Cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pendente')

    def __str__(self):
        return f'Pedido {self.id} - {self.cliente.nome}'

# Itens dentro de um pedido
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})'

# Transportadora responsável pela entrega
class Transportadora(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.nome

# Registro de entrega
class Entrega(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE)
    data_saida = models.DateTimeField()
    data_prevista_entrega = models.DateTimeField()
    data_real_entrega = models.DateTimeField(blank=True, null=True)
    status_choices = [
        ('A Caminho', 'A Caminho'),
        ('Entregue', 'Entregue'),
        ('Atrasado', 'Atrasado'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='A Caminho')

    def __str__(self):
        return f'Entrega do Pedido {self.pedido.id} - {self.status}'