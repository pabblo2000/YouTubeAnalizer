# video_info_extractor.py

import os
import re
from googleapiclient.discovery import build
import pandas as pd
import config

# Asegúrate de que la carpeta 'data' exista
if not os.path.exists('data'):
    os.makedirs('data')

# Función para extraer la información del video
def extract_info(url):
    video_id = extract_video_id(url)
    
    if not video_id:
        print("URL no válida")
        return
    
    youtube = build('youtube', 'v3', developerKey=config.API_KEY)
    
    # Obtener información básica del video
    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    )
    response = request.execute()
    
    video_info = response['items'][0]
    snippet = video_info['snippet']
    statistics = video_info['statistics']
    content_details = video_info['contentDetails']
    
    # Extraer los datos requeridos
    data = {
        'video_id': video_id,
        'video_title': snippet['title'],
        'views': statistics.get('viewCount', 0),
        'likes': statistics.get('likeCount', 0),
        'n_comments': statistics.get('commentCount', 0),
        'duration': content_details['duration'],
        'channel_name': snippet['channelTitle'],
        'subscribers': get_channel_subscribers(youtube, snippet['channelId'])
    }
    
    # Crear un DataFrame de pandas
    df = pd.DataFrame([data])
    
    # Archivo CSV de salida
    output_file = os.path.join('data', 'video_info.csv')
    
   # Si el archivo no existe, lo creamos; de lo contrario, añadimos los nuevos datos
    if not os.path.exists(output_file):
        df.to_csv(output_file, index=False, encoding='utf-8')
    else:
        df.to_csv(output_file, mode='a', header=False, index=False, encoding='utf-8')

    
    print(f"Datos del video guardados o actualizados en {output_file}")
    return df

# Función para extraer el ID del video desde varias formas de URL
def extract_video_id(url):
    # Diferentes patrones de URL de YouTube
    patterns = [
        r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+v=([^&]+)',
        r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/([^&]+)'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(4)  # Extraer el ID del video

    return None

# Función para obtener el número de suscriptores del canal
def get_channel_subscribers(youtube, channel_id):
    channel_request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    channel_response = channel_request.execute()
    return channel_response['items'][0]['statistics'].get('subscriberCount', 0)
