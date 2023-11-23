import os
from app import app
import random
from flask import Flask, render_template, request, make_response, redirect, jsonify
from sqlalchemy import ForeignKey, text
from app import db


def custom_render_template(page, **var):
    var.setdefault('title', '')
    var.setdefault('scripts', [])
    var.setdefault('styles', [])

    static_folder = 'app/static'
    page_name = page.replace('.html', '').replace('/index', '')

    for t in ['css', 'js']:
        static_path = f"{static_folder}/{t}/{page_name}"
        if os.path.exists(static_path):
            files = os.listdir(static_path)
            type = 'styles' if t == 'css' else 'scripts'
            var[type] += [f"{page_name}/{file}" for file in files]
    return render_template('page.html', page=page, **var)


from sqlalchemy import text

def execute(sql, params=None, session=None):
    with app.app_context():
        sql_query = text(sql)

        if session is None:
            session = db.session()

        try:
            if params:
                result = session.execute(sql_query, params)
            else:
                result = session.execute(sql_query)

            session.commit()

            if result.returns_rows:
                result_list = []
                columns = result.keys()

                for row in result:
                    row_dict = {}
                    for i, column in enumerate(columns):
                        row_dict[column] = row[i]
                    result_list.append(row_dict)

                return result_list
            else:
                return None
        except Exception as e:
            session.rollback()
            raise e


def empty(object):
    return object == [] or object is None or object == ''

def generate_token():
    token = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    return token

def get_html_from(path):
    base_url = "app/templates/"
    try:
        with open(base_url + path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            return html_content
    except FileNotFoundError:
        return "Arquivo não encontrado"
    except Exception as e:
        return f"Ocorreu um erro: {e}"

def get_html_main_pages():
    return {
        'agenda': get_html_from("main/agenda.html"),
        'arquivos': get_html_from("main/arquivos.html"),
        'configuracoes': get_html_from("main/configuracoes.html"),
        'home': get_html_from("main/home.html"),
        'registros': get_html_from("main/registros.html"),
        'servidores': get_html_from("main/servidores.html")
    }

def serialize_values(values):
    if values is None:
        return None
    serialized_user = {}
    for key, value in values.__dict__.items():
        if not key.startswith('_'):
            serialized_user[key] = value
    return serialized_user