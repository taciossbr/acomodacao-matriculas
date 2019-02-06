from django.urls import path

from .views import home_view, cadastro_aluno_view, login_aluno_view, action_view

urlpatterns = [
    path('', home_view),
    path('aluno/cadastrar/<int:ra>', cadastro_aluno_view), 
    path('aluno/cadastrar/', cadastro_aluno_view, {'ra': None}), 
    path('aluno/login/<int:ra>', login_aluno_view), 
    path('aluno/login/', login_aluno_view, {'ra': None}), 
    path('aluno/action/', action_view)
]
