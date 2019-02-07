from functools import wraps

from .models import Aluno, Submissao

def require_session(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        sub_id = request.session.get('submissao')
        if request.session.get('submissao') is None:
            ra = request.user.username
            aluno = Aluno.objects.get(pk=ra)
            sub = Submissao.objects.create(aluno=aluno)
            request.session['submissao'] = sub.id
            request.session['solicitacoes'] = []
        return f(request, *args, **kwargs)
    return wrap