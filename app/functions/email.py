import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models import *
from app.models import execute
from app import scheduler, app
from datetime import datetime
def login_server(server):
    user = "ifrsrh@gmail.com"
    password = "fbys pmxc kpnr utey"
    server.starttls()
    server.login(user, password)

def send(destinatario, assunto, texto):
    remetente = "ifrsrh@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(texto, 'plain', 'utf-8'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    login_server(server)
    server.sendmail(remetente, destinatario, msg.as_string())
    server.quit()

def programar_email(id_destinatario, data_hora_envio, assunto, texto, evento_vinculado, id = None):
    if id is None:
        programacaoEmail = EmailProgramado(None, id_destinatario, data_hora_envio, str(assunto), str(texto), evento_vinculado)
        id = programacaoEmail.save()
    if id:
        scheduler.add_job(
            id=str(id),
            func=submit_email_by_id,
            args=[id],
            trigger="date",
            run_date=data_hora_envio,
        )
        return {'success': True, 'msg': 'E-mail programado com sucesso!'}
    return {'success': False, 'msg': 'Ocorreu um erro ao programar o E-mail'}

def submit_email_by_id(email_id):
    with app.app_context():
        email = EmailProgramado.query.filter_by(id=email_id).first()
        if email and not email.enviado:
            send(email.destinatario, email.assunto, email.texto)
            email.enviado = True
            email.save()

def backup_emails_programados():
    emailsProgramados = EmailProgramado.getProgramacaoEmails()
    for email in emailsProgramados:
        if email['enviado'] == 0:
            if email['data_hora_envio'] <= datetime.now():
                submit_email_by_id(email['id'])
            else:
                existing_job = scheduler.get_job(str(email['id']))
                if not existing_job:
                    programar_email(email['id_destinatario'], email['data_hora_envio'], email['assunto'], email['texto'], email['evento_vinculado'], email['id'])

def create_event_program_email(id_servidor, data, id_categoria):
    servidor = Servidor.query.filter_by(id=id_servidor).first()
    evento = Eventos(None, data, servidor.nome, id_categoria, None, None, None)
    id_evento = evento.save()
    if id_evento is None:
        return {"success": False, "msg": "Ocorreu um erro ao criar o evento"}
    servidor_evento = ServidorEvento(None, id_evento, id_servidor)
    if servidor_evento is None:
        return {"success": False, "msg": "Ocorreu um erro ao vincular evento e servidor"}
    categoria = CategoriaEventos.query.filter_by(id=id_categoria).first()
    return programar_email(id_servidor, data, categoria.descricao, categoria.texto_envio, id_evento, id=None)

def delete_event_program_email(id_servidor):
    idsAgendamentos = execute(
        """SELECT GROUP_CONCAT(id SEPARATOR ',') AS IDs FROM email_programado WHERE id_destinatario = :id_servidor""",
        {"id_servidor": id_servidor})[0]['IDs']
    if idsAgendamentos is not None:
        for id in idsAgendamentos.split(','):
            if scheduler.get_job(str(id)) is not None:
                scheduler.remove_job(str(id))
    execute("""
                DELETE email_programado, eventos
                FROM email_programado
                LEFT JOIN eventos ON email_programado.evento_vinculado = eventos.id
                WHERE email_programado.id_destinatario = :id_servidor;
                """,{"id_servidor": id_servidor})
