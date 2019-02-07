from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ra = models.CharField(max_length=13, primary_key=True)
    nome = models.CharField(max_length=60, null=False)
    email_contato = models.EmailField()

    def __str__(self):
        return "{} ({})".format(self.nome, self.ra)


class Disciplina(models.Model):
    sigla = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=50, null=False)

    def __str__(self):
        return "{} - {}".format(self.sigla, self.nome)


class Curso(models.Model):
    nome = models.CharField(max_length=50, null=False)
    disciplinas = models.ManyToManyField(Disciplina)

    def __str__(self):
        return self.nome


class SolicitacaoAlteracao(models.Model):
    submissao = models.ForeignKey('Submissao', on_delete=models.CASCADE)
    disciplina = models.ForeignKey('Disciplina', on_delete=models.CASCADE)
    acao = models.CharField(max_length=1, choices=(
        ('R', 'Retirar Diciplina'),
        ('I', 'Incluir Disciplina')
    ))
    dp = models.BooleanField(default=False)


class Submissao(models.Model):
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now=True)
