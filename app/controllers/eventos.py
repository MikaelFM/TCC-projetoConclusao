from app.models import *
def salvar(data):
    try:
        evento = Eventos(
            data['id'] if data['id'] != '' else None,
            data['data'],
            data['descricao'],
            1,
            None,
            None,
            data['privacidade'],
        )
        evento.save()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': e}

def delete(id):
    evento = Eventos.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return {'success': True}