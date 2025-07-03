# Agenda de contactos con Flask

Aplicacion web para registrar, ver, editar y eliminar contactos. Incluye autenticacion de usuarios.

## Caracteristicas

- Registro de inicio de sesion
- Gestion de contactos
- Base de datos MySQL
- Contraseña cifradas
- Proyecto modularizado con BLueprints

## Tecnologias

- Python 3
- Flask
- MySQL
- HTML/CSS

## Instalacion

1. Clonar el repositorio
2. Crear y activar un entorno virtual (venv)
	- python3 -m venv venv
	- source venv/bin/activate (para activar el entorno o deactivate)
3. Instalar dependencias con (esto dentro del entorno virtual activado):
	- pip install flask
	- pip freeze > requirements.txt
	- pip install -r requirements.txt
	- pip install mysql-connector-python (para trabajar con mysql)
4. Configurar la Base de Datos
5. Ejecutar con 'python3 app.py'

## Base de Datos

Crear una base de datos 'myapp' con el user 'flaskuser' y el pass 'abc123' y ejecutar las siguientes sentencias SQL para crear las tablas:

```sql

CREATE DATABASE myapp;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(255)
);

CREATE TABLE contacto (
    id_contacto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    telefono VARCHAR(50),
    email VARCHAR(100),
    observaciones VARCHAR(200),
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);


## Estructura del proyecto

agenda-contacto-app/
├── app.py
├── db.py
├── auth/
│   ├── __init__.py
│   └── routes.py
├── contactos/
│   ├── __init__.py
│   └── routes.py
├── templates/
│   ├── auth/
│   │   ├── login.html
│   │   └── registro.html
│   ├── contactos/
│   │   ├── agendar.html
│   │   └── editar.html
│   └── dashboard.html
├── static/
│   ├── styles.css
│   └── stylesDash.css
└── README.md

## Autor

Proyecto desarrollado por Jonatan Ayala como parte de aprendizaje Fullstack.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.



