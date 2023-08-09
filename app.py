import requests, json
from flask import Flask, render_template, request, redirect
from datetime import date

app = Flask(__name__)
# URL de la API del Banco de México
BANXICO_API_URL = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno?token=194dd7b63978ba1884a5fda5187d2873f2c5523d0d8bc4400079ef6faf5cfa6a"
BANXICO_API_TOKEN = "194dd7b63978ba1884a5fda5187d2873f2c5523d0d8bc4400079ef6faf5cfa6a"


# Lista de artículos (simulación de una tabla en una base de datos)
articulos = [
    {
        "clave": 1,
        "descripcion_corta": "Artículo 1",
        "descripcion_larga": "Descripción del artículo 1",
        "unidad_medida": "Unidades",
        "costo": 10,
        "precio": 20,
        "tipo_cambio": None,
        "precio_dolares": None,

    
    },# Agregar más artículos aquí si es necesario
]

# Página principal que muestra la lista de artículos
@app.route("/")
def index():
    return render_template("index.html", articulos=articulos)

# Página para ver el detalle de un artículo seleccionado
@app.route("/detalle/<int:clave>")
def detalle(clave):
    articulo = next((item for item in articulos if item["clave"] == clave), None)
    if not articulo:
        return "Artículo no encontrado"
    return render_template("detalle.html", articulo=articulo)

def obtener_tipo_cambio():
    try:
        response = requests.get(BANXICO_API_URL)
        if response.status_code == 200:
            data = response.json()
            print(data)
            tipo_cambio = data['bmx']['series'][0]['datos'][0]["dato"]
            print(tipo_cambio)
            return float(tipo_cambio)
        else:
            print("La solicitud no fue exitosa. Código de estado:", response.status_code)
            
    except Exception as e:
        print("Error al obtener el tipo de cambio:", e)
    
def obtener_proxima_clave():
    if not articulos:
        return 1
    return max(articulo["clave"] for articulo in articulos) + 1
    
# Página para agregar un nuevo artículo
@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        # Obtener los datos del formulario
        descripcion_corta = request.form["descripcion_corta"]
        descripcion_larga = request.form["descripcion_larga"]
        unidad_medida = request.form["unidad_medida"]
        costo = float(request.form["costo"])
        precio = float(request.form["precio"])

        nueva_clave = obtener_proxima_clave()
        


        # Obtener el tipo de cambio del dólar
        tipo_cambio = obtener_tipo_cambio()

        if tipo_cambio is not None:
            # Calcular el precio en dólares
            precio_dolares = precio / tipo_cambio
        else:
            tipo_cambio = 0
            precio_dolares = 0

        # Asignar automáticamente la clave (llave autonumerada)
        nueva_clave = max(articulos, key=lambda x: x["clave"])["clave"] + 1

        # Crear un nuevo artículo
        nuevo_articulo = {
            "clave": nueva_clave,
            "descripcion_corta": descripcion_corta,
            "descripcion_larga": descripcion_larga,
            "unidad_medida": unidad_medida,
            "costo": costo,
            "precio": precio,
            "tipo_cambio": tipo_cambio,
            "precio_dolares": precio_dolares,
        }

        # Agregar el nuevo artículo a la lista
        articulos.append(nuevo_articulo)

        # Redireccionar a la página principal
        return redirect("/")
    return render_template("nuevo.html")

if __name__ == "__main__":
    app.run(debug=True)
