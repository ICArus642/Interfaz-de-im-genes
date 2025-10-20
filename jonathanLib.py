from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt

# Helpers -------------------------------------------------
# Convierte PIL.Image o numpy.ndarray a numpy.ndarray HxWxC uint8
def _to_numpy(img):
    if isinstance(img, np.ndarray):
        return img
    if isinstance(img, Image.Image):
        arr = np.array(img)
        # si imagen en modo L -> convertir a HxWx1 para consistencia
        return arr
    raise TypeError("La imagen debe ser PIL.Image o numpy.ndarray")

#Convierte numpy array a PIL.Image. Acepta HxW (grises) o HxWx3/4.
def _to_pil(arr):
    if isinstance(arr, Image.Image):
        return arr
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

# Asegura que la imagen tenga 3 canales RGB
def _ensure_3ch(arr):
    if arr.ndim == 2:
        return np.stack((arr,)*3, axis=-1)
    if arr.shape[2] == 4:
        # eliminar canal alpha para procesamiento por defecto
        return arr[:,:,:3]
    return arr

# 1. Brillo global ---------------------------------------

# Aumenta/disminuye brillo de toda la imagen
#valor en rango -1.0 .. 1.0, donde 0 no cambia. Multiplica por 255 internamente.
def brillo_global(img, valor):

    arr = _to_numpy(img).astype(np.float32)
    arr = _ensure_3ch(arr)
    arr = arr + valor * 255.0
    arr = np.clip(arr, 0, 255)
    return _to_pil(arr)

# 2. Brillo por canal ------------------------------------

def brillo_por_canal(img, r=0.0, g=0.0, b=0.0):
    arr = _to_numpy(img).astype(np.float32)
    arr = _ensure_3ch(arr)
    factores = np.array([r, g, b]) * 255.0
    arr = arr + factores.reshape((1,1,3))
    arr = np.clip(arr, 0, 255)
    return _to_pil(arr)

# 3. Contraste logarítmico ------------------------------

def contraste_log(img, c=1.0):
    arr = _to_numpy(img).astype(np.float32)
    arr = _ensure_3ch(arr)
    out = c * np.log1p(arr)
    # normalizar para cubrir 0..255
    out = out / np.max(out) * 255.0 if np.max(out) > 0 else out
    out = np.clip(out, 0, 255)
    return _to_pil(out)

# 4. Contraste exponencial (gamma) -----------------------

def contraste_exponencial(img, gamma=1.0):
    arr = _to_numpy(img).astype(np.float32)
    arr = _ensure_3ch(arr)
    norm = arr / 255.0
    out = 255.0 * (norm ** gamma)
    out = np.clip(out, 0, 255)
    return _to_pil(out)

# 5. Recorte de la imagen --------------------------------

def recortar(img, x1=50, y1=50, x2=None, y2=None):
    """
    Recorta una imagen (array NumPy) entre (x1, y1) y (x2, y2).
    Si no se especifica x2 o y2, toma la mitad inferior derecha por defecto.
    """
    # Obtener alto y ancho
    h, w = img.shape[:2]

    # Si no se indican coordenadas finales, usar parte central
    if x2 is None:
        x2 = int(w * 0.75)
    if y2 is None:
        y2 = int(h * 0.75)

    # Asegurar que los límites estén dentro de la imagen
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)

    # Recortar con slicing de NumPy
    recorte = img[y1:y2, x1:x2]

    return recorte



# 6. Zoom (ampliar sobre un área) ------------------------

def zoom_simple(img, factor):
    pil = _to_pil(_to_numpy(img))
    if factor <= 0:
        factor = 1
    ancho, alto = pil.size
    nuevo_tam = (int(ancho * factor), int(alto * factor))
    return pil.resize(nuevo_tam, Image.BICUBIC)

# 7. Rotación (ángulo libre) ----------------------------

def rotar(img, angulo, expand=True):
    pil = _to_pil(_to_numpy(img))
    return pil.rotate(-float(angulo), expand=expand, resample=Image.BICUBIC)

# 8. Visualización del histograma ------------------------

def histograma(img, mostrar=False):
    arr = _to_numpy(img)
    if arr.ndim == 2:
        hist, bins = np.histogram(arr.flatten(), bins=256, range=(0,255))
        if mostrar:
            plt.figure()
            plt.plot(bins[:-1], hist)
            plt.title('Histograma - nivel de gris')
            plt.xlabel('Intensidad')
            plt.ylabel('Frecuencia')
            plt.show()
        return {'l': (hist, bins)}

    arr = _ensure_3ch(arr)
    resultados = {}
    canales = ['r','g','b']
    for i, c in enumerate(canales):
        hist, bins = np.histogram(arr[:,:,i].flatten(), bins=256, range=(0,255))
        resultados[c] = (hist, bins)
        if mostrar:
            plt.figure()
            plt.plot(bins[:-1], hist)
            plt.title(f'Histograma - {c.upper()}')
            plt.xlabel('Intensidad')
            plt.ylabel('Frecuencia')
            plt.show()
    return resultados

# util: ecualizar un canal --------------------------------

def _equalize_channel(chan):
    hist, _ = np.histogram(chan.flatten(), bins=256, range=(0,255))
    cdf = hist.cumsum()
    cdf_mask = np.ma.masked_equal(cdf, 0)  # evita division por 0
    cdf_mask = (cdf_mask - cdf_mask.min()) * 255.0 / (cdf_mask.max() - cdf_mask.min())
    cdf_final = np.ma.filled(cdf_mask, 0).astype('uint8')
    return cdf_final[chan]

# 9. Fusión de dos imágenes ------------------------------

def fusion(img1, img2, alpha=0.5):
    pil1 = _to_pil(_to_numpy(img1)).convert('RGBA')
    pil2 = _to_pil(_to_numpy(img2)).convert('RGBA')
    if pil2.size != pil1.size:
        pil2 = pil2.resize(pil1.size, Image.BICUBIC)
    return Image.blend(pil1, pil2, float(alpha)).convert('RGB')


# 10. Fusión de imágenes ecualizadas ---------------------

def fusion_ecualizada(img1, img2, alpha=0.5):
    # convertir a numpy RGB
    a1 = _ensure_3ch(_to_numpy(img1).astype(np.uint8)).copy()
    a2 = _ensure_3ch(_to_numpy(img2).astype(np.uint8)).copy()
    # redimensionar a1/a2 al mismo tamaño (usar tamaño de a1)
    if a1.shape[0:2] != a2.shape[0:2]:
        pil2 = _to_pil(a2).resize((a1.shape[1], a1.shape[0]), Image.BICUBIC)
        a2 = np.array(pil2)

    out1 = np.zeros_like(a1)
    out2 = np.zeros_like(a2)
    for ch in range(3):
        out1[:,:,ch] = _equalize_channel(a1[:,:,ch])
        out2[:,:,ch] = _equalize_channel(a2[:,:,ch])

    mezclada = (out1.astype(np.float32) * alpha + out2.astype(np.float32) * (1.0-alpha))
    mezclada = np.clip(mezclada, 0, 255).astype(np.uint8)
    return _to_pil(mezclada)

# 11. Extracción de capas RGB ---------------------------

def extraer_rgb(img):
    arr = _to_numpy(img)
    arr = _ensure_3ch(arr)
    r = Image.fromarray(arr[:,:,0].astype(np.uint8)).convert('L')
    g = Image.fromarray(arr[:,:,1].astype(np.uint8)).convert('L')
    b = Image.fromarray(arr[:,:,2].astype(np.uint8)).convert('L')
    return r, g, b

# 12. Extracción de capas CMYK --------------------------

def extraer_cmyk(img):
    pil = _to_pil(_to_numpy(img)).convert('CMYK')
    c,m,y,k = pil.split()
    return c, m, y, k

# 13. Foto negativa -------------------------------------

def negativo(img):
    arr = _to_numpy(img).astype(np.uint8)
    inv = 255 - arr
    return _to_pil(inv)

# 14. Conversión a escala de grises ----------------------

def a_grises(img):
    pil = _to_pil(_to_numpy(img))
    return pil.convert('L')

# 15. Binarización --------------------------------------
def binarizar(img, umbral):
    gray = a_grises(img)
    arr = np.array(gray).astype(np.uint8)
    out = (arr >= int(umbral)).astype(np.uint8) * 255
    return Image.fromarray(out).convert('L')



# Si se ejecuta como script, mostrar ejemplo rapido ----------------
if __name__ == '__main__':
    print('Libimg: módulo de utilidades para imágenes. Importar y usar sus funciones en su proyecto.')
    
    
    
    
def layer_prog(img, r=True, g=True, b=True):
    
    arr = _to_numpy(img).astype(np.float32)
    arr = _ensure_3ch(arr)

    # Crear máscara [r,g,b] -> [1 o 0]
    mask = np.array([float(r), float(g), float(b)]).reshape((1, 1, 3))
    arr = arr * mask

    arr = np.clip(arr, 0, 255)
    return arr.astype(np.uint8)