# database.py
import mysql.connector
from sentiment_analysis import SentimentAnalyzer

class DatabaseController:
    def __init__(self):
        self.conn = None
        self.sentiment_analyzer = SentimentAnalyzer()

    def connect(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def get_videos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT video_id, video_title FROM video_info")
        videos = cursor.fetchall()
        cursor.close()
        return videos

    def get_video_ids_by_titles(self, video_titles):
        cursor = self.conn.cursor()
        format_strings = ','.join(['%s'] * len(video_titles))
        query = f"SELECT video_id FROM video_info WHERE video_title IN ({format_strings})"
        cursor.execute(query, tuple(video_titles))
        video_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return video_ids

    def analyze_sentiment(self, video_ids, progress_callback=None):
        cursor = self.conn.cursor()
        total_videos = len(video_ids)
        processed_videos = 0
        for idx, video_id in enumerate(video_ids):
            # Obtener transcrito del video
            cursor.execute("SELECT video_transcript FROM video_transcript WHERE video_id = %s", (video_id,))
            result = cursor.fetchone()
            if result:
                transcript = result[0]
            else:
                transcript = ''
            # Obtener comentarios del video
            cursor.execute("SELECT comment_id, comment FROM video_comments WHERE video_id = %s", (video_id,))
            comments = cursor.fetchall()
            # Verificar y agregar columna 'sentiment' si no existe
            cursor.execute("SHOW COLUMNS FROM video_comments LIKE 'sentiment'")
            result = cursor.fetchone()
            if not result:
                cursor.execute("ALTER TABLE video_comments ADD COLUMN sentiment VARCHAR(10)")
            # Analizar sentimiento de cada comentario
            total_comments = len(comments)
            for i, (comment_id, comment) in enumerate(comments):
                combined_text = comment + " " + transcript
                sentiment = self.sentiment_analyzer.analyze(combined_text)
                cursor.execute("UPDATE video_comments SET sentiment = %s WHERE comment_id = %s", (sentiment, comment_id))
                if progress_callback:
                    progress = ((i + 1) / total_comments) * 100
                    progress_callback(progress)
            self.conn.commit()
            processed_videos += 1
            if progress_callback:
                overall_progress = (processed_videos / total_videos) * 100
                progress_callback(overall_progress)
        cursor.close()
