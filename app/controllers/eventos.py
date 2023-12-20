import json

from app.models import *
def salvar(data):
    try:
        evento = Eventos(
            data['id'] if data['id'] != '' else None,
            data['data'],
            data['descricao'],
            1,
            (session['user_id'] if session['type'] == 'servidor' else None),
            data['privacidade'] if data['privacidade'] != '' else None,
        )
        idEvento = evento.save()
        ServidorEvento.deleteByEvent(idEvento)

        if len(json.loads(data['servidoresVinculados'])) > 0:
            for idServidor in json.loads(data['servidoresVinculados']):
                servidorEvento = ServidorEvento(None, idEvento, idServidor)
                servidorEvento.save()

        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': e}

def delete(id):
    ServidorEvento.deleteByEvent(id)
    evento = Eventos.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return {'success': True}