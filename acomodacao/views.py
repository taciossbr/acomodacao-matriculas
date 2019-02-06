from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages

from .forms import HomeForm, CadastroForm, LoginForm, SelectActionForm
from .models import Aluno

# Create your views here.
@require_http_methods("GET")
def home_view(request):
    if request.method == 'GET' and request.GET:
        # aluno = Aluno.objects.get(pk=request.GET['ra'])
        try: 
            aluno = Aluno.objects.get(pk=request.GET['ra'])
            return redirect(login_aluno_view, ra=aluno.ra)
        except ObjectDoesNotExist:
            print('n\n\n\n\n\n9')
            return redirect(cadastro_aluno_view, ra=request.GET['ra'])
    form = HomeForm(request.GET or None)
    return render(request, 'acomodacao/index.html', {'form': form})

@require_http_methods(("GET", "POST"))
def cadastro_aluno_view(request, ra):
    # import pdb; pdb.set_trace()
    if request.method == 'POST' :
        form = CadastroForm(request.POST or None)
        data = request.POST
        if form.is_valid() and data['senha'] == data['confirmacao_senha']:
            user=User.objects.create_user(username=data['ra'].strip(),
                                          password=data['senha'].strip())
            aluno = Aluno.objects.create(ra=data['ra'].strip(),
                                        nome=data['nome'].strip(),
                                        email_contato=data['email_contato'].strip(),
                                        user=user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect(home_view)
    else:
        form = CadastroForm(initial={'ra': ra})
    return render(request, 'acomodacao/cadastro_aluno.html', {'form': form})

@require_http_methods(("GET", "POST"))
def login_aluno_view(request, ra):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['ra'],
                                password=cd['senha'])
            aluno = Aluno.objects.get(pk=cd['ra'])
            if user is not  None and aluno is not None:
                messages.success(request, 'Bem Vindo {}!'.format(aluno.nome))
                return redirect(action_view)
            else:
                messages.error(request, 'RA ou senha inválidos!')
    else:
        form = LoginForm(initial={'ra': ra})
    return render(request, 'acomodacao/login_aluno.html', {'form': form})


def action_view(request):
    form = SelectActionForm()
    return render(request, 'acomodacao/action.html', {'form': form})