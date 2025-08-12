# Google Feud Español

Un juego estilo Google Feud en español donde los jugadores adivinan las respuestas más populares a preguntas de búsqueda de Google.

## 🎮 Cómo jugar

1. Selecciona una categoría para la primera ronda
2. Lee la pregunta mostrada
3. Escribe tu respuesta en el campo de texto
4. Tienes 4 intentos por ronda
5. Hay 10 rondas por juego
6. **Después de cada ronda, selecciona una nueva categoría**
7. Cada respuesta correcta te da puntos según su popularidad (10,000 - 1,000 puntos)
8. Las respuestas incorrectas muestran una ✗ roja en pantalla

## 📁 Estructura del proyecto

```
google-feud-espanol/
├── index.html           # Página principal del juego
├── styles.css           # Estilos CSS (estilo Google)
├── script.js            # Lógica del juego en JavaScript
├── generate_game_data.py # Script para generar datos del juego automáticamente
├── docker-compose.yml   # Configuración Docker
├── nginx.conf           # Configuración del servidor Nginx
├── data/                # Archivos JSON con preguntas y respuestas
│   ├── seed.json        # Consultas semilla para generar datos
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
```json
[
  {
    "question": "Your question here...?",
    "answers": [
      { "text": "most popular answer", "rank": 1 },
      { "text": "second most popular", "rank": 2 },
      { "text": "third most popular", "rank": 3 },
      // ... up to rank 10
      { "text": "least popular answer", "rank": 10 }
    ]
  }
]
```

### Reglas para las respuestas:
- Cada pregunta debe tener exactamente 10 respuestas
- Los ranks van de 1 (más popular) a 10 (menos popular)
- **Los puntos se calculan automáticamente**: Rank 1 = 10,000 puntos, Rank 10 = 1,000 puntos
- Las respuestas deben estar ordenadas por popularidad (rank 1 a 10)

## 🤖 Generación automática de datos

### Script `generate_game_data.py`

El proyecto incluye un script en Python que puede generar automáticamente preguntas y respuestas utilizando la API de autocompletado de Google. Este script:

- 📖 Lee consultas semilla desde `data/seed.json`
- 🔍 Obtiene sugerencias de autocompletado de Google para cada consulta
- 🎯 Genera preguntas de juego con respuestas ordenadas por popularidad
- 💾 Guarda los datos en los archivos JSON correspondientes de cada categoría

### Archivo `seed.json`

El archivo `data/seed.json` contiene las consultas base organizadas por categoría:

```json
{
  "cultura": [
    "por qué los españoles",
    "cómo es la cultura",
    "qué tradiciones tienen",
    ...
  ],
  "personas": [
    "por qué la gente",
    "cómo son las personas",
    ...
  ],
  ...
}
```

### Cómo usar el generador de datos

1. **Instalar dependencias de Python:**
   ```bash
   pip install requests
   ```

2. **Editar las consultas semilla:**
   - Modifica `data/seed.json` para agregar, quitar o cambiar consultas base
   - Cada consulta debe ser un fragmento de búsqueda en español

3. **Ejecutar el generador:**
   ```bash
   python generate_game_data.py
   ```

4. **El script automáticamente:**
   - Obtiene sugerencias de Google para cada consulta
   - Filtra y limpia las respuestas
   - Genera archivos JSON con formato compatible con el juego
   - Incluye limitación de velocidad para evitar bloqueos

### Características del generador:
- ✅ **Rate limiting inteligente**: Evita ser bloqueado por Google
- ✅ **Expansión alfabética**: Si no hay suficientes sugerencias, prueba con sufijos
- ✅ **Filtrado automático**: Limpia y filtra respuestas irrelevantes
- ✅ **Soporte multiidioma**: Configurado específicamente para español
- ✅ **Reintentos automáticos**: Maneja errores de red y límites de velocidad
- ✅ **Logging detallado**: Muestra el progreso de cada consulta

**Nota:** El uso de este script debe ser responsable y respetar los términos de servicio de Google. Se recomienda usar con moderación y espaciar las ejecuciones.

## 🚀 Cómo ejecutar el juego

### Usar Docker

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
- **Python 3**: Script de generación automática de datos
- **JSON**: Almacenamiento de datos

## 📝 Características

- ✅ Interfaz responsive (funciona en móviles y desktop)
- ✅ Diseño estilo Google Search** con colores y elementos familiares
- ✅ 7 categorías diferentes
- ✅ 3 rondas por juego
- ✅ 4 intentos por ronda (límite estricto)
- ✅ Feedback visual para respuestas incorrectas (✗ roja animada)
- ✅ Animaciones suaves
- ✅ Fácil edición de preguntas (archivos JSON con ranks)
- ✅ Búsqueda flexible (ignora acentos y mayúsculas)
- ✅ Docker setup con Nginx para fácil despliegue

## 🎯 Personalización

### Agregar nuevas categorías:
1. Agrega consultas semilla en `data/seed.json` para la nueva categoría
2. Ejecuta `python generate_game_data.py` para generar los datos automáticamente
3. Agrega el botón de categoría en `index.html`
4. Actualiza el array de categorías en `script.js`

### Actualizar preguntas existentes:
- **Opción 1 (Automática)**: Modifica las consultas en `data/seed.json` y ejecuta el script
- **Opción 2 (Manual)**: Edita directamente los archivos JSON en la carpeta `data/`

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
