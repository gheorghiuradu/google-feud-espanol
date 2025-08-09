# Google Feud Español

Un juego estilo Google Feud en español donde los jugadores adivinan las respuestas más populares a preguntas de búsqueda de Google.

## 🎮 Cómo jugar

1. Selecciona una categoría
2. Lee la pregunta mostrada
3. Escribe tu respuesta en el campo de texto
4. Tienes 4 intentos por ronda
5. Hay 10 rondas por juego
6. Cada respuesta correcta te da puntos (de 100 a 1000 puntos)

## 📁 Estructura del proyecto

```
google-feud-espanol/
├── index.html          # Página principal del juego
├── styles.css          # Estilos CSS (estilo Google)
├── script.js           # Lógica del juego en JavaScript
├── docker-compose.yml  # Configuración Docker
├── nginx.conf          # Configuración del servidor Nginx
├── data/               # Archivos JSON con preguntas y respuestas
│   ├── cultura.json
│   ├── personas.json
│   ├── nombres.json
│   ├── preguntas.json
│   ├── animales.json
│   ├── entretenimiento.json
│   └── comida.json
└── README.md
```

## 🗂️ Categorías disponibles

- **Cultura**: Preguntas sobre tradiciones, países y costumbres
- **Personas**: Preguntas sobre comportamientos y características de las personas
- **Nombres**: Preguntas sobre nombres populares y apellidos
- **Preguntas**: Meta-preguntas sobre qué pregunta la gente
- **Animales**: Preguntas sobre animales y mascotas
- **Entretenimiento**: Preguntas sobre música, películas, series y redes sociales
- **Comida**: Preguntas sobre gastronomía y alimentación

## ✏️ Cómo editar preguntas y respuestas

Cada categoría tiene su propio archivo JSON en la carpeta `data/`. El formato es:

```json
[
  {
    "question": "¿Tu pregunta aquí...?",
    "answers": [
      { "text": "respuesta 1", "points": 1000 },
      { "text": "respuesta 2", "points": 900 },
      { "text": "respuesta 3", "points": 800 },
      { "text": "respuesta 4", "points": 700 },
      { "text": "respuesta 5", "points": 600 },
      { "text": "respuesta 6", "points": 500 },
      { "text": "respuesta 7", "points": 400 },
      { "text": "respuesta 8", "points": 300 },
      { "text": "respuesta 9", "points": 200 },
      { "text": "respuesta 10", "points": 100 }
    ]
  }
]
```

### Reglas para las respuestas:
- Cada pregunta debe tener exactamente 10 respuestas
- Los puntos van de 1000 (más popular) a 100 (menos popular)
- Las respuestas deben estar ordenadas por popularidad (mayor a menor puntuación)

## 🚀 Cómo ejecutar el juego

### Opción 1: Usar Docker (Recomendado)

1. Clona o descarga este repositorio
2. Asegúrate de tener Docker y Docker Compose instalados
3. Ejecuta el siguiente comando en la raíz del proyecto:

```bash
docker-compose up -d
```

4. Abre tu navegador y ve a `http://localhost:8080`
5. ¡Empieza a jugar!

Para detener el servidor:
```bash
docker-compose down
```

### Opción 2: Servidor local

1. Clona o descarga este repositorio
2. Abre `index.html` en un navegador web moderno
3. ¡Empieza a jugar!

### Requisitos:
- **Para Docker**: Docker y Docker Compose
- **Para servidor local**: Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexión a Internet (para cargar jQuery desde CDN)

## 🛠️ Tecnologías utilizadas

- **HTML5**: Estructura de la página
- **CSS3**: Estilos y animaciones
- **JavaScript ES6**: Lógica del juego
- **jQuery**: Manipulación del DOM y eventos
- **JSON**: Almacenamiento de datos

## 📝 Características

- ✅ Interfaz responsive (funciona en móviles y desktop)
- ✅ **Diseño estilo Google Search** con colores y elementos familiares
- ✅ 7 categorías diferentes
- ✅ 10 rondas por juego
- ✅ 4 intentos por ronda (límite estricto)
- ✅ Sistema de puntuación
- ✅ Animaciones suaves
- ✅ Fácil edición de preguntas (archivos JSON)
- ✅ Búsqueda flexible (ignora acentos y mayúsculas)
- ✅ **Docker setup con Nginx** para fácil despliegue
- ✅ **Configuración de servidor optimizada** con compresión y caché

## 🎯 Personalización

### Agregar nuevas categorías:
1. Crea un nuevo archivo JSON en la carpeta `data/`
2. Agrega el botón de categoría en `index.html`
3. Actualiza el array de categorías en `script.js`

### Cambiar el número de rondas:
Modifica la variable en `script.js` donde dice `this.currentRound <= 10`

### Cambiar el número de intentos:
Modifica `this.guessesLeft = 4` en `script.js`

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Puedes:
- Agregar más preguntas a las categorías existentes
- Crear nuevas categorías
- Mejorar el diseño
- Agregar nuevas características
- Reportar bugs

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🎉 ¡Diviértete jugando!

Esperamos que disfrutes este juego de Google Feud en español. ¡Comparte tu puntuación más alta con tus amigos!
