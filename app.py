from flask import Flask,render_template,flash,redirect,session
import config as c
from auth import auth #importa el blueprint auth
from contactos import contactos # blueprint contactos
import db 

app = Flask(__name__)
app.secret_key = c.SECRET_KEY

#registrar los blueprint
app.register_blueprint(auth) 
app.register_blueprint(contactos) 


#Muestra los contactos del user, y desde aqui se puede ir a agregar o editar
@app.route('/dashboard')
def home():
    if 'usuario' in session and 'id' in session:
        id_user = session['id']
        conexion = db.conexion_db()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM contacto WHERE id_usuario=%s",(id_user,))
        resultado = cursor.fetchall()
        return render_template("dashboard.html",resultado=resultado)
    else:
        flash("Debes iniciar sesion para entrar al dashboard")
        return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
