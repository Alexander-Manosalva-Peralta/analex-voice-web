// main.js — controla reconocimiento de voz, TTS y media
// Requiere que el usuario diga 'analex' para ejecutar (evita acciones no deseadas)
if(!text.includes('analex')){
status.textContent = 'No se detectó la palabra "Analex". Di "Analex, ..." para dar un comando.';
return;
}


// Quitar la palabra 'analex' para facilitar matching
const cleaned = text.replace('analex', '').trim();


// COMANDOS: fondo (imagen)
if(cleaned.includes('fondo') && !cleaned.includes('video')){
// buscamos una clave de background que aparezca en la frase
for(const key of Object.keys(assets.backgrounds)){
if(cleaned.includes(key)){
setBackgroundImage(assets.backgrounds[key]);
speak('Listo, poniendo fondo ' + key);
status.textContent = 'Fondo: ' + key;
return;
}
}
speak('No encontré ese fondo. Fondos disponibles: ' + Object.keys(assets.backgrounds).join(', '));
return;
}


// COMANDO: fondo en video
if(cleaned.includes('video') || cleaned.includes('fondo video') || cleaned.includes('video de')){
for(const key of Object.keys(assets.videos)){
if(cleaned.includes(key)){
setBackgroundVideo(assets.videos[key]);
speak('Poniendo video de fondo ' + key);
status.textContent = 'Video fondo: ' + key;
return;
}
}
speak('No encontré ese video. Videos disponibles: ' + Object.keys(assets.videos).join(', '));
return;
}


// COMANDO: reproducir música
if(cleaned.includes('reproduc') || cleaned.includes('toca') || cleaned.includes('reproduce') || cleaned.includes('pon musica') || cleaned.includes('cancion') || cleaned.includes('canción') || cleaned.includes('musica')){
for(const key of Object.keys(assets.songs)){
if(cleaned.includes(key)){
playSong(assets.songs[key]);
speak('Reproduciendo ' + key);
status.textContent = 'Reproduciendo: ' + key;
return;
}
}
// si no especifica canción, tocar primera
const firstKey = Object.keys(assets.songs)[0];
if(firstKey){ playSong(assets.songs[firstKey]); speak('Reproduciendo ' + firstKey); status.textContent = 'Reproduciendo: ' + firstKey; return; }
speak('No encontré canciones disponibles.');
return;
}


// COMANDO: detener
if(cleaned.includes('deten') || cleaned.includes('para') || cleaned.includes('pausa') || cleaned.includes('stop')){
stopMedia();
speak('Detenido');
status.textContent = 'Detenido';
return;
}


// Si no coincide nada
speak('No entendí el comando. Puedo: cambiar fondo, poner video de fondo o reproducir música. Ejemplo: "Analex, pon un fondo de Paris"');
status.textContent = 'Comando no reconocido';
}


// ---------------- RECONOCIMIENTO DE VOZ (Web Speech API) ----------------
let recognition;
if('webkitSpeechRecognition' in window || 'SpeechRecognition' in window){
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
recognition = new SR();
recognition.lang = 'es-PE'; // ajusta según prefieras
recognition.interimResults = false;
recognition.maxAlternatives = 1;


recognition.onstart = () => { status.textContent = 'Escuchando...'; };
recognition.onresult = (event) => {
const text = event
// Hacer que Analex hable en voz alta
const voz = new SpeechSynthesisUtterance(data.respuesta);
voz.lang = "es-ES"; // idioma español
voz.pitch = 1;      // tono (0.5 más grave, 2 más agudo)
voz.rate = 1;       // velocidad (1 = normal)
voz.volume = 1;     // volumen (0 a 1)

// Opcional: elegir voz disponible (depende del navegador)
const voces = window.speechSynthesis.getVoices();
if (voces.length > 0) {
    voz.voice = voces.find(v => v.lang === "es-ES") || voces[0];
}

window.speechSynthesis.speak(voz);
