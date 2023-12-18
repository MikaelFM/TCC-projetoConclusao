import base64

from app.models import *
from flask import session
import base64
import requests
def salvar(data):
    try:
        if data['id'] != '':
            arquivo = Arquivos.query.get_or_404(data['id'])
            arquivo.nome = data['nome']
        else:
            arquivo = Arquivos(
                None,
                data['nome'],
                bytes(data['arquivo'], encoding='utf8'),
                data['tipo'],
                data['tamanho'],
                None,
            )
        arquivo.save()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': e}

def decode_base64(arquivo_base64):
    try:
        arquivo_base64 = arquivo_base64.split(',')
        arquivo_bytes = base64.b64decode(arquivo_base64)

        return arquivo_bytes
    except Exception as e:
        print(f"Erro ao decodificar base64: {e}")
        return None

def delete(id):
    arquivo = Arquivos.query.get_or_404(id)
    db.session.delete(arquivo)
    db.session.commit()
    return {'success': True}