from django import forms


class HomeForm(forms.Form):
    ra = forms.CharField(label="RA", max_length=13)

class CadastroForm(forms.Form):
    ra = forms.CharField(max_length=13)
    nome = forms.CharField(max_length=60)
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