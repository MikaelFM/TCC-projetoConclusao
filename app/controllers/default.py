from app import app
from flask import Flask, render_template, request, make_response, redirect, jsonify

@app.route("/")
def index():
    return render_template("index.html")