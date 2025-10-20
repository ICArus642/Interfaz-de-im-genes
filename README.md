# Interfaz de imagenes
proyecto para editor de imagenes




# 🖼️ Procesador de Imágenes - Computación Gráfica

Este proyecto implementa una aplicación interactiva para **procesamiento digital de imágenes**, desarrollada en **Python** utilizando las librerías **Tkinter**, **Pillow (PIL)** y **NumPy**.  
Permite aplicar una amplia gama de transformaciones visuales y análisis sobre imágenes, incluyendo ajustes de brillo, contraste, rotación, fusión y más.

---

## 🚀 Características principales

La aplicación integra las siguientes funcionalidades dentro de una interfaz gráfica:

### 🔆 Ajustes de brillo y contraste
1. **Brillo global:** Aumenta o disminuye el brillo general de la imagen.  
2. **Brillo por canal (R, G, B):** Modifica individualmente la intensidad de cada canal de color.  
3. **Contraste logarítmico:** Mejora zonas oscuras usando una función logarítmica.  
4. **Contraste exponencial:** Resalta zonas claras mediante una función exponencial.

### ✂️ Transformaciones geométricas
5. **Recorte (crop):** Permite seleccionar un área específica de la imagen.  
6. **Zoom:** Amplía una región de interés manteniendo la proporción.  
7. **Rotación:** Gira la imagen con un ángulo libre elegido por el usuario.

### 📊 Análisis y visualización
8. **Histograma:** Muestra la distribución de intensidades de los píxeles para analizar brillo y contraste.

### 🧩 Fusión de imágenes
9. **Fusión de dos imágenes:** Combina dos imágenes seleccionadas con un factor de mezcla ajustable.  
10. **Fusión de imágenes ecualizadas:** Ecualiza ambas imágenes antes de mezclarlas para mejorar contraste y uniformidad.

### 🎨 Manipulación de color
11. **Extracción de capas RGB:** Separa la imagen en sus tres componentes rojo, verde y azul.  
12. **Extracción de capas CMYK:** Convierte la imagen y extrae las cuatro capas del modelo CMYK (Cian, Magenta, Amarillo, Negro).  
13. **Foto negativa:** Invierte los valores de color, generando el negativo fotográfico.  
14. **Conversión a escala de grises:** Convierte la imagen a un solo canal de luminancia.  
15. **Binarización:** Convierte la imagen en blanco y negro usando un umbral definido por el usuario.

---



---

## 🪟 Interfaz gráfica (Tkinter)

La interfaz permite:
- Abrir imágenes desde el explorador de archivos.
- Visualizar resultados antes y después del procesamiento.
- Ajustar parámetros (brillo, contraste, zoom, rotación, etc.) mediante sliders y botones.
- Guardar los resultados en formato `.png` o `.jpg`.

---

## ⚙️ Instalación

1. Clonar este repositorio:
   ```bash
   git clone https://github.com/tuusuario/procesador-imagenes.git
   cd procesador-imagenes

pip install -r requirements.txt

python main.py



