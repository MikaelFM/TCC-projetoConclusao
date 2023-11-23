from app.models import *
def salvar(data):
    try:
        servidor = Servidor(
            data['id'] if data['id'] != '' else None,
            data['nome'],
            data['email'],
            data['telefone'],
            data['cpf'],
            data['dataAdmissao'],
            data['cargo'] if data['cargo'] != '' else None,
            data['foto'],
            data['tipo'] if data['tipo'] != '' else None,
        )
        servidor.save()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': e}
