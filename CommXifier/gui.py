# gui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os 

class AppGUI:
    def __init__(self, master, db_controller):
        self.master = master
        self.db_controller = db_controller  # Controlador de la base de datos
        master.title("Análisis de Sentimiento")

        # Obtener la ruta del icono
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

        # Establecer el icono
        master.iconbitmap(icon_path)

        master.geometry("600x500") 

        # Campos para credenciales
        tk.Label(master, text="Host:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entry_host = tk.Entry(master, width=30)
        self.entry_host.insert(0, 'localhost')
        self.entry_host.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(master, text="Usuario:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entry_user = tk.Entry(master, width=30)
        self.entry_user.insert(0, 'root')
        self.entry_user.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(master, text="Contraseña:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.entry_password = tk.Entry(master, show="*", width=30)
        self.entry_password.insert(0, '1234')
        self.entry_password.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(master, text="Base de datos:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.entry_database = tk.Entry(master, width=30)
        self.entry_database.insert(0, 'youtube')
        self.entry_database.grid(row=3, column=1, padx=10, pady=5)

        self.btn_conectar = tk.Button(master, text="Conectar", command=self.conectar_bd, width=20)
        self.btn_conectar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Lista de videos
        tk.Label(master, text="Selecciona uno o más videos para analizar:").grid(row=5, column=0, columnspan=2)
        self.listbox_videos = tk.Listbox(master, selectmode=tk.MULTIPLE, width=60, height=10)
        self.listbox_videos.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.btn_analizar = tk.Button(master, text="Analizar Sentimiento", command=self.analizar_sentimiento, width=20)
        self.btn_analizar.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(master, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        # Mensaje de estado
        self.status_label = tk.Label(master, text="")
        self.status_label.grid(row=9, column=0, columnspan=2)

    def conectar_bd(self):
        host = self.entry_host.get() or 'localhost'
        user = self.entry_user.get() or 'root'
        password = self.entry_password.get() or ''
        database = self.entry_database.get() or 'youtube'
        try:
            self.db_controller.connect(host, user, password, database)
            messagebox.showinfo("Conexión", "Conexión exitosa a la base de datos")
            self.obtener_videos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar: {e}")

    def obtener_videos(self):
        videos = self.db_controller.get_videos()
        self.listbox_videos.delete(0, tk.END)
        for video in videos:
            video_title = video[1]
            self.listbox_videos.insert(tk.END, video_title)

    def update_progress(self, value):
        self.progress['value'] = value
        self.master.update_idletasks()

    def analizar_sentimiento(self):
        seleccion = self.listbox_videos.curselection()
        if not seleccion:
            messagebox.showwarning("Selección", "Por favor, selecciona al menos un video")
            return
        video_titles = [self.listbox_videos.get(idx) for idx in seleccion]
        video_ids = self.db_controller.get_video_ids_by_titles(video_titles)
        self.progress['value'] = 0
        self.status_label.config(text="Iniciando análisis...")
        self.master.update_idletasks()
        try:
            def progress_callback(value):
                self.update_progress(value)
                self.status_label.config(text=f"Procesando... {int(value)}%")
                self.master.update_idletasks()
            self.db_controller.analyze_sentiment(video_ids, progress_callback)
            self.status_label.config(text="Análisis completado")
            messagebox.showinfo("Completado", "Análisis de sentimiento completado")
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar: {e}")
