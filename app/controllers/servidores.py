import json
from datetime import timedelta

from app.models import *
from app.functions import email
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.functions.validate import *



def salvar(data):
    try:
        servidor = Servidor(
            data['id'] if data['id'] != '' else None,
            (data['nome']).strip(),
            (data['email']).strip(),
            get_clean_number(data['telefone']),
            get_clean_number(data['cpf']),
            data['dataAdmissao'],
            data['cargo'] if data['cargo'] != '' else None,
            data['foto'],
            data['tipo'] if data['tipo'] != '' else None,
        )
        valoresRepetidos = servidor.getRepetido()
        if not empty(valoresRepetidos):
            if len(valoresRepetidos) == 1:
                msg = f"{valoresRepetidos[0]} já cadastrado, por favor, verifique"
            else:
                msg = "Servidor já cadastrado, por favor, verifique"
            return {'success': False, 'msg': msg}
        if servidor.nome.count(" ") == 0:
            return {'success': False, 'msg': 'Por favor, digite o nome completo do funcionário'}
        if not name_validate(servidor.nome):
            return {'success': False, 'msg': 'Por favor, digite um nome válido com apenas letras e espaços'}
        if not cpf_validate(servidor.cpf):
            return {'success': False, 'msg': 'Por favor, digite um CPF válido'}
        if not validate_phone(servidor.telefone):
            return {'success': False, 'msg': 'Por favor, digite um telefone válido'}
        id_servidor = servidor.save()
        if data['id'] == '':
            return vincularEventosEmailaoFuncionario(id_servidor, data['tipo'], data['dataAdmissao'])
        return {'success': True}
    except Exception as e:
        return {'success': False, 'error': e}

def delete(id):
    try:
        servidor = Servidor.query.get_or_404(id)
        email.delete_event_program_email(id)
        db.session.delete(servidor)
        db.session.commit()
        return {"success": True, "msg": "Registro excluído com sucesso"}
    except Exception as e:
        db.session.rollback()
        print(e)
        return {"success": False, "msg": e}
def vincularEventosEmailaoFuncionario(id_servidor, id_tipo, data_admissao):
    tabela_progressao = TiposServidores.query.filter_by(id=id_tipo).first().tabela_progressao
    if tabela_progressao is None:
        return {"success": False, "msg": "Ocorreu um erro ao pegar a tabela de progressão"}
    categoriaEvento = 3 if id_tipo != 3 else 2
    data = datetime.strptime(data_admissao, '%Y-%m-%d')
    for meses in tabela_progressao:
        data += relativedelta(months=meses)
        if data > datetime.now():
            email.create_event_program_email(id_servidor, data, categoriaEvento)
    return {'success': True}
