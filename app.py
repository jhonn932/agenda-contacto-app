from flask import Flask,render_template,url_for,request,flash,redirect,session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import config as c

app = Flask(__name__)
app.secret_key = c.SECRET_KEY

def conexion_db():
    try:
        conexion = mysql.connector.connect(
            host=c.MYSQL_HOST,
            database=c.MYSQL_DATABASE,
            user=c.MYSQL_USER,
            password=c.MYSQL_PASSWORD
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
            cursor.execute("SELECT password, id FROM usuarios WHERE username= %s" ,(username,))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                has_guardado = resultado[0]
                if check_password_hash(has_guardado,password):
                    session['usuario'] = username
                    session['id'] = resultado[1]
                    return redirect("/dashboard")
                else:
                    flash("La contraseña es incorrecta.")
            else: 
                flash("Nombre de usuario no encontrado.")
            return redirect(url_for('loguear'))
        
    return render_template("login.html")


@app.route('/agendar', methods=['GET','POST'])
def agendar():
    if 'id' in session:
        if request.method == 'POST':
            nombre = request.form.get('nombre').strip()
            telefono = request.form.get('telefono').strip()
            correo = request.form.get('correo').strip()
            observacion = request.form.get('observacion').strip()

            errores = []
            #new validacion campo por campo
            if not nombre:
                errores.append("El nombre es Obligario!")
            if not telefono.isdigit() or len(telefono) < 10:
                errores.append("Numero de telefono invalido.")
            if not correo or '.' not in correo.split('@')[-1]:
                errores.append("La direccion de correo es invalida.")

            #mostrar errores si hay
            if errores:
                for error in errores:
                    flash(error)
                return redirect(url_for('agendar'))
            
            id_user = session['id']
            conexion = conexion_db()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO contacto (nombre, telefono, email, observaciones, id_usuario) VALUES (%s, %s, %s, %s, %s)",
                           (nombre, telefono, correo, observacion, id_user))
            conexion.commit()
            conexion.close()
            flash("Contacto agendado Exitosamente!! Wow")
            return redirect(url_for('agendar'))
        
        return render_template('agendar.html')
    
    flash("Debes iniciar sesion para agendar un contacto")
    return redirect(url_for('loguear'))


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
    session.pop('id',None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
