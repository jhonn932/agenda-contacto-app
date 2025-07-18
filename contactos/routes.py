from flask import render_template,url_for,request,flash,redirect,session,Blueprint
import db

contactos = Blueprint('contactos',__name__)

#funcion reutilizable para recibir datos de input y validarlos
def campos(n,t,c,o):
    input_campos = {
        'nombre' : request.form.get(n).strip(),
        'telefono' : request.form.get(t).strip(),
        'correo' : request.form.get(c).strip(),
        'obs' : request.form.get(o).strip()
    }

    errores = []
    #new validacion campo por campo
    if not input_campos['nombre'] :
        errores.append("El nombre es Obligario!")
    if not input_campos['telefono'].isdigit() or len(input_campos['telefono']) < 10:
        errores.append("Numero de telefono invalido.")
    if not input_campos['correo'] or '.' not in input_campos['correo'].split('@')[-1]:
        errores.append("La direccion de correo es invalida.")

    if errores:
        for e in errores:
            flash(e)

    return input_campos,errores


#agendar contactos
@contactos.route('/agendar', methods=['GET','POST'])
def agendar():
    if 'id' in session:
        if request.method == 'POST':
            valor_c,err = campos('nombre','telefono','correo','observacion')
            
            if err:
                return redirect(url_for('contactos.agendar'))

            id_user = session['id']
            conexion = db.conexion_db()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO contacto (nombre, telefono, email, observaciones, id_usuario) VALUES (%s, %s, %s, %s, %s)",
                           (valor_c['nombre'], valor_c['telefono'], valor_c['correo'], valor_c['obs'], id_user))
            conexion.commit()
            conexion.close()
            flash("Contacto agendado Exitosamente!! Wow")
            return redirect(url_for('contactos.agendar'))
        
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


#func para guardar los cambios de la edicion
@contactos.route('/guardar_cambios/<int:id>', methods=['POST'])
def guardar_cambios(id):
    valor_c,err = campos('nombre','telefono','correo','observacion')

    if err:
        return redirect(url_for('contactos.editar',id=id))

    conexion = db.conexion_db()
    cursor = conexion.cursor()
    cursor.execute('UPDATE contacto SET nombre=%s, telefono=%s, email=%s, observaciones=%s WHERE id_contacto=%s',
                   (valor_c['nombre'],valor_c['telefono'],valor_c['correo'],valor_c['obs'],id))
    conexion.commit()
    conexion.close()
    flash("Cambios guardados exitosamente!!")
    return redirect(url_for('contactos.editar',id=id))


#func para eliminar un contacto
@contactos.route('/eliminar/<int:id>', methods=['GET'])
def eliminar(id):

    conexion = db.conexion_db()
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM contacto WHERE id_contacto=%s', (id,))
    conexion.commit()
    conexion.close()

    return redirect(url_for('home'))
    