from usuarios.models import Usuarios

def get_perfil_logado(request):
    """
    Função para retornar o perfil do usuário logado.
    """
    return Usuarios.objects.select_related().get(username=request.user)
