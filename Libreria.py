import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import jonathanLib as tf
#Importar la libreria de transformaciones


def brillo(img, valor):
    img_cop = np.copy(img)
    img_cop = img_cop + valor * 255
    img_cop = np.clip(img_cop, 0, 255)
    return img_cop

# Variable global
imagen_actual = None

def aplicar_canales():
    global imagen_actual
    if imagen_actual is None:
        return
    if not (r_var.get() or g_var.get() or b_var.get()):
        messagebox.showwarning("Advertencia", "Debe seleccionar al menos un canal (Rojo, Verde o Azul).")
        r_var.set(True)
        g_var.set(True)
        b_var.set(True)
        mostrar_imagen(imagen_actual)
        return
    r=r_var.get()
    g=g_var.get()
    b=b_var.get()
    combined=tf.layer_prog(imagen_actual, r, g, b)
    img_combined = Image.fromarray(combined.astype(np.uint8))
    mostrar_imagen(img_combined)

def abrir_imagen():
    global imagen_actual
    ruta = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes","*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff"), ("Todos","*.*")]
    )
    if not ruta:
        return
    imagen_actual = Image.open(ruta).resize((400,300))
    mostrar_imagen(imagen_actual)

    
def mostrar_imagen(img):
    foto = ImageTk.PhotoImage(img)
    lbl.config(image=foto)
    lbl.image = foto

def aplicar_brillo_btn(valor):
    global imagen_actual
    r_var.set(True)
    g_var.set(True)
    b_var.set(True)
    if imagen_actual is None:
        return
    try:
        while True:
            valor = float(valor)  # lee el valor del Slider
            if not -1.0 <= valor <= 1.0:
                messagebox.showerror("Error", "Ingresa un número entre -1.0 y 1.0")
                return
            break
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido")
        return

    # Convertir PIL a numpy
    img_np = np.array(imagen_actual, dtype=np.float32)

    # Usar directamente la función de brillo
    img_np = brillo(img_np, valor)
    # Convertir numpy a PIL
    imagen_np = Image.fromarray(img_np.astype(np.uint8))
    mostrar_imagen(imagen_np)

def aplicar_contraste_log():
    global imagen_actual
    img_resultado = tf.contraste_log(imagen_actual, c=30)
    mostrar_imagen(img_resultado)

def aplicar_contraste_exp():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Debe abrir una imagen primero.")
        return
    img_resultado = tf.contraste_exponencial(imagen_actual, gamma=0.5)
    mostrar_imagen(img_resultado)
    

def aplicar_recorte_interactivo():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Primero abre una imagen.")
        return

    # Crear nueva ventana para recorte
    win = tk.Toplevel(root)
    win.title("Selecciona área de recorte")
    
    # Convertir imagen actual a formato Tk
    img_tk = ImageTk.PhotoImage(imagen_actual)
    canvas = tk.Canvas(win, width=img_tk.width(), height=img_tk.height(), cursor="cross")
    canvas.pack()
    canvas.create_image(0, 0, anchor="nw", image=img_tk)
    canvas.image = img_tk  # evitar recolección de basura

    # Variables para coordenadas
    rect = None
    start_x = start_y = 0

    def on_press(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_drag(event):
        nonlocal rect
        if rect:
            canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_release(event):
        global imagen_actual
        x1, y1, x2, y2 = start_x, start_y, event.x, event.y

        # Convertir a numpy y recortar
        arr = np.array(imagen_actual)
        y1, y2 = sorted([int(y1), int(y2)])
        x1, x2 = sorted([int(x1), int(x2)])
        recortada = arr[y1:y2, x1:x2]

        # Convertir a PIL para mostrar y guardar
        imagen_actual = Image.fromarray(recortada.astype(np.uint8))
        mostrar_imagen(imagen_actual)
        win.destroy()

    # Vincular eventos
    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)

    
    
def aplicar_zoom(valor):
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Debe abrir una imagen primero.")
        return

    factor = float(valor)
    zoom_img = tf.zoom_simple(imagen_actual, factor)
    mostrar_imagen(zoom_img)


def aplicar_rotacion(angulo):
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Debe abrir una imagen primero.")
        return
    
    try:
        angulo = float(angulo)
    except ValueError:
        messagebox.showerror("Error", "Ingresa un valor numérico para el ángulo.")
        return
    
    img_rot = tf.rotar(imagen_actual, angulo)
    mostrar_imagen(img_rot)


def mostrar_histograma():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Debe abrir una imagen primero.")
        return
    tf.histograma(imagen_actual, mostrar=True)



def aplicar_fusion():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Primero abre una imagen base.")
        return

    # Seleccionar segunda imagen
    ruta = filedialog.askopenfilename(title="Selecciona la segunda imagen")
    if not ruta:
        return

    img2 = Image.open(ruta).resize(imagen_actual.size)

    # Pedir alpha directamente (0.0 a 1.0)
    alpha = tf.simpledialog.askfloat("Fusión", "Ingrese valor alpha (0.0 - 1.0):", minvalue=0.0, maxvalue=1.0)
    if alpha is None:
        return

    # Fusionar
    imagen_actual = tf.fusion(imagen_actual, img2, alpha)
    mostrar_imagen(imagen_actual)


def aplicar_fusion_ecualizada():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Abre primero una imagen base.")
        return
    ruta = filedialog.askopenfilename(title="Selecciona la segunda imagen")
    if not ruta:
        return
    img2 = Image.open(ruta).resize(imagen_actual.size)
    alpha = tf.simpledialog.askfloat("Fusión ecualizada", "Ingrese alpha (0.0 - 1.0):", minvalue=0.0, maxvalue=1.0)
    imagen_actual = tf.fusion_ecualizada(imagen_actual, img2, alpha)
    mostrar_imagen(imagen_actual)

