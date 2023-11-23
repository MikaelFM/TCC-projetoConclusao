import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_apscheduler import APScheduler
from app.models import EmailProgramado, Registros
from app import scheduler, db
from datetime import datetime
def login_server(server):
    user = "ifrsrh@gmail.com"
    password = "fbys pmxc kpnr utey"
    server.starttls()
    server.login(user, password)

def send(destinatario, assunto, texto, id = None):
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

    if id is not None:
        programacaoEmail = EmailProgramado.query.filter_by(id=id).first()
        programacaoEmail.enviado = True
        programacaoEmail.save()

    print("Email enviado")

def programar_email(destinatario, assunto, texto, data_hora_envio):
    programacaoEmail = EmailProgramado(destinatario, data_hora_envio, assunto, texto)
    save = programacaoEmail.save()
    if save:
        scheduler.add_job(
            id="my_job",
            func=send,
            args=[destinatario, assunto, texto, save],
            trigger="date",
            run_date=data_hora_envio,
        )
        return {'success': True, 'msg': 'E-mail programado com sucesso!'}
    return {'success': False, 'msg': 'Ocorreu um erro ao programar o E-mail'}

def backup_emails_programados():
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    emailsProgramados = EmailProgramado.getProgramacaoEmails()
    for email in emailsProgramados:
        if email['data_hora_envio'] <= datetime.now():
            print("ba")
        else:
            scheduler.add_job(
                id="my_job",
                func=send,
                args=[email['destinatario'], email['assunto'], email['texto'], email['id']],
                trigger="date",
                run_date=email['data_hora_envio'],
            )
        print(email)