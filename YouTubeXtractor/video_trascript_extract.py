# video_trascript_extract.py

from youtube_transcript_api import YouTubeTranscriptApi
import csv
import os

def extract_transcript(video_id, language="en"):
    try:
        # Obtener la transcripción del video en el idioma seleccionado
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # Concatenar todos los textos de la transcripción en una sola cadena
        transcript_text = " ".join([entry['text'] for entry in transcript])

        # Crear un archivo CSV para guardar la transcripción
        output_file = os.path.join('data', 'video_transcript.csv')

        # Verificar si el archivo ya existe
        file_exists = os.path.isfile(output_file)

        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Escribir el encabezado solo si el archivo no existía previamente
            if not file_exists:
                writer.writerow(['video_id', 'video_transcript'])

            # Escribir el video_id y la transcripción completa en una sola fila
            writer.writerow([video_id, transcript_text])

        print(f"Transcripción guardada en {output_file}")
        return output_file

    except Exception as e:
        print(f"Error al extraer la transcripción: {e}")
        return None
