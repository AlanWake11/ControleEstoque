"""
URL configuration for projeto_TCC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_projeto_TCC import views


urlpatterns = [

    # Paginas Webs #
    path('', views.verificar_bd, name='start_page'),
    path('admin/', admin.site.urls, name='admin_page'),
    path('cadastro/', views.cadastro_page, name='cadastro_page'),
    path('cadastroCliente/', views.cadastroCliente_page, name= 'cadastroCliente_page'),
    path('cadastroFornecedor/', views.cadastroFornecedor_page, name='cadastroFornecedor_page'),
    path('cadastroProduto', views.cadastroProduto_page, name='cadastroProduto_page'),
    path('cadastroUsuario/', views.cadastroUsuario_page, name='cadastroUsuario_page'),
    path('notaFiscal/', views.cadastroNotaFiscal_page, name='cadastroNotaFiscal_page'),
    path('login/', views.login_page, name='login_page'),
    path('home/', views.home_page, name='home_page'),
    path('exibicaoCliente/', views.exibir_clientes_page, name='exibir_clientes_page'),
    path('exibicaoFornecedor/', views.exibir_fornecedores_page, name='exibir_fornecedores_page'),
    path('exibicaoProduto/', views.exibir_produtos_page, name='exibir_produtos_page'),
    path('exibicaoUsuario/', views.exibir_usuarios_page, name='exibir_usuarios_page'),

    # Funções Webs #
    path('cadastrarAdmin/', views.cadastrar_admin, name='cadastrar_admin'),
    path('loginUsuario/', views.login_usuario, name='logar_usuario'),
    path('cadastrarCliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('cadastrarUsuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('cadastroProduto/', views.cadastro_produto, name='cadastro_produto')

]  
