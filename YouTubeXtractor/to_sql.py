# https://dev.mysql.com/downloads/file/?id=532678

# pip install mysql-connector-python pandas

import mysql.connector #type: ignore
from mysql.connector import Error #type: ignore
import pandas as pd #type: ignore
from pandas.errors import EmptyDataError #type: ignore
import re #type: ignore
from datetime import datetime #type: ignore
from datetime import timedelta #type: ignore


def sql_connection(host, user, password):
    """Connect to MySQL database"""

    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        )
    print("Connection to MySQL successful")
    return connection    

def sql_table_creation(host, user, password, database):

    connection = sql_connection(host=host, user=user, password=password)

    cursor = connection.cursor()

    # Crear la base de datos si no existe
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
    cursor.execute(f"USE {database};")

    # Crear la tabla para video_info con video_id como clave primaria
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS video_info (
        video_id VARCHAR(255) PRIMARY KEY,
        video_title VARCHAR(255),
        views INT,
        likes INT,
        n_comments INT,
        duration TIME,
        channel_name VARCHAR(255),
        subscribers INT
    );
    """)

    # Crear la tabla para video_comments con video_id como clave foránea
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS video_comments (
        video_id VARCHAR(255),
        comment_id VARCHAR(255),
        comment_user VARCHAR(255),
        comment TEXT,
        comment_like INT,
        time_published DATETIME,
        FOREIGN KEY (video_id) REFERENCES video_info(video_id)
    );
    """)

    # Crear la tabla para video_transcript con video_id como clave foránea
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS video_transcript (
        video_id VARCHAR(255),
        video_transcript LONGTEXT,
        FOREIGN KEY (video_id) REFERENCES video_info(video_id),
        UNIQUE (video_id)   
    );
    """)

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    cursor.close()
    connection.close()

    print(f"Las tablas se han creado correctamente o ya existian en la base de datos {database}")


def duration_to_datetime(iso_duration):
    # Expresión regular para extraer las horas, minutos y segundos
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
    match = pattern.match(iso_duration)
    
    if not match:
        return "00:00:00"  # Devolver 00:00:00 si el formato no es correcto

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    # Convertir a un objeto timedelta
    duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    
    # Formatear la duración a hh:mm:ss
    return str(duration)


def time_published_to_datetime(time_string):
    try:
        # Convertir la cadena de tiempo a un objeto datetime
        dt = datetime.fromisoformat(time_string.replace("Z", "+00:00"))
        # Formatear el objeto datetime a una cadena legible
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        # Si hay un error en la conversión, devolver una fecha por defecto o manejar el error
        return "1970-01-01 00:00:00"

def insert_data(host, user, password, database):
    # Leer los CSV
    try:
        video_comments = pd.read_csv('data/video_comments.csv')
    except EmptyDataError:
        print("No se encontraron datos en el archivo 'video_comments.csv'")
    except FileNotFoundError:
        print("No se encontró el archivo 'video_comments.csv'")
    try:
        video_info = pd.read_csv('data/video_info.csv')
    except EmptyDataError:
        print("No se encontraron datos en el archivo 'video_info.csv'")
    except FileNotFoundError:
        print("No se encontró el archivo 'video_info.csv'")
    try:
        video_transcript = pd.read_csv('data/video_transcript.csv')
    except EmptyDataError:
        print("No se encontraron datos en el archivo 'video_transcript.csv'")
    except FileNotFoundError:
        print("No se encontró el archivo 'video_transcript.csv'")

    try:
        # Reemplazar NaN con valores adecuados o nulos
        video_comments = video_comments.fillna({
            'comment_like': 0,          # Ejemplo: likes de comentarios faltantes se reemplazan por 0
            'time_published': '1970-01-01 00:00:00'  # Fecha por defecto para tiempos faltantes
        }).fillna('')  # Otros NaN se rellenan con cadenas vacías
    except Exception as e:
        print(f"Error al reemplazar NaN en video_comments: {e}")

    video_info = video_info.fillna({
        'views': 0,
        'likes': 0,
        'n_comments': 0,
        'subscribers': 0,
        'duration': '00:00:00',
        'channel_name': 'Error',
        'video_title': 'Error'
    }).fillna('')

    try:
        video_transcript = video_transcript.fillna('')
    except Exception as e:
        print(f"Error al reemplazar NaN en video_transcript: {e}")

    try:
        # Convertir la columna 'duration' al formato adecuado
        video_info['duration'] = video_info['duration'].apply(duration_to_datetime)
    except Exception as e:
        print(f"Error al convertir la columna 'duration' a datetime: {e}")
    

    try:
        # Convertir la columna 'time_published' al formato adecuado
        video_comments['time_published'] = video_comments['time_published'].apply(time_published_to_datetime)
    except Exception as e:
        print(f"Error al convertir la columna 'time_published' a datetime: {e}")

    # Conexión a MySQL Workbench
    connection = sql_connection(host=host, user=user, password=password)

    cursor = connection.cursor()

    # Usar la base de datos VideoData
    cursor.execute(f"USE {database};")

    try:
        # Insertar datos en la tabla video_info
        for _, row in video_info.iterrows():
            try:
                cursor.execute("""
                INSERT INTO video_info (video_id, video_title, views, likes, n_comments, duration, channel_name, subscribers)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, tuple(row))
            except Error as e:
                print(f"Error al insertar datos en la tabla video_info: {e}")
    except Exception as e:
        print(f"Error al insertar datos en la tabla video_info: {e}")

    try:
        # Insertar datos en la tabla video_comments
        for _, row in video_comments.iterrows():
            try:
                cursor.execute("""
                INSERT INTO video_comments (video_id, comment_id, comment_user, comment, comment_like, time_published)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, tuple(row))
            except Error as e:
                print(f"Error al insertar datos en la tabla video_comments: {e}")
    except Exception as e:
        print(f"Error al insertar datos en la tabla video_comments: {e}")

    try:
        # Insertar datos en la tabla video_transcript
        for _, row in video_transcript.iterrows():
            try:
                cursor.execute("""
                INSERT INTO video_transcript (video_id, video_transcript)
                VALUES (%s, %s)
                """, tuple(row))
            except Error as e:
                print(f"Error al insertar datos en la tabla video_transcript: {e}")
    except Exception as e:
        print(f"Error al insertar datos en la tabla video_transcript: {e}")

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    cursor.close()
    connection.close()

    print("Los datos de los CSV se han insertado correctamente en las tablas.")


def save_to_database(host, user, password, database):
    sql_table_creation(host=host, user=user, password=password, database=database)
    insert_data(host=host, user=user, password=password, database=database)




