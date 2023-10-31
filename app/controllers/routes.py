from app import app
from flask import Flask, request, make_response, redirect, jsonify
from app.functions import custom_render_template as render_template, empty, get_html_main_pages
from app.controllers import register_login


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/loginSubmit", methods=['POST'])
def loginSubmit():
    return register_login.login(request.form['email'], request.form['password'])


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
@app.route("/emailInput")
@app.route("/emailInput", methods=['POST'])
def emailInput():
    if request.method == 'POST':
        return render_template("input-email.html", title="Corrija seu E-mail", styles=['/login/login.css'],
                               oldEmail=request.form['email'])
    else:
        return render_template("input-email.html", title="Digite seu E-mail", styles=['/login/login.css'])


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
    return render_template("main/index.html")

@app.route("/getHTML")
def teste():
    return get_html_main_pages()
