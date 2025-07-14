from flask import render_template,url_for,request,flash,redirect,session,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import db

auth = Blueprint('auth',__name__)

#Registrar usuario
@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre').strip()
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if not nombre or not username or not password:
            flash("Los campos son obligatiorios")
            return redirect(url_for('auth.registro'))
        
        hashed_password = generate_password_hash(password)
        conexion = db.conexion_db()
        cursor = conexion.cursor()
        cursor.execute('INSERT INTO usuarios (username, password, nombre) VALUES (%s, %s, %s)',
                       (username, hashed_password, nombre))
        conexion.commit()
        conexion.close()
        flash("Te has registrado Exitosamente!!")
        return redirect(url_for('auth.registro'))

    return render_template("auth/registro.html")


#Loguear usuario
@auth.route('/login', methods=['GET', 'POST'])
def loguear():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if not username or not password:
            flash('Usuario o contraseña invalidos')
            return redirect(url_for('auth.loguear'))
        
        conexion = db.conexion_db()

        cursor = conexion.cursor()
        cursor.execute("SELECT password, id, nombre FROM usuarios WHERE username= %s" ,(username,))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            has_guardado = resultado[0]
            if check_password_hash(has_guardado,password):
                session['usuario'] = username
                session['id'] = resultado[1]
                session['nombre'] = resultado[2]
                return redirect("/dashboard")
            else:
                flash("La contraseña es incorrecta.")
        else: 
            flash("Nombre de usuario no encontrado.")
            return redirect(url_for('auth.loguear'))
        
    return render_template("auth/login.html")


#cerrar session activa
@auth.route('/logout')
def logout():
    session.pop('usuario',None)
    session.pop('id',None)
    session.pop('nombre',None)
    flash("Saliste de tu cuenta.")
    return redirect('/login')