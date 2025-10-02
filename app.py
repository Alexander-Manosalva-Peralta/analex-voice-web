from flask import Flask, render_template, request, jsonify, url_for
from datetime import datetime
import unicodedata

app = Flask(__name__)

# Fondos disponibles
fondos = {
    "paris": "assets/paris.mp4",
    "fogata": "assets/fogata.mp4",
    "monte everest": "assets/Monte Everest.mp4",
    "fondo monte everest": "assets/Everest.mp4",
    "playa": "assets/playa.jpg",
    "costa verde lima": "assets/Costa Verde Lima.mp4",
    "atardecer": "assets/Atardecer.mp4",
}

# Canciones
canciones = {
    "cancion monte everest": "assets/Monte Everest.mp3",
    "control": "assets/control.mp3",
    "control de jammal sanchez": "assets/control.mp3",
    "la vida sin ti": "assets/La vida sin ti Rels B.mp3"
}

preguntas_tiempo = {
    "hora": "hora",
    "que hora es": "hora",
    "dime la hora": "hora",
    "dia": "dia",
    "que dia es": "dia",
    "dime el dia": "dia",
    "hoy que dia es": "dia"
}

def normalizar(texto):
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')
    return texto

def hora_a_palabras():
    ahora = datetime.now()
    return f"Claro, son las {ahora.hour}:{ahora.minute}:{ahora.second}."

def dia_a_palabras():
    ahora = datetime.now()
    return f"Hoy es {ahora.strftime('%A, %d de %B de %Y')}."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()
    texto = normalizar(data.get("texto", ""))

    respuesta = "No entendí lo que pediste."
    acciones = {}

    # Preguntas de hora/día
    for clave, tipo in preguntas_tiempo.items():
        if clave in texto:
            if tipo == "hora":
                respuesta = hora_a_palabras()
                return jsonify({"respuesta": respuesta})
            elif tipo == "dia":
                respuesta = dia_a_palabras()
                return jsonify({"respuesta": respuesta})

    # Pausar o detener música
    if "pausa la musica" in texto or "pausa la cancion" in texto:
        acciones["musica"] = {"accion": "pause"}
        respuesta = "He pausado la música."
        return jsonify({"respuesta": respuesta, **acciones})
    if "apaga la musica" in texto or "deten la musica" in texto or "quita la cancion" in texto:
        acciones["musica"] = {"accion": "stop"}
        respuesta = "He apagado la música."
        return jsonify({"respuesta": respuesta, **acciones})

    # Determinar si busca fondo o canción
    es_fondo = "fondo" in texto or "pantalla" in texto or "imagen" in texto or "video" in texto
    es_cancion = "cancion" in texto or "musica" in texto or "canción" in texto

    # Fondos
    if es_fondo:
        for nombre, ruta in fondos.items():
            if nombre in texto:
                tipo = "video" if ruta.endswith((".mp4", ".webm")) else "imagen"
                acciones["fondo"] = {"tipo": tipo, "src": url_for('static', filename=ruta)}
                respuesta = f"Mostrando el fondo de {nombre}."
                return jsonify({"respuesta": respuesta, **acciones})
        respuesta = "No encontré ese fondo."
        return jsonify({"respuesta": respuesta})

    # Canciones
    if es_cancion:
        for nombre, ruta in canciones.items():
            if nombre in texto:
                acciones["musica"] = {"accion": "play", "src": url_for('static', filename=ruta)}
                respuesta = f"Reproduciendo {nombre}."
                return jsonify({"respuesta": respuesta, **acciones})
        respuesta = "No encontré esa canción."
        return jsonify({"respuesta": respuesta})

    return jsonify({"respuesta": respuesta, **acciones})

if __name__ == "__main__":
    app.run(debug=True)
