import tkinter as tk
from tkinter import ttk


class VentanaCarrera(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Carrera de Vehículos")
        self.geometry("950x700")
        self.configure(bg="#0f172a")

        self._aplicar_estilos()
        self._init_ui()

    def _aplicar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TFrame", background="#0f172a")
        style.configure("Dark.TFrame", background="#1e293b")
        
        style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 10))
        style.configure("Dark.TLabel", background="#1e293b", foreground="#f8fafc", font=("Segoe UI", 10))
       
        style.configure("TButton", background="#3b82f6", foreground="#ffffff", font=("Segoe UI", 10, "bold"))
        style.map("TButton", background=[("active", "#2563eb"), ("disabled", "#334155")])
        
        style.configure("Treeview", background="#1e293b", foreground="#f8fafc", fieldbackground="#bbd2f7", bordercolor="#334155", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#0f172a", foreground="#94a3b8", relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#b0ceff")], foreground=[("selected", "#ffffff")])

    def _init_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        col_izq = ttk.Frame(main_frame)
        col_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        frame_controles = ttk.Frame(col_izq)
        frame_controles.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_controles, text="Haz tu apuesta:").pack(side=tk.LEFT, padx=5)
        self.apuesta = ttk.Combobox(frame_controles, values=[f"Auto {i}" for i in range(1, 11)], state="readonly", width=10)
        self.apuesta.current(0)
        self.apuesta.pack(side=tk.LEFT, padx=5)

        ttk.Label(frame_controles, text="Rondas (Idas/Vueltas):").pack(side=tk.LEFT, padx=5)
        self.rondas_global = ttk.Spinbox(frame_controles, from_=1, to=10, width=5)
        self.rondas_global.set(1)
        self.rondas_global.pack(side=tk.LEFT, padx=5)

        self.btn_accion = ttk.Button(frame_controles, text="Iniciar Carrera")
        self.btn_accion.pack(side=tk.LEFT, padx=10)

        self.pista = tk.Canvas(col_izq, bg="#2e2e2e", highlightthickness=1, highlightbackground="#334155")
        self.pista.pack(fill=tk.BOTH, expand=True)

        frame_slider = ttk.Frame(col_izq)
        frame_slider.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(frame_slider, text="Acelerar:").pack(side=tk.LEFT, padx=5)
        self.slider_velocidad = ttk.Scale(frame_slider, from_=1, to=10, orient=tk.HORIZONTAL)
        self.slider_velocidad.set(1)
        self.slider_velocidad.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        col_der = ttk.Frame(main_frame, style="Dark.TFrame")
        col_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, ipadx=10, ipady=10)

        ttk.Label(col_der, text="Tabla de Posiciones:", style="Dark.TLabel").pack(anchor="w", pady=(0, 10))
        
        columnas = ("lugar", "vehiculo", "tiempo")
        self.tabla_resultados = ttk.Treeview(col_der, columns=columnas, show="headings", height=15)
        self.tabla_resultados.heading("lugar", text="Lugar")
        self.tabla_resultados.heading("vehiculo", text="Vehículo")
        self.tabla_resultados.heading("tiempo", text="Tiempo (seg)")
        
        self.tabla_resultados.column("lugar", width=60, anchor="center")
        self.tabla_resultados.column("vehiculo", width=90, anchor="center")
        self.tabla_resultados.column("tiempo", width=100, anchor="center")
        
        self.tabla_resultados.pack(fill=tk.BOTH, expand=True)