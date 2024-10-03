# video_comment_extractor.py

import os
from googleapiclient.discovery import build
import pandas as pd
import config

# Asegúrate de que la carpeta 'data' exista
if not os.path.exists('data'):
    os.makedirs('data')

# Función para extraer comentarios del video
def extract_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=config.API_KEY)
    
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()

    while request is not None:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append({
                'video_id': video_id,  # Relacionar cada comentario con el video
                'comment_id': item['id'],
                'comment_user': comment['authorDisplayName'],
                'comment': comment['textDisplay'],
                'comment_like': comment['likeCount'],
                'time_published': comment['publishedAt']
            })
        # Verificar si hay más páginas de comentarios
        if 'nextPageToken' in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response['nextPageToken'],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break

    # Crear un DataFrame con los comentarios
    df = pd.DataFrame(comments)
    
    # Archivo CSV de salida
    output_file = os.path.join('data', 'video_comments.csv')
    
    # Si el archivo no existe, lo creamos; de lo contrario, añadimos los nuevos datos
    if not os.path.exists(output_file):
        df.to_csv(output_file, index=False)
    else:
        df.to_csv(output_file, mode='a', header=False, index=False, encoding='utf-8')
    
    print(f"Comentarios guardados o actualizados en {output_file}")
    return df
