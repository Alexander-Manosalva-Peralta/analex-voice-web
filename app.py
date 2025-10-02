from flask import Flask, render_template, request, jsonify, url_for
from datetime import datetime
import unicodedata
import random
import pytz  # Importamos pytz para manejar zonas horarias

app = Flask(__name__)

# --- Zona horaria Lima ---
tz_lima = pytz.timezone("America/Lima")

# --- Traducción manual de días y meses ---
dias = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}

meses = {
    "January": "enero",
    "February": "febrero",
    "March": "marzo",
    "April": "abril",
    "May": "mayo",
    "June": "junio",
    "July": "julio",
    "August": "agosto",
    "September": "septiembre",
    "October": "octubre",
    "November": "noviembre",
    "December": "diciembre"
}

# --- Función para obtener fecha en español ---
def fecha_en_espanol():
    hoy = datetime.now(tz_lima)
    dia = dias[hoy.strftime("%A")]
    mes = meses[hoy.strftime("%B")]
    return dia, hoy.strftime("%d"), mes, hoy.strftime("%Y")

# --- Fondos disponibles ---
fondos = {
    "paris": "assets/paris.mp4",
    "fogata": "assets/fogata.mp4",
    "monte everest": "assets/Monte Everest.mp4",
    "fondo de monte everest": "assets/Everest.mp4",
    "playa": "assets/Playa.mp4",
    "costa verde lima": "assets/Costa Verde Lima.mp4",
    "atardecer": "assets/Atardecer.mp4",
    "lobo": "assets/lobo.mp4",
    "condor": "assets/condor_andino.jpg",
    "delfin": "assets/Delfin.mp4",
    "pizza": "assets/pizza.mp4",
    "causa": "assets/causa_limeña.jpg",
    "lomo": "assets/lomo_saltado.png"
}

# --- Canciones ---
canciones = {
    "cancion monte everest": "assets/Monte Everest.mp3",
    "control": "assets/Control.mp3",
    "control de jammal sanchez": "assets/Control.mp3",
    "la vida sin ti": "assets/La vida sin ti Rels B.mp3",
    "apocalypse": "assets/Apocalypse - Cigarettes After Sex.mp3",
    "apocalipse": "assets/Apocalypse - Cigarettes After Sex.mp3",
    "te regalo": "assets/Te Regalo - Rels B.mp3",
    "la chata": "assets/La Chata - Amen.mp3",
    "mujer amante": "assets/Mujer Amante - Rata Blanca.mp3",
    "hazme olvidarla": "assets/Hazme Olvidarla - Willie Gonzalez.mp3",
    "luna": "assets/Luna - Zoe.mp3",
    "yellow": "assets/Yellow - Coldplay.mp3",
    "la tormenta de arena": "assets/La Tormenta de Arena - Dorian.mp3"
}

# --- Función para normalizar texto ---
def normalizar(texto):
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')
    return texto

# --- Respuestas dinámicas ---
respuestas_hora = [
    "Son exactamente las {hora}:{minuto}.",
    "En este momento son las {hora}:{minuto}.",
    "Déjame ver… ahora son las {hora}:{minuto}.",
    "Claro, la hora actual es {hora}:{minuto}."
]

respuestas_dia = [
    "Hoy es {dia}, {num} de {mes} de {anio}.",
    "Estamos a {dia}, {num} de {mes}.",
    "Déjame confirmarlo… sí, hoy es {dia}, {num} de {mes} de {anio}."
]

respuestas_quien_eres = [
    "Soy Analex, un asistente virtual creado para conversar contigo y transformar la experiencia en pantalla.",
    "Me llamo Analex, un asistente retro-futurista que responde a tus preguntas y cambia fondos, música y más.",
    "Soy Analex, un asistente diseñado para interactuar contigo: puedo mostrarte paisajes, reproducir música y decirte la hora o el día.",
    "Puedes llamarme Analex. Estoy aquí para acompañarte con fondos, canciones y respuestas a lo que necesites."
]

respuestas_quien_te_creo = [
    "Fui creado por Yojan Alexander Manosalva Peralta como un proyecto innovador de asistente virtual.",
    "Mi creador es Yojan Alexander Manosalva Peralta, quien me programó para transformar la pantalla y reproducir música.",
    "Yo nací gracias al trabajo de Yojan Alexander Manosalva Peralta, quien me desarrolló como asistente retro-futurista.",
    "Mi creador es Yojan Alexander Manosalva Peralta. Él me dio la capacidad de hablar, cambiar fondos, reproducir canciones y responder preguntas."
]

respuestas_que_puedes_hacer = [
    "Puedo mostrar fondos, reproducir música, decirte la hora, el día y mucho más.",
    "Soy capaz de responder a tus preguntas, cambiar el ambiente y hasta poner música.",
    "Mi misión es entretenerte e informarte, cambiando fondos y canciones cuando lo pidas.",
    "Puedo conversar contigo, transformar la pantalla y darte información útil."
]

respuestas_saludos = [
    "¡Hola! Qué bueno verte aquí.",
    "Estoy muy bien, gracias por preguntar. ¿Y tú?",
    "¡Hey! Siempre listo para conversar contigo.",
    "¡Hola! Me alegra que estés aquí conmigo."
]

respuestas_despedida = [
    "Hasta pronto, fue un gusto hablar contigo.",
    "¡Nos vemos! Recuerda que siempre estaré aquí para ti.",
    "Adiós, cuídate mucho.",
    "Hasta la próxima, estaré esperándote."
]

respuestas_curiosidades = [
    "¿Sabías que el Monte Everest mide 8,849 metros de altura?",
    "Un dato curioso: el corazón humano late unas 100 mil veces al día.",
    "La Vía Láctea tiene más de 100 mil millones de estrellas.",
    "Los delfines se llaman entre sí por sus propios nombres con silbidos."
]

respuestas_color = [
    "Me gustan los colores oscuros, como el negro retro-futurista.",
    "El rojo intenso, porque me recuerda a la energía.",
    "Creo que el azul sería un buen color para mí, tranquilo pero profundo."
]

respuestas_comida = [
    "No puedo comer, pero si pudiera probar, elegiría pizza, ¡suena genial!",
    "Creo que disfrutaría mucho una causa limeña.",
    "Probablemente me encantaría un buen lomo saltado."
]

respuestas_animal = [
    "Me gustan los lobos, son libres y poderosos.",
    "Creo que sería el cóndor, porque vuela alto como mis ideas.",
    "Los delfines, porque son inteligentes y sociales."
]

# --- Rutas ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()
    texto = normalizar(data.get("texto", ""))
    respuesta = "No entendí lo que pediste."
    acciones = {}

    # Preguntar hora
    if "hora" in texto:
        ahora = datetime.now(tz_lima)
        hora = ahora.strftime("%H")
        minuto = ahora.strftime("%M")
        respuesta = random.choice(respuestas_hora).format(hora=hora, minuto=minuto)
        return jsonify({"respuesta": respuesta})

    # Preguntar día
    if "dia" in texto or "fecha" in texto:
        dia, num, mes, anio = fecha_en_espanol()
        respuesta = random.choice(respuestas_dia).format(dia=dia, num=num, mes=mes, anio=anio)
        return jsonify({"respuesta": respuesta})

    # Quién eres
    if "quien eres" in texto or "como te llamas" in texto:
        respuesta = random.choice(respuestas_quien_eres)
        return jsonify({"respuesta": respuesta})

    # Quién te creó
    if "quien te creo" in texto or "creador" in texto:
        respuesta = random.choice(respuestas_quien_te_creo)
        return jsonify({"respuesta": respuesta})

    # Qué puedes hacer
    if "que puedes hacer" in texto or "para que sirves" in texto:
        respuesta = random.choice(respuestas_que_puedes_hacer)
        return jsonify({"respuesta": respuesta})

    # Saludos
    if "hola" in texto or "como estas" in texto:
        respuesta = random.choice(respuestas_saludos)
        return jsonify({"respuesta": respuesta})

    # Despedidas
    if "adios" in texto or "chao" in texto or "hasta luego" in texto:
        respuesta = random.choice(respuestas_despedida)
        return jsonify({"respuesta": respuesta})

    # Curiosidades
    if "dato curioso" in texto or "cuentame algo" in texto:
        respuesta = random.choice(respuestas_curiosidades)
        return jsonify({"respuesta": respuesta})

    # Color favorito
    if "color favorito" in texto:
        respuesta = random.choice(respuestas_color)
        return jsonify({"respuesta": respuesta})

    # Animal favorito
    if "animal favorito" in texto:
        respuesta = random.choice(respuestas_animal)
        if "lobo" in respuesta.lower():
            acciones["fondo"] = {"tipo": "video", "src": url_for('static', filename=fondos["lobo"])}
        elif "condor" in respuesta.lower():
            acciones["fondo"] = {"tipo": "video", "src": url_for('static', filename=fondos["condor"])}
        elif "delfin" in respuesta.lower():
            acciones["fondo"] = {"tipo": "video", "src": url_for('static', filename=fondos["delfin"])}
        return jsonify({"respuesta": respuesta, **acciones})

    # Comida favorita
    if "comida favorita" in texto:
        respuesta = random.choice(respuestas_comida)
        if "pizza" in respuesta.lower():
            acciones["fondo"] = {"tipo": "video", "src": url_for('static', filename=fondos["pizza"])}
        elif "causa" in respuesta.lower():
            acciones["fondo"] = {"tipo": "imagen", "src": url_for('static', filename=fondos["causa"])}
        elif "lomo" in respuesta.lower():
            acciones["fondo"] = {"tipo": "imagen", "src": url_for('static', filename=fondos["lomo"])}
        return jsonify({"respuesta": respuesta, **acciones})

    # Pausar música
    if "pausa la musica" in texto or "pausa la cancion" in texto:
        acciones["musica"] = {"accion": "pause"}
        respuesta = "He pausado la música."
        return jsonify({"respuesta": respuesta, **acciones})

    # Detener música
    if "apaga la musica" in texto or "deten la musica" in texto or "quita la cancion" in texto:
        acciones["musica"] = {"accion": "stop"}
        respuesta = "He apagado la música."
        return jsonify({"respuesta": respuesta, **acciones})

    # Fondos
    if "fondo" in texto or "pantalla" in texto or "imagen" in texto or "video" in texto:
        for nombre, ruta in fondos.items():
            if nombre in texto:
                tipo = "video" if ruta.endswith((".mp4", ".webm")) else "imagen"
                acciones["fondo"] = {"tipo": tipo, "src": url_for('static', filename=ruta)}
                respuesta = f"Mostrando el fondo de {nombre}."
                return jsonify({"respuesta": respuesta, **acciones})
        respuesta = "No encontré ese fondo."
        return jsonify({"respuesta": respuesta})

    # Canciones
    if "cancion" in texto or "musica" in texto or "canción" in texto:
        for nombre, ruta in canciones.items():
            if nombre in texto:
                acciones["musica"] = {"accion": "play", "src": url_for('static', filename=ruta)}
                respuesta = f"Reproduciendo {nombre}."
                return jsonify({"respuesta": respuesta, **acciones})
        respuesta = "No encontré esa canción."
        return jsonify({"respuesta": respuesta})

    return jsonify({"respuesta": respuesta, **acciones})

# --- Solo para pruebas locales ---
if __name__ == "__main__":
    app.run(debug=True)
