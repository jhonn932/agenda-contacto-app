from flask import Flask,render_template,url_for,request,flash,redirect,session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def conexion_db():
    try:
        conexion = mysql.connector.connect(
            host=config.MYSQL_HOST,
            database=config.MYSQL_DATABASE,
            user=config.MYSQL_USER,
            password=config.MYSQL_PASSWORD
        )

        if conexion.is_connected():
            return conexion
        
    except Error as e:
        flash(f"Error al conectar las base de datos mySQL: {e}")
        return None


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if not username or not password:
            flash("Los campos son obligatiorios")
            return redirect(url_for('registro'))
        
        hashed_password = generate_password_hash(password)
        conexion = conexion_db()

        if conexion:
            cursor = conexion.cursor()
            cursor.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)',
                           (username, hashed_password))
            conexion.commit()
            conexion.close()
            flash("Te has registrado Exitosamente!!")
            return redirect(url_for('registro'))
        else:
            flash("Se ha producido un error al registrarte")
            return redirect(url_for('registro'))


    return render_template("registro.html")


@app.route('/login', methods=['GET', 'POST'])
def loguear():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        if not username or not password:
            flash('Usuario o contraseña invalidos')
            return redirect(url_for('loguear'))
        
        conexion = conexion_db()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT password FROM usuarios WHERE username= %s" ,(username,))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                has_guardado = resultado[0]
                if check_password_hash(has_guardado,password):
                    session['usuario'] = username
                    return redirect("/dashboard")
                else:
                    flash("La contraseña es incorrecta.")
            else: 
                flash("Nombre de usuario no encontrado.")
            return redirect(url_for('loguear'))
        
    return render_template("login.html")

@app.route('/dashboard')
def home():
    if 'usuario' in session:
        return render_template("dashboard.html")
    else:
        flash("Debes iniciar sesion para entrar al dashboard")
        return redirect('/login')
    
@app.route('/logout')
def logout():
    session.pop('usuario',None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
