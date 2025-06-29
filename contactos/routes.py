from flask import render_template,url_for,request,flash,redirect,session,Blueprint
import db

contactos = Blueprint('contactos',__name__)

#agendar contactos
@contactos.route('/agendar', methods=['GET','POST'])
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
                return redirect(url_for('contactos.agendar'))
            
            id_user = session['id']
            conexion = db.conexion_db()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO contacto (nombre, telefono, email, observaciones, id_usuario) VALUES (%s, %s, %s, %s, %s)",
                           (nombre, telefono, correo, observacion, id_user))
            conexion.commit()
            conexion.close()
            flash("Contacto agendado Exitosamente!! Wow")
            return redirect(url_for('agendar'))
        
        return render_template('contactos/agendar.html')
    
    flash("Debes iniciar sesion para agendar un contacto.")
    return redirect(url_for('auth.loguear'))


#muestra los datos del contacto seleccionado para editarlo
@contactos.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    if 'usuario' in session and 'id' in session:
        conexion = db.conexion_db()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute('SELECT * FROM contacto WHERE id_contacto=%s',(id,))
        contacto = cursor.fetchall()
        conexion.close()

        return render_template('contactos/editar.html',contacto=contacto[0],id=id)
    else:
        flash("Debes iniciar sesion para editar contactos.")
        redirect(url_for('auth.loguear'))


#agregar func para guardar los cambios de la edicion
@contactos.route('/guardar_cambios/<int:id>', methods=['POST'])
def guardar_cambios(id):
    flash("Todavia no esta lista esta Funcionalidad.")
    return redirect(url_for('contactos.editar', id=id))