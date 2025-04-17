from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

# Funções #

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
                messages.error(request, "Email não encontrado")
                return redirect('inicio')  
        
        return render(request, 'Cadastro/index.html')
    
    except Exception as e:
        return HttpResponse(e)

# Paginas Webs #

def start_page(request):
    logout_usuario(request)
    return render(request, 'Cadastro/index.html')

def cadastro_page(request):
    logout_usuario(request)
    if User.objects.exists():
        return render(request, 'Cadastro/login.html')
    return render(request, 'Cadastro/cadastro.html')

def login_page(request):
    logout_usuario(request)
    verificar_bd(request)
    return render(request, 'Cadastro/login.html')

@login_required(login_url='start_page')
def home_page(request):
    return render(request, 'admin/Inicio/index.html')

@login_required(login_url='start_page')
def cadastroFuncionario_page(request):
    return render(request, 'admin/Inicio/cadastrar_funcionario.html')

@login_required(login_url='start_page')
def dashboard_page(request):
    return render(request, 'admin/Inicio/dashboard.html')