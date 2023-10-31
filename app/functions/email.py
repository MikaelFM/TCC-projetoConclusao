import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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