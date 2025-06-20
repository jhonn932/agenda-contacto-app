from flask import Flask,render_template,url_for,request,flash,redirect,session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route('/')
def registro():
    return render_template("registro.html")


if __name__ == '__main__':
    app.run(debug=True)
