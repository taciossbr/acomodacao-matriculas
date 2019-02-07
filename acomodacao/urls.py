from django.urls import path

from .views import ( home_view, cadastro_aluno_view, login_aluno_view, 
                     action_view, logout_view, retirar_disciplina_view,
                     incluir_disciplina_view, revisar_submissao_view,
                     submissao_view )

urlpatterns = [
    path('', home_view, name='home'),
    path('aluno/cadastrar/<int:ra>', cadastro_aluno_view), 
    path('aluno/cadastrar/', cadastro_aluno_view, {'ra': None}), 
    path('aluno/login/<int:ra>', login_aluno_view), 
    path('aluno/login/', login_aluno_view, {'ra': None}), 
    path('aluno/revisar/', revisar_submissao_view, name='revisar_submissao'), 
    path('aluno/submeter/', submissao_view, name='submeter'), 
    path('aluno/action/<int:curso_id>', action_view),
    path('aluno/action/<int:curso_id>/r/', retirar_disciplina_view),
    path('aluno/action/<int:curso_id>/i/', incluir_disciplina_view),
    path('aluno/logout/', logout_view, name='logout'),

]
