# Interfaz de imagenes
proyecto para editor de imagenes


# Proyecto de Procesamiento Digital de Imágenes 🧠📷

Este proyecto implementa una **interfaz gráfica en Python (Tkinter)** que permite aplicar distintas transformaciones y análisis a imágenes, utilizando una librería personalizada llamada **Libimg**.

Incluye operaciones de brillo, contraste, rotación, recorte interactivo, zoom, histograma, fusión, extracción de capas RGB/CMYK, negativo, escala de grises y binarización.

---

## 🚀 Requisitos

Asegúrate de tener instalado **Python 3.8 o superior**.

### 📦 Librerías necesarias

Instálalas ejecutando en tu terminal:

```bash
pip install pillow numpy matplotlib
```

📂 Proyecto_Procesamiento_Imagenes
│
├── Clase9.py              # Archivo principal (interfaz gráfica)
├── Libimg.py              # Librería personalizada de transformaciones
├── README.md              # Documento de descripción del proyecto
└── ejemplo.jpg            # Imagen de ejemplo (opcional)


python Clase9.py

## 🖱️ Uso de la Interfaz Gráfica

La aplicación está diseñada para ser intuitiva y fácil de usar.  
A continuación se describe la función de cada control disponible en la ventana principal:

---

### 🖼️ 1. Abrir imagen
- **Botón:** `Abrir imagen...`  
- Permite seleccionar una imagen desde tu equipo en formatos como `.jpg`, `.png`, `.bmp`, `.gif`, `.tiff`, etc.  
- La imagen se carga automáticamente y se muestra en el visor principal.

---

### 🌞 2. Control de brillo
- **Control:** Deslizador horizontal (slider)  
- Ajusta el brillo de la imagen en tiempo real.  
- Valores negativos oscurecen la imagen, positivos la aclaran.  
- Rango: `-1.0` a `1.0`

---

### 🎨 3. Canales RGB
- **Controles:** Tres casillas de verificación:  
  - `Rojo`  
  - `Verde`  
  - `Azul`  
- Permiten activar o desactivar los canales de color individualmente.  
- Al desmarcar un canal, este se elimina temporalmente de la visualización.  
- Si se desactivan todos, el programa advierte y restaura los tres canales.

---

### 🌈 4. Transformaciones de contraste
- **Botones:**
  - `Contraste logarítmico`  
  - `Contraste exponencial`
- Mejoran la visibilidad de detalles oscuros o brillantes aplicando funciones de realce de contraste.  
- El resultado se muestra inmediatamente.

---

### 🔄 5. Rotación de imagen
- **Botón:** `Rotar imagen`  
- Solicita un ángulo (en grados) e imprime la imagen rotada.  
- El ángulo puede ser positivo (rotación horaria) o negativo (antihoraria).

---

### 🔍 6. Zoom y recorte
- **Botón:** `Zoom`  
  Amplía una zona de la imagen definida por coordenadas o área preestablecida.  
- **Botón:** `Recorte interactivo`  
  Abre una ventana donde puedes **seleccionar con el mouse** el área que deseas conservar.  
  Al soltar el clic, la imagen se recorta automáticamente y se actualiza en pantalla.

---

### 📊 7. Histograma
- **Botón:** `Mostrar histograma`  
- Calcula y grafica la distribución de niveles de intensidad por canal (R, G, B o escala de grises).  
- Se muestra una ventana emergente con las curvas correspondientes.

---

### 🧩 8. Fusión de imágenes
- **Botón:** `Fusionar imágenes`  
  - Solicita una segunda imagen y combina ambas con un nivel de transparencia ajustable (`alpha`).  
- **Botón:** `Fusión ecualizada`  
  - Igual que la anterior, pero primero ecualiza los histogramas de ambas imágenes antes de fusionarlas.

---

### 💡 9. Operaciones básicas
- **Botones:**
  - `Negativo` → Invierte los colores.  
  - `Escala de grises` → Convierte la imagen a tonos de gris.  
  - `Binarizar` → Crea una imagen en blanco y negro a partir de un umbral fijo.

---

### 🧬 10. Extracción de capas
- **Botones:**
  - `Extraer RGB` → Muestra las capas Roja, Verde y Azul como imágenes separadas.  
  - `Extraer CMYK` → Genera las capas Cian, Magenta, Amarillo y Negro (modo de impresión).

---

### 🔚 11. Cierre
- Para cerrar la aplicación, simplemente cierra la ventana principal o presiona `Alt + F4`.

---

## 🎯 Consejos de uso

- Todas las transformaciones aplican directamente sobre la imagen cargada.  
- Si deseas recuperar

## 🧠 Tecnologías utilizadas

- Python 3.9+
- Tkinter – Interfaz gráfica.
- NumPy – Manipulación de matrices e imágenes.
- Pillow (PIL) – Carga y visualización (solo cuando se usa).
- Matplotlib – Gráficas de histograma.

👨‍💻 Autor

Jonathan Muñoz Jimenez — Computación Gráfica (2025)
Universidad Tecnologica de Pereira
Repositorio académico para prácticas de procesamiento digital de imágenes.

