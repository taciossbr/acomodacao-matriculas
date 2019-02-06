from django.contrib import admin

from .models import Aluno, Curso, Disciplina, SolicitacaoAlteracao, Submissao
# Register your models here.
admin.site.register(Aluno)
admin.site.register(Curso)
admin.site.register(Disciplina)
# admin.site.register(SolicitacaoAlteracao)
# admin.site.register(Submissao)