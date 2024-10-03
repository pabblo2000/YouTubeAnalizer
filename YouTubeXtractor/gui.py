# gui.py

import tkinter as tk
from tkinter import ttk
import os
import video_info_extractor
import video_comment_extractor
import video_trascript_extract
import config
import threading
import to_sql

def run_gui():
    def submit_url():
        url = entry_url.get()
        if not url:
            update_message("Por favor, introduce una URL.")
        else:
            thread = threading.Thread(target=process_data, args=(url,))
            thread.start()

    def process_data(url):
        try:
            progress_bar["value"] = 0
            video_info_extractor.extract_info(url)
            progress_bar["value"] = 50

            video_id = video_info_extractor.extract_video_id(url)
            if video_id and extract_comments.get() == 1:
                video_comment_extractor.extract_comments(video_id)
                progress_bar["value"] = 65

            if video_id and extract_transcript.get() == 1:
                language_code = language_var.get()
                video_trascript_extract.extract_transcript(video_id, language_code)
                progress_bar["value"] = 80

            if save_to_sql.get() == 1:
                host = sql_host.get()
                user = sql_user.get()
                password = sql_password.get()
                database = sql_database.get()
                to_sql.save_to_database(host, user, password, database)
                progress_bar["value"] = 95

            update_message("Los datos se han guardado correctamente.")
            progress_bar["value"] = 100

            if close_after_execution.get() == 1:
                root.quit()

        except Exception as e:
            update_message(f"Ocurrió un error: {e}")

    def open_data_folder():
        data_path = os.path.join(os.getcwd(), 'data')
        if os.path.exists(data_path):
            os.startfile(data_path)
        else:
            update_message("La carpeta 'data' no existe.")

    def toggle_api_section():
        if api_label.winfo_ismapped():
            api_label.grid_remove()
            api_entry.grid_remove()
            save_api_button.grid_remove()
        else:
            api_label.grid(row=api_row, column=0, pady=5, sticky="w")
            api_entry.grid(row=api_row, column=1, padx=10, pady=5, sticky="w")
            save_api_button.grid(row=api_row + 1, column=0, columnspan=2, pady=10)

    def save_api_key():
        new_api_key = api_entry.get()
        if new_api_key:
            config.API_KEY = new_api_key
            update_config_file(new_api_key)
            update_message("La API Key ha sido actualizada correctamente.")
            toggle_api_section()  # Cerrar la sección si la API Key se guarda correctamente
        else:
            update_message("Por favor, introduce una nueva API Key.")

    def update_config_file(new_api_key):
        config_path = os.path.join(os.getcwd(), 'config.py')
        try:
            with open(config_path, 'w') as config_file:
                config_file.write(f'API_KEY = "{new_api_key}"\n')
            update_message("El archivo config.py ha sido actualizado.")
        except Exception as e:
            update_message(f"Error al actualizar config.py: {e}")

    def update_message(message):
        status_label.config(text=message)

    def toggle_transcript_options():
        if extract_transcript.get() == 1:
            language_label.grid(row=transcript_row, column=0, pady=5, sticky="w")
            language_menu.grid(row=transcript_row, column=1, pady=5, sticky="w")
        else:
            language_label.grid_remove()
            language_menu.grid_remove()
        adjust_position()

    def toggle_sql_options():
        if save_to_sql.get() == 1:
            sql_host_label.grid(row=sql_row, column=0, pady=5, sticky="w")
            sql_host.grid(row=sql_row, column=1, pady=5, sticky="w")
            sql_user_label.grid(row=sql_row + 1, column=0, pady=5, sticky="w")
            sql_user.grid(row=sql_row + 1, column=1, pady=5, sticky="w")
            sql_password_label.grid(row=sql_row + 2, column=0, pady=5, sticky="w")
            sql_password.grid(row=sql_row + 2, column=1, pady=5, sticky="w")
            sql_database_label.grid(row=sql_row + 3, column=0, pady=5, sticky="w")
            sql_database.grid(row=sql_row + 3, column=1, pady=5, sticky="w")
        else:
            sql_host_label.grid_remove()
            sql_host.grid_remove()
            sql_user_label.grid_remove()
            sql_user.grid_remove()
            sql_password_label.grid_remove()
            sql_password.grid_remove()
            sql_database_label.grid_remove()
            sql_database.grid_remove()
        adjust_position()

    def adjust_position():
        current_row = max(transcript_row + (1 if extract_transcript.get() == 1 else 0),
                          sql_row + (4 if save_to_sql.get() == 1 else 0))
        close_checkbutton.grid(row=current_row, column=0, pady=5, sticky="w", columnspan=2)
        open_data_button.grid(row=current_row + 1, column=0, padx=10, pady=10, sticky="w")
        expand_api_button.grid(row=current_row + 2, column=0, padx=10, pady=10, sticky="w")
        progress_bar.grid(row=current_row + 3, column=0, padx=10, pady=10, columnspan=2, sticky="w")
        status_label.grid(row=current_row + 4, column=0, pady=10, columnspan=4)

    def clear_url():
        entry_url.delete(0, tk.END)

    root = tk.Tk()
    root.title("YouTube Video Info & Comments Extractor")

    transcript_row = 3
    sql_row = 5
    api_row = 17

    # URL y botón de borrado
    label = tk.Label(root, text="Introduce la URL del video de YouTube:")
    label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    entry_url = tk.Entry(root, width=50)
    entry_url.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    clear_button = tk.Button(root, text="X", command=clear_url)
    clear_button.grid(row=0, column=2, padx=5, sticky="w")

    # Botón de Submit
    submit_button = tk.Button(root, text="Submit", command=submit_url)
    submit_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")

    # Casilla para extraer comentarios
    extract_comments = tk.IntVar(value=1)
    extract_comments_checkbutton = tk.Checkbutton(root, text="Extraer comentarios", variable=extract_comments)
    extract_comments_checkbutton.grid(row=1, column=0, pady=5, sticky="w", columnspan=2)

    # Casilla para extraer transcripción
    extract_transcript = tk.IntVar(value=1)
    extract_transcript_checkbutton = tk.Checkbutton(root, text="Extraer transcripción", variable=extract_transcript, command=toggle_transcript_options)
    extract_transcript_checkbutton.grid(row=2, column=0, pady=5, sticky="w")

    # Menú desplegable para seleccionar el idioma de la transcripción
    languages = [("Español", "es"), ("Inglés", "en"), ("Francés", "fr")]
    language_var = tk.StringVar(root)
    language_var.set("es")

    language_label = tk.Label(root, text="Selecciona el idioma de la transcripción:")
    language_menu = ttk.Combobox(root, textvariable=language_var, values=[lang[1] for lang in languages], state="readonly")

    # Casilla para guardar en SQL y configuraciones SQL
    save_to_sql = tk.IntVar(value=0)
    save_to_sql_checkbutton = tk.Checkbutton(root, text="Guardar en SQL", variable=save_to_sql, command=toggle_sql_options)
    save_to_sql_checkbutton.grid(row=4, column=0, pady=5, sticky="w")

    sql_host_label = tk.Label(root, text="Host:")
    sql_host = tk.Entry(root, width=20)
    sql_host.insert(0, 'localhost')

    sql_user_label = tk.Label(root, text="Usuario:")
    sql_user = tk.Entry(root, width=20)
    sql_user.insert(0, 'root')

    sql_password_label = tk.Label(root, text="Contraseña:")
    sql_password = tk.Entry(root, width=20, show='*')
    sql_password.insert(0, '1234')

    sql_database_label = tk.Label(root, text="Base de datos:")
    sql_database = tk.Entry(root, width=20)
    sql_database.insert(0, 'youtube')

    # Casilla para cerrar la aplicación al finalizar
    close_after_execution = tk.IntVar(value=0)
    close_checkbutton = tk.Checkbutton(root, text="Cerrar la aplicación al finalizar", variable=close_after_execution)

    # Botón para abrir la carpeta 'data'
    open_data_button = tk.Button(root, text="Abrir carpeta 'data'", command=open_data_folder, width=15)
    open_data_button.grid(row=sql_row + 5, column=0, padx=10, pady=10, sticky="w")

    # Botón para expandir y cambiar la API Key
    expand_api_button = tk.Button(root, text="Cambiar API Key", command=toggle_api_section, width=15)
    expand_api_button.grid(row=sql_row + 6, column=0, padx=10, pady=10, sticky="w")

    # Barra de progreso
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=250, mode="determinate")
    progress_bar.grid(row=sql_row + 7, column=0, padx=10, pady=10, columnspan=2, sticky="w")

    # Label y campo de entrada para la nueva API Key (inicialmente ocultos)
    api_label = tk.Label(root, text="Introduce la nueva API Key:")
    api_entry = tk.Entry(root, width=50)
    save_api_button = tk.Button(root, text="Guardar API Key", command=save_api_key)

    # Label para mostrar mensajes de estado
    status_label = tk.Label(root, text="", fg="red")

    # Mostrar configuraciones iniciales
    toggle_transcript_options()
    toggle_sql_options()
    adjust_position()

    root.mainloop()
