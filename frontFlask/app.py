from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

FASTAPI_URL = os.getenv('FASTAPI_URL', 'http://localhost:5000')

@app.route('/')
def index():
    # Obtener lista de usuarios desde FastAPI para mostrarlos en la tabla
    try:
        response = requests.get(f"{FASTAPI_URL}/v1/usuarios/")
        response.raise_for_status()
        usuarios = response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        usuarios = []
        print(f"Error al obtener usuarios: {e}")
    return render_template('index.html', usuarios=usuarios)

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        # Obtener datos del formulario
        nuevo = {
            "id": int(request.form['id']),
            "nombre": request.form['nombre'],
            "edad": int(request.form['edad'])
        }
        try:
            response = requests.post(f"{FASTAPI_URL}/v1/usuarios/", json=nuevo)
            if response.status_code == 200:
                return redirect(url_for('index'))
            else:
                return f"Error al crear usuario: {response.text}", 400
        except requests.exceptions.RequestException as e:
            return f"Error de conexión: {e}", 500
    # GET: mostrar formulario
    return render_template('nuevo.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    if request.method == 'POST':
        # Datos actualizados
        actualizado = {
            "nombre": request.form['nombre'],
            "edad": int(request.form['edad'])
        }
        try:
            response = requests.put(f"{FASTAPI_URL}/v1/usuarios/{id}", json=actualizado)
            if response.status_code == 200:
                return redirect(url_for('index'))
            else:
                return f"Error al actualizar: {response.text}", 400
        except requests.exceptions.RequestException as e:
            return f"Error de conexión: {e}", 500
    # GET: obtener datos actuales del usuario para prellenar el formulario
    try:
        response = requests.get(f"{FASTAPI_URL}/v1/usuarios/")
        usuarios = response.json().get('data', [])
        usuario = next((u for u in usuarios if u['id'] == id), None)
        if not usuario:
            return "Usuario no encontrado", 404
    except requests.exceptions.RequestException as e:
        return f"Error al obtener usuario: {e}", 500
    return render_template('editar.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    try:
        response = requests.delete(f"{FASTAPI_URL}/v1/usuarios/{id}")
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return f"Error al eliminar: {response.text}", 400
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)