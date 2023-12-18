from apscheduler.jobstores.base import JobLookupError

from app import app, scheduler
from flask import Flask, request, redirect, jsonify, session, g, url_for
from app.functions import custom_render_template as render_template, empty, get_html_main_pages, get_html_from
from app.controllers import register_login, main_page, servidores, eventos, arquivos
from flask_login import logout_user


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/loginSubmit", methods=['POST'])
def loginSubmit():
    return register_login.login(request.form['email'], request.form['password'], request.form['remember'])


@app.route("/register")
def registreSe():
    return render_template("register.html", title="Registre-se", styles=['/login/login.css'])


@app.route("/registerSubmit", methods=['POST'])
def registerSubmit():
    return register_login.save(
        request.form['nome'],
        request.form['email'],
        request.form['telefone'],
        request.form['cpf'],
        request.form['password']
    )


@app.route("/emailConfirmation", methods=['POST'])
def emailConfirmation():
    return render_template("confirmation.html", title="Confirme seu e-mail", email=request.form['email'])


@app.route("/passwordRecovery")
def passRecovery():
    return render_template("recovery.html", title="Recuperação de Senha")


@app.route("/confirmation/<token>", methods=['GET'])
def confirmation(token):
    return register_login.confirmEmail(token)


@app.route("/recovery/<token>", methods=['GET'])
def recovery(token):
    return register_login.recoveryPassoword(token)

@app.route("/corrigirEmail", methods=['POST'])
def corrigirEmail():
    register_login.corrigirEmail(
        request.form['oldEmail'],
        request.form['newEmail']
    )
    return render_template("confirmation.html", title="Confirme seu e-mail", styles=['sendEmailStyles.css'],
                           scripts=['sendEmailFunctions.js'], email=request.form['newEmail'])


@app.route("/sendConfirmation", methods=['POST'])
def sendConfirmation():
    return register_login.makeEmailConfirmation(
        request.form['email']
    )


@app.route("/sendRecovery", methods=['POST'])
def sendRecovery():
    return register_login.makePasswordRecovery(
        request.form['email'],
    )


@app.route("/checkEmailExists", methods=['POST'])
def checkEmailExists():
    return register_login.checkEmailExists(
        request.form['email'],
    )


@app.route("/saveNewPass", methods=['POST'])
def saveNewPass():
    return register_login.saveNewPassword(request.form['token'], request.form['password'])


@app.route("/invalidToken")
def invalidToken():
    return render_template("return_token.html", styles=["confirmation.css"])


@app.route("/")
def index():
    if 'user_id' in session:
        return render_template("main/index.html")
    return redirect('/login')


@app.route("/getDados")
def getDados():
    if not 'user_id' in session:
        return redirect('/login')
    return {'success': True, 'logado': True, 'dados': main_page.getDados()}


@app.route("/getHTML")
def getHTML():
    return get_html_main_pages()


@app.route("/getHTML/<path>", methods=['GET'])
def getHTMLpath(path):
    return {'html': get_html_from(f"modals/{path}")}


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    logout_user()
    return redirect('/login')


@app.route("/saveFuncionario", methods=['POST'])
def saveFuncionario():
    return servidores.salvar(request.form)
@app.route("/deleteFuncionario", methods=['POST'])
def deleteFuncionario():
    return servidores.delete(request.form['id'])
@app.route("/saveEvento", methods=['POST'])
def saveEvento():
    return eventos.salvar(request.form)

@app.route("/deleteEvento", methods=['POST'])
def deleteEvento():
    return eventos.delete(request.form['id'])
@app.route("/saveArquivo", methods=['POST'])
def saveArquivo():
    return arquivos.salvar(request.form)

@app.route("/deleteFile", methods=['POST'])
def deleteFile():
    return arquivos.delete(request.form['id'])
@app.route("/tasks")
def tasks():
    try:
        tarefas_agendadas = scheduler.get_jobs()

        tasks_info = []
        for tarefa in tarefas_agendadas:
            task_info = {
                "id": tarefa.id,
                "name": tarefa.name,
                "next_run_time": str(tarefa.next_run_time),
            }
            tasks_info.append(task_info)

        return jsonify(tasks_info)
    except JobLookupError as e:
        return f"Erro ao obter informações das tarefas: {e}", 500
