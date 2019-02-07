from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.forms.models import model_to_dict

from .forms import ( HomeForm, CadastroForm, LoginForm, SelectActionForm, 
                    SelectCursoForm, RetirarDisciplinaForm, 
                    IncluirDisciplinaForm)
from .models import Aluno, Submissao, SolicitacaoAlteracao, Disciplina
from .helpers  import require_session

# Create your views here.
@require_http_methods(("GET", 'POST'))
def home_view(request):
    if request.user.is_authenticated:
        # import pdb; pdb.set_trace()
        if request.method == 'POST':
            form = SelectCursoForm(request.POST)
            if form.is_valid():
                return redirect(action_view, curso_id=form.cleaned_data['curso'].id)
            return render(request, 'acomodacao/action.html', {'form': form})
            
        else:
            form = SelectCursoForm()

        return render(request, 'acomodacao/action.html', {'form': form})
    if request.method == 'GET' and request.GET:
        # aluno = Aluno.objects.get(pk=request.GET['ra'])
        try: 
            aluno = Aluno.objects.get(pk=request.GET['ra'])
            return redirect(login_aluno_view, ra=aluno.ra)
        except ObjectDoesNotExist:
            return redirect(cadastro_aluno_view, ra=request.GET['ra'])
    form = HomeForm(request.GET or None)
    return render(request, 'acomodacao/index.html', {'form': form})

@require_http_methods(("GET", "POST"))
def cadastro_aluno_view(request, ra):
    # import pdb; pdb.set_trace()
    if request.method == 'POST' :
        form = CadastroForm(request.POST or None)
        data = request.POST
        if form.is_valid():
            if data['senha'] == data['confirmacao_senha']:
                user=User.objects.create_user(username=data['ra'].strip(),
                                                password=data['senha'].strip())
                aluno = Aluno.objects.create(ra=data['ra'].strip(),
                                            nome=data['nome'].strip(),
                                            email_contato=data['email_contato'].strip(),
                                            user=user)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect(home_view)
            else:
                messages.error(request, 
                               'Senha e confirmação de Senha não conferem')
                return render(request, 'acomodacao/cadastro_aluno.html', {'form': form})

        else:
            messages.error(request, 'Formulário Inválido')
            return render(request, 'acomodacao/cadastro_aluno.html', {'form': form})
    else:
        form = CadastroForm(initial={'ra': ra})
    return render(request, 'acomodacao/cadastro_aluno.html', {'form': form})

@require_http_methods(("GET", "POST"))
def login_aluno_view(request, ra):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                username=cd['ra'],
                                password=cd['senha'])
            aluno = Aluno.objects.get(pk=cd['ra'])
            if user is not  None and aluno is not None:
                login(request, user)
                messages.success(request, 'Bem Vindo {}!'.format(aluno.nome))
                return redirect(home_view)
            else:
                messages.error(request, 'RA ou senha inválidos!')
    else:
        form = LoginForm(initial={'ra': ra})
    return render(request, 'acomodacao/login_aluno.html', {'form': form})

@require_http_methods(("GET", "POST"))
@require_session
def action_view(request, curso_id):
    sub_id = request.session.get('submissao')

    form = SelectActionForm()
    if request.method == 'POST':
        form = SelectActionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['action'] == 'R':
                return redirect(retirar_disciplina_view, curso_id=curso_id)
            elif cd['action'] == 'I':
                return redirect(incluir_disciplina_view, curso_id=curso_id)
            else:
                messages.error(request, 'Opção Inválida')
    return render(request, 'acomodacao/action.html', {
            'form': form,
            'sub_id': sub_id
        })

@require_http_methods(("GET", "POST"))
@require_session
def retirar_disciplina_view(request, curso_id):
    sub_id = request.session.get('submissao')
    form = RetirarDisciplinaForm(curso_id=curso_id)
    if request.method == 'POST':
        form = RetirarDisciplinaForm(curso_id, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sol = SolicitacaoAlteracao(
                submissao = Submissao.objects.get(pk=sub_id),
                acao='R',
                **cd)
            l = request.session['solicitacoes']
            l.append(model_to_dict(sol))
            l = list({v['disciplina']: v for v in l}.values())
            request.session['solicitacoes'] = l
    return render(request, 'acomodacao/action.html', {
        'sub_id': sub_id,
        'form': form
    })


@require_http_methods(("GET", "POST"))
@require_session
def incluir_disciplina_view(request, curso_id):
    sub_id = request.session.get('submissao')
    form = IncluirDisciplinaForm(curso_id=curso_id)
    if request.method == 'POST':
        form = IncluirDisciplinaForm(curso_id, request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            sol = SolicitacaoAlteracao(
                submissao = Submissao.objects.get(pk=sub_id),
                acao='I',
                **cd)
            l = request.session['solicitacoes']
            l.append(model_to_dict(sol))
            l = list({v['disciplina']: v for v in l}.values())
            request.session['solicitacoes'] = l
    return render(request, 'acomodacao/action.html', {
        'sub_id': sub_id,
        'form': form
    })


@require_http_methods(("GET"))
@require_session
def revisar_submissao_view(request):

    solicitacoes = []
    for data in request.session['solicitacoes']:
        submissao = Submissao.objects.get(pk=data['submissao'])
        disciplina = Disciplina.objects.get(pk=data['disciplina'])
        solicitacao = SolicitacaoAlteracao(
            submissao=submissao,
            disciplina=disciplina,
            acao=data['acao'],
            dp=data['dp'])
        solicitacoes.append(solicitacao)

    return render(request, 'acomodacao/revisar.html', {
        'solicitacoes': solicitacoes
    })


@require_http_methods(("GET", "POST"))
@require_session
def submissao_view(request):

    solicitacoes = []
    for data in request.session['solicitacoes']:
        submissao = Submissao.objects.get(pk=data['submissao'])
        disciplina = Disciplina.objects.get(pk=data['disciplina'])
        solicitacao = SolicitacaoAlteracao(
            submissao=submissao,
            disciplina=disciplina,
            acao=data['acao'],
            dp=data['dp'])
        solicitacao.save()
        solicitacoes.append(solicitacao)

    if len(solicitacoes) == 0:
        messages.error(request, 'Impossivel realizar Solicitação Vazia')
        return redirect(home_view)
    submissao.save()
    messages.success(request, '''Submissão realisado com Sucesso!''')
    del request.session['submissao']
    del request.session['solicitacoes']
    return render(request, 'acomodacao/submeter.html', {
        'solicitacoes': solicitacoes,
        'submissao': submissao
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'Até a Próxima')
    return redirect(home_view)