def aplicar_rgb():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Abre primero una imagen.")
        return
    r, g, b = tf.extraer_rgb(imagen_actual)
    r.show(title="Canal Rojo")
    g.show(title="Canal Verde")
    b.show(title="Canal Azul")

def aplicar_cmyk():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Abre primero una imagen.")
        return
    c, m, y, k = tf.extraer_cmyk(imagen_actual)
    c.show(title="Cian")
    m.show(title="Magenta")
    y.show(title="Amarillo")
    k.show(title="Negro")

def aplicar_negativo():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Abre primero una imagen.")
        return
    imagen_actual = tf.negativo(imagen_actual)
    mostrar_imagen(imagen_actual)

def aplicar_grises():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Abre primero una imagen.")
        return
    imagen_actual = tf.a_grises(imagen_actual)
    mostrar_imagen(imagen_actual)


def aplicar_binarizacion():
    global imagen_actual
    if imagen_actual is None:
        messagebox.showwarning("Advertencia", "Abre primero una imagen.")
        return

    # Crear ventana emergente
    ventana_umbral = tk.Toplevel(root)
    ventana_umbral.title("Binarización")
    ventana_umbral.geometry("250x120")
    ventana_umbral.resizable(False, False)

    tk.Label(ventana_umbral, text="Ingrese un umbral (0-255):").pack(pady=10)
    entrada_umbral = tk.Entry(ventana_umbral, justify="center")
    entrada_umbral.pack()

    def confirmar():
        try:
            valor = int(entrada_umbral.get())
            if 0 <= valor <= 255:
                ventana_umbral.destroy()
                aplicar_binarizacion_valor(valor)
            else:
                messagebox.showerror("Error", "El umbral debe estar entre 0 y 255.")
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar un número entero.")

    tk.Button(ventana_umbral, text="Aceptar", command=confirmar).pack(pady=10)
    
def aplicar_binarizacion_valor(umbral):
    global imagen_actual
    try:
        imagen_actual = tf.binarizar(imagen_actual, umbral)
        mostrar_imagen(imagen_actual)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo aplicar la binarización.\nDetalles: {e}")



# -------- Interfaz --------
root = tk.Tk()
root.title("Proyecto- Procesamiento de Imágenes")
root.geometry("1200x700")

btn = tk.Button(root, text="Abrir imagen...", command=abrir_imagen)
btn.place(x=10,y=10)


slider = tk.Scale(root, from_=-1.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, length=220,command=aplicar_brillo_btn) #Slider para seleccionar el brillo
slider.place(x=350, y=5)

r_var=tk.BooleanVar(value=True)
g_var=tk.BooleanVar(value=True)
b_var=tk.BooleanVar(value=True)
chk_r=tk.Checkbutton(root, text="Rojo", variable=r_var, command=aplicar_canales)
chk_r.place(x=900,y=50)
chk_g=tk.Checkbutton(root, text="Verde", variable=g_var, command=aplicar_canales)
chk_g.place(x=900,y=80)
chk_b=tk.Checkbutton(root, text="Azul", variable=b_var, command=aplicar_canales)
chk_b.place(x=900,y=110)

btn_contraste_log = tk.Button(root, text="Contraste Logarítmico", command=aplicar_contraste_log)
btn_contraste_log.place(x=900, y=140)

btn_contraste_exp = tk.Button(root, text="Contraste Exponencial", command=aplicar_contraste_exp)
btn_contraste_exp.place(x=900, y=170)

# Botón para recorte interactivo
aplicar_recorte_interactivo_btn = tk.Button(root, text="Recorte Interactivo", command=aplicar_recorte_interactivo)
aplicar_recorte_interactivo_btn.place(x=900, y=450)

# ----- Control de Zoom -----
lbl_zoom = tk.Label(root, text="Zoom:")
lbl_zoom.place(x=10, y=60)

slider_zoom = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, length=220, command=aplicar_zoom)
slider_zoom.set(1.0)  # valor inicial sin zoom
slider_zoom.place(x=70, y=50)


# Slider y botón para rotación
lbl_rot = tk.Label(root)
lbl_rot.place(x=350, y=50)

slider_rot = tk.Scale(root, from_=-180, to=180, resolution=1, orient=tk.HORIZONTAL, length=220, command=aplicar_rotacion)
slider_rot.place(x=350, y=50)

# Botón para mostrar histograma
btn_hist = tk.Button(root, text="Mostrar histograma", command=mostrar_histograma)
btn_hist.place(x=900, y=200)


# --- Botones adicionales ---

#boton para fusionar imagenes
btn_fusion = tk.Button(root, text="Fusión imágenes", command=aplicar_fusion)
btn_fusion.place(x=900, y=260)

#boton para fusion ecualizada
btn_fusion_eq = tk.Button(root, text="Fusión ecualizada", command=aplicar_fusion_ecualizada)
btn_fusion_eq.place(x=900, y=290)


#boton para rgb
btn_rgb = tk.Button(root, text="Capas RGB", command=aplicar_rgb)
btn_rgb.place(x=900, y=310)

#boton para cmyk
btn_cmyk = tk.Button(root, text="Capas CMYK", command=aplicar_cmyk)
btn_cmyk.place(x=900, y=330)

#boton para negativo
btn_negativo = tk.Button(root, text="Negativo", command=aplicar_negativo)
btn_negativo.place(x=900, y=360)

#boton para escala de grises
btn_grises = tk.Button(root, text="Escala de grises", command=aplicar_grises)
btn_grises.place(x=900, y=390)

#boton para binarización
btn_bin = tk.Button(root, text="Binarizar", command=aplicar_binarizacion)
btn_bin.place(x=900, y=420)




lbl = tk.Label(root)
lbl.place(x=100,y=100)

root.mainloop()