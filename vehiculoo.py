import threading
import time
import random
from PIL import Image, ImageTk

class Vehiculo(threading.Thread):
    def __init__(self, id_vehiculo, ruta_imagen, canvas):
        super().__init__()
        self.id_vehiculo = id_vehiculo
        self.canvas = canvas
        self.y = 0
        self.x = 10
        self.factor_tiempo = 1.0
        self.rondas = 1
        self.callback_final = None
        self.daemon = True  # Hilo en segundo plano
        
        # Cargar imagen y crear en el canvas
        imagen_pil = Image.open(ruta_imagen).resize((40, 20))
        self.imagen = ImageTk.PhotoImage(imagen_pil)
        self.item_id = self.canvas.create_image(self.x, self.y, image=self.imagen, anchor="nw")

    def reiniciar(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.item_id, self.x, self.y)

    def iniciar(self, x, y, rondas, callback_final):
        self.reiniciar(x, y)
        self.rondas = rondas
        self.callback_final = callback_final
        self.start()  # Dispara el método run() en un hilo concurrente

    def actualizar_factor_tiempo(self, factor):
        self.factor_tiempo = factor

    def run(self):
        inicio_tiempo = time.time()
        ancho_pista = self.canvas.winfo_width() - 50
        if ancho_pista < 100:
            ancho_pista = 600

        meta_total = ancho_pista * self.rondas
        distancia_recorrida = 0

        while distancia_recorrida < meta_total:
            avance = random.randint(5, 15)
            distancia_recorrida += avance
            self.x += avance

            if self.x > self.canvas.winfo_width() - 40:
                self.x = 10  # Vuelve al inicio si llega al borde antes de completar las rondas

            # Actualizamos las coordenadas en el Canvas
            self.canvas.coords(self.item_id, self.x, self.y)
            
            tiempo_dormir = 0.05 / self.factor_tiempo
            time.sleep(tiempo_dormir)

        tiempo_total = time.time() - inicio_tiempo
        
        if self.callback_final:
            self.callback_final(self.id_vehiculo, tiempo_total)