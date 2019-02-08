from django import forms

from .models import Curso


class HomeForm(forms.Form):
    ra = forms.CharField(label="RA", max_length=13)

class CadastroForm(forms.Form):
    ra = forms.CharField(max_length=13)
    primeiro_nome = forms.CharField(max_length=60)
    ultimo_nome = forms.CharField(max_length=60)
    email_contato = forms.EmailField()
    senha = forms.CharField(max_length=16, widget=forms.PasswordInput)
    confirmacao_senha = forms.CharField(max_length=16, 
                                        widget=forms.PasswordInput,
                                        label="Confirmação senha")


class LoginForm(forms.Form):
    ra = forms.CharField(max_length=13)
    senha = forms.CharField(max_length=16, widget=forms.PasswordInput)

class SelectActionForm(forms.Form):
    action = forms.ChoiceField(label='Você deseja ?',
                               choices=(
        ('R', 'Retirar Diciplina'),
        ('I', 'Incluir Disciplina')
    ))



class SelectCursoForm(forms.Form):
    curso = forms.ModelChoiceField(
        label='Da grade de qual curso é a Disciplina?',
        queryset=Curso.objects.all())

class RetirarDisciplinaForm(forms.Form):
    def __init__(self, curso_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].queryset = Curso.objects.get(pk=curso_id).disciplinas.all()
    disciplina = forms.ModelChoiceField(
        label='Disciplina',
        queryset=None)
    dp = forms.BooleanField(
        label='A disciplina que você deseja alterar é uma DP?',
        required=False)

class IncluirDisciplinaForm(forms.Form):
    def __init__(self, curso_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['disciplina'].queryset = Curso.objects.get(pk=curso_id).disciplinas.all()
    disciplina = forms.ModelChoiceField(
        label='Disciplina',
        queryset=None)
