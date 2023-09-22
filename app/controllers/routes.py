from app import app
from flask import Flask, request, make_response, redirect, jsonify
from app.functions import custom_render_template as render_template 

@app.route("/")
def index():
    return render_template("content.html", title="oie")
