import os
from tkinter import messagebox
from ventana_principal import VentanaCarrera
from vehiculo import Vehiculo

class ControladorCarrera:
    def __init__(self):
        self.vista = VentanaCarrera()
        self.vehiculos = []
        self.tiempos_finales = []
        self.carrera_activa = False

        self.vista.btn_accion.config(command=self.controlar_carrera)
        self.vista.slider_velocidad.config(command=self.cambiar_velocidad_juego)

        self.crear_vehiculos()

    def crear_vehiculos(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_img = os.path.join(base_dir, "auto.png")

        self.vehiculos.clear()
        for i in range(10):
            auto = Vehiculo(i + 1, ruta_img, self.vista.pista)
            y_pos = 10 + (i * 33)
            auto.reiniciar(10, y_pos)
            self.vehiculos.append(auto)

    def controlar_carrera(self):
        if not self.carrera_activa:
            self.carrera_activa = True
            self.vista.btn_accion.config(text="Reiniciar Carrera")
            
            for item in self.vista.tabla_resultados.get_children():
                self.vista.tabla_resultados.delete(item)
            self.tiempos_finales.clear()

            self.vista.apuesta.config(state="disabled")
            self.vista.rondas_global.config(state="disabled")

            rondas = int(self.vista.rondas_global.get())
            
            # Recreamos los vehículos para asegurar hilos nuevos listos para ejecutarse (.start())
            base_dir = os.path.dirname(os.path.abspath(__file__))
            ruta_img = os.path.join(base_dir, "auto.png")
            self.vehiculos.clear()

            for i in range(10):
                auto = Vehiculo(i + 1, ruta_img, self.vista.pista)
                y_pos = 10 + (i * 33)
                self.vehiculos.append(auto)
                auto.iniciar(10, y_pos, rondas, callback_final=self.registrar_llegada)
        else:
            self.reiniciar_juego()

    def cambiar_velocidad_juego(self, valor):
        factor = float(valor)
        for auto in self.vehiculos:
            auto.actualizar_factor_tiempo(factor)

    def registrar_llegada(self, id_vehiculo, tiempo_total):
        self.tiempos_finales.append((id_vehiculo, tiempo_total))

        if len(self.tiempos_finales) == len(self.vehiculos):
            self.tiempos_finales.sort(key=lambda x: x[1])
            # Usamos after para actualizar la UI desde el hilo principal de Tkinter de forma segura
            self.vista.after(0, self.mostrar_resultados)

    def mostrar_resultados(self):
        ganador_id = self.tiempos_finales[0][0]
        apuesta_id = int(self.vista.apuesta.get().split()[1])

        for lugar, (id_v, tiempo) in enumerate(self.tiempos_finales):
            self.vista.tabla_resultados.insert(
                "", "end", values=(f"#{lugar + 1}", f"Vehículo {id_v}", f"{tiempo:.2f} s")
            )

        if ganador_id == apuesta_id:
            messagebox.showinfo(
                "¡Resultado!",
                f"¡Felicidades! Solo fue suerte, El Vehículo {ganador_id} ganó la carrera"
            )
        else:
            messagebox.showwarning(
                "¡Resultado!",
                f"JAJAJA Perdiste!! El ganador fue el Vehículo {ganador_id}, no apuestes por: {apuesta_id}."
            )

    def reiniciar_juego(self):
        self.carrera_activa = False
        self.vista.btn_accion.config(text="Iniciar Carrera")
        self.vista.apuesta.config(state="readonly")
        self.vista.rondas_global.config(state="normal")

        for auto in self.vehiculos:
            auto.reiniciar(10, auto.y)


if __name__ == "__main__":
    app = ControladorCarrera()
    app.vista.mainloop()