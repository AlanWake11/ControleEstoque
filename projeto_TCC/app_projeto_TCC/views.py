from .models import *
from .forms import *
from django.forms import modelformset_factory, inlineformset_factory
from django.db import DatabaseError, transaction
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
import json


# Create your views here.

### Login ###

# Verifica se o banco de dados está vazio, se sim, cadastra o administrador
def verificar_bd(request):
    try:
        if not User.objects.exists():
            return redirect('cadastro_page')
        else:
            return redirect('login_page')
    except Exception as e:
        return HttpResponse(f'Erro ao verificar o banco de dados: {e}')

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

# Logout do usuario
def logout_usuario(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('start_page')

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
                    return redirect('home_page')
                else:
                    messages.error(request, 'Senha incorreta')
            else:
                
                return redirect('home_page')  
        
        return render(request, 'Cadastro/index.html')
    
    except Exception as e:
        return HttpResponse(e)


### Cadastros ###

# def cadastro_cliente(request):
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

# Cadastrar cliente
def cadastro_cliente(request):
    try:
        if request.method == "POST":
            form = ClienteForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Cadastro do cliente realizado com sucesso!')
                
                return redirect('home_page')
            else:
                return render(request, 'cadastro/cadastroCliente.html', {'form':form})

    except DatabaseError as e:
        messages.error(request, f'Erro no banco de dados: {str(e)}')
        return redirect('home_page')

    except Exception as e:
        return HttpResponse(e)

# Cadastrar Usuario
def cadastro_usuario(request):
    try:
        if request.method == 'POST':
            form = UsuarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario cadastrado com sucesso!')
                return redirect('home_page')
            
            else:
                return render(request, 'cadastro/cadastroUsuario.html', {'form':form})

    except Exception as e:
        messages.error(request, e)
        return redirect('home_page')

def cadastro_produto(request):
    try:
        if request.method == 'POST':
            form = ProdutoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto cadastrado com sucesso!')
                return redirect('home_page')
            else:
                messages.warning(request, 'Houve uma falha')
                return redirect('home_page')

    except Exception as e:
        messages.error(request, e)
        return redirect('home_page')

def cadastro_fornecedor(request):
    try:
        if request.method == 'POST':
            form = FornecedorForm(request.POST)
            if form.is_valid():
               messages.success(request, 'Fornecedor cadastrado com sucesso!')
               form.save()

               return redirect('home_page')
            
            else:
                return render(request,'cadastro/cadastroFornecedor.html',{'form':form})

    except Exception as e:
        messages.error(request, e)
        return redirect('home_page')

@require_http_methods(["GET", "POST"])
def cadastro_nota_fiscal(request):
    if request.method == "POST":
        try:
            # Dados do formulário
            tipo = request.POST.get("tipo")
            operacao = request.POST.get("operacao")
            deposito = request.POST.get("deposito")
            status = request.POST.get("status")
            numero = request.POST.get("numero")
            remetente = request.POST.get("remetente")
            data_emissao = request.POST.get("data") or None
            responsavel_nome = request.POST.get("responsavel")
            valor_total = request.POST.get("valorTotal") or 0
            itens_json = request.POST.get("itensNota")

            # Buscar o responsável (usuário) pelo nome
            responsavel = Usuarios.objects.filter(nome=responsavel_nome).first() if responsavel_nome else None

            # Começar transação
            with transaction.atomic():
                # Criar nota fiscal
                nota = NotaFiscal.objects.create(
                    tipo=tipo,
                    operacao=operacao,
                    deposito=deposito,
                    status=status,
                    numero=numero,
                    remetente=remetente,
                    data_emissao=data_emissao,
                    responsavel=responsavel,
                    valor_total=valor_total
                )

                # Processar e criar itens
                itens = json.loads(itens_json or "[]")
                for item in itens:
                    produto = Produtos.objects.get(codigo=item["codigo"])  # ajuste conforme seu modelo
                    quantidade = int(item.get("quantidade", 0))
                    valor_unitario = float(item.get("valorUnitario", 0))
                    valor_total_item = round(quantidade * valor_unitario, 2)

                    ItemNotaFiscal.objects.create(
                        nota_fiscal=nota,
                        produto=produto,
                        quantidade=quantidade,
                        valor_unitario=valor_unitario,
                        valor_total=valor_total_item
                    )

            messages.success(request, "Nota fiscal cadastrada com sucesso!")
            return redirect('home_page')  # ou outra view/URL conforme seu fluxo

        except Produtos.DoesNotExist:
            messages.error(request, "Produto não encontrado.")
        except json.JSONDecodeError:
            messages.error(request, "Erro ao processar os itens da nota.")
        except Exception as e:
            messages.error(request, f"Erro ao salvar nota fiscal: {str(e)}")

    return render(request, 'admin/Inicio/index.html')

### Paginas Webs ###

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
    form = UsuarioForm()
    return render(request, 'cadastro/cadastroUsuario.html', {'form': form})

@login_required(login_url='start_page')
def cadastroCliente_page(request):
    form = ClienteForm()
    return render(request, 'cadastro/cadastroCliente.html', {'form' : form})

@login_required(login_url='start_page')
def cadastroFornecedor_page(request):
    form = FornecedorForm()
    return render(request, 'cadastro/cadastroFornecedor.html', {'form':form})

@login_required(login_url='start_page')
def cadastroProduto_page(request):
    form = ProdutoForm()
    return render(request, 'cadastro/cadastroProduto.html', {'form': form})

@login_required(login_url='start_page')
def cadastroNotaFiscal_page(request):
    ItemFormSet = inlineformset_factory(
        NotaFiscal, ItemNotaFiscal, form=ItemNotaFiscalForm,
        extra=1, can_delete=True
    )
    
    nota_form = NotaFiscalForm()
    formset = ItemFormSet()
    
    return render(request, 'cadastro/notafiscal.html', {'nota_form':nota_form, 'formset':formset})

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

@login_required(login_url='start_page')
def exibir_notasFiscais_page(request):
    notas_fiscais = {
        'notas_fiscais':NotaFiscal.objects.all()
    }
    return render(request, 'exibicao/exibirNotaFiscal.html', notas_fiscais)

@login_required(login_url='start_page')
def exibirProdutoNotaFiscal_page(request):
    produtos = {
        'produtos':Produtos.objects.all()
    }
    return render(request, 'cadastro/exibirProdutoNotaFiscal.html', produtos)