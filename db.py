import mysql.connector
from mysql.connector import Error
from flask import flash, redirect, url_for
import config as c

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
        return redirect(url_for('registro'))
