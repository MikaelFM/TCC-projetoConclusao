import os
from app import app
from flask import Flask, render_template, request, make_response, redirect, jsonify

def custom_render_template(page, **var):
    var = {
        'title': [],
        'scripts': [],
        'styles': []
    }
    static_folder = 'app/static'

    page_name = page.replace('.html', '')

    for static_type in var.keys():
        static_path = f"{static_folder}/{static_type}/{page_name}"
        if os.path.exists(static_path):
            files = os.listdir(static_path)
            var[static_type] = [f"{page_name}/{file}" for file in files]

    return render_template('page.html', page=page, **var)