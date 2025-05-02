from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from .models import Clientes, Fornecedores, Historico, Movimentacoes, Usuarios, Produtos
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

# Create your views here.

### Funções ###

# Verifica se o banco de dados está vazio, se sim, cadastra o administrador
def verificar_bd(request):
    try:
        if not User.objects.exists():
            return redirect('cadastro_page')
        else:
            return redirect('login_page')
    except Exception as e:
        return HttpResponse(f'Erro ao verificar o banco de dados: {e}')

# Logout do usuario
def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)

# Cadastrar o administrador 
def cadastrar_admin(request):
    try:
        if User.objects.filter(is_superuser=True).exists():
            return HttpResponse('Administrador já cadastrado!')

        if request.method == "POST":
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            
            User.objects.create_superuser(username=nome, email=email, password=senha)
            user = authenticate(username=nome, password=senha)
            login_django(request, user)
            
            return redirect('home_page')
        
        return render(request, "Cadastro/index.html")
    
    except Exception as e:
        return HttpResponse(e)

# Logar usuario
def login_usuario(request):
    try:
        if request.method == "POST":
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            usuario = User.objects.filter(email=email).first()
            if usuario:
                user = authenticate(username=usuario.username, password=senha)
                if user:
                    login_django(request, user)
                    request.session['username'] = user.username
                    return redirect('home_page')
                else:
                    messages.error(request, 'Senha incorreta')
            else:
                
                return redirect('home_page')  
        
        return render(request, 'Cadastro/index.html')
    
    except Exception as e:
        return HttpResponse(e)


### Cadastros ###

def cadastro_cliente(request):
    try: 
        if request.method == 'POST':
            novo_cliente = Clientes()
            novo_cliente.nome = request.POST.get('nome')
            novo_cliente.telefone = request.POST.get('telefone')
            novo_cliente.email = request.POST.get('email')
            
            cpf_cnpj = request.POST.get('documento')
            if len(cpf_cnpj) == 11:
                novo_cliente.cpf = cpf_cnpj
            elif len(cpf_cnpj) == 14:
                novo_cliente.cnpj = cpf_cnpj
            else:
                return HttpResponse('Não é CPF, nem CNPJ')

            if len(novo_cliente.telefone) != 10:
                messages.error(request, 'Numero de telefone invalido')
                return redirect('home_page')

            novo_cliente.save()
            messages.success(request, 'Cadastro do cliente realizado com sucesso!')

            return redirect('home_page')

    except Exception as e:
        messages.error(request, e)
        return redirect('home_page') 

def cadastro_usuario(request):
    try:
        if request.method == 'POST':
            novo_usuario = Usuarios()
            novo_usuario.nome = request.POST.get('nome')
            novo_usuario.cpf = request.POST.get('documento')
            novo_usuario.email = request.POST.get('email')
            novo_usuario.telefone = request.POST.get('telefone')
            novo_usuario.cargo = request.POST.get('cargo')
            senha = request.POST.get('senha')
            senha_hash = make_password(senha)
            novo_usuario.senha_hash = senha_hash

            if Usuarios.objects.filter(email=novo_usuario.email).exists():
                return HttpResponse('Email já cadastrado!')

            novo_usuario.save()
            messages.success(request, 'Usuario cadastrado com sucesso!')
            
            return redirect('home_page')

    except Exception as e:
        messages.error(request, e)
        return redirect('home_page')

def cadastro_produto(request):
    try:
        if request.method == 'POST':
            novo_produto = Produtos()
            novo_produto.nome = request.POST.get('nome')
            novo_produto.codigo = request.POST.get('codigo')
            novo_produto.categoria = request.POST.get('categoria')
            novo_produto.quantidade_estoque = request.POST.get('quantidade')
            novo_produto.localizacao = request.POST.get('localizacao')
            novo_produto.validade = request.POST.get('validade')
            novo_produto.preco_custo = request.POST.get('preco_custo')
            novo_produto.preco_venda = request.POST.get('preco_venda')
            novo_produto.fornecedor = request.POST.get('fornecedor_id')

            novo_produto.save()
            messages.success(request, 'Produto cadastrado com sucesso!')

            return redirect('home_page')


    except Exception as e:
        messages.error(request, e)
        return redirect('home_page')

def cadastro_fornecedor(request):
    try:
        if request.method == 'POST':
            novo_fornecedor = Fornecedores()
            novo_fornecedor.nome = request.POST.get('nome')
            novo_fornecedor.cnpj = request.POST.get('documento')
            novo_fornecedor.telefone = request.POST.get('telefone')
            novo_fornecedor.email = request.POST.get('email')

            novo_fornecedor.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')

            return redirect('home_page')
        
    except Exception as e:
        messages.error(request, e)
        return redirect('home_page')



# Paginas Webs #

def start_page(request):
    logout_usuario(request)
    return render(request, 'cadastro/index.html')

def cadastro_page(request):
    logout_usuario(request)
    if User.objects.exists():
        return render(request, 'cadastro/login.html')
    return render(request, 'cadastro/cadastro.html')

def login_page(request):
    logout_usuario(request)
    verificar_bd(request)
    return render(request, 'cadastro/login.html')

@login_required(login_url='start_page')
def home_page(request):
    return render(request, 'admin/Inicio/index.html')

@login_required(login_url='start_page')
def dashboard_page(request):
    return render(request, 'exibicao/dashboard.html')

@login_required(login_url='start_page')
def cadastroUsuario_page(request):
    return render(request, 'cadastro/cadastroUsuario.html')

@login_required(login_url='start_page')
def cadastroCliente_page(request):
    return render(request, 'cadastro/cadastroCliente.html')

@login_required(login_url='start_page')
def cadastroFornecedor_page(request):
    return render(request, 'cadastro/cadastroFornecedor.html')

@login_required(login_url='start_page')
def cadastroProduto_page(request):
    return render(request, 'cadastro/cadastroProduto.html')

@login_required(login_url='start_page')
def cadastroNotaFiscal_page(request):
    return render(request, 'cadastro/notafiscal.html')

@login_required(login_url='start_page')
def exibir_clientes_page(request):
    clientes = {
        'clientes': Clientes.objects.all()
    }
    return render(request, 'exibicao/exibirCliente.html', clientes)

@login_required(login_url='start_page')
def exibir_fornecedores_page(request):
    fornecedores = {
        'fornecedores': Fornecedores.objects.all()
    }
    return render(request, 'exibicao/exibirFornecedor.html', fornecedores)
    
@login_required(login_url='start_page')
def exibir_usuarios_page(request):
    usuarios = {
        'usuarios': Usuarios.objects.all()
    }  
    return render(request, 'exibicao/exibirUsuario.html', usuarios)

@login_required(login_url='start_page')
def exibir_produtos_page(request):
    produtos = {
        'produtos': Produtos.objects.all()
    }
    return render(request, 'exibicao/exibirProduto.html', produtos)
