# YouTubeAnalyzer

YouTubeAnalyzer es un proyecto que consta de **dos aplicaciones independientes**, cada una con su propia interfaz gráfica (GUI). El objetivo principal es extraer y analizar datos de videos de YouTube utilizando la API de YouTube y aplicar machine learning para clasificar los comentarios.

## Aplicaciones

### 1. **YouTubeXtractor**

Esta aplicación permite extraer información detallada sobre los videos y los comentarios de YouTube.

#### Funcionalidades
- **Extracción de Información del Video:**
  - ID del video
  - Título del video
  - Número de vistas
  - Número de likes
  - Duración del video
  - Nombre del canal
  - Número de suscriptores
- **Extracción de Comentarios del Video:**
  - ID del comentario
  - Usuario que comentó
  - Contenido del comentario
  - Número de likes en el comentario
  - Fecha de publicación del comentario
- **Exportación de Datos:**
  - Los datos extraídos se guardan en archivos CSV dentro de la carpeta `/data`.
  - Opcionalmente, puedes exportar los datos a una base de datos MySQL.

#### GUI
- La GUI permite ingresar la URL del video de YouTube y seleccionar si se desea extraer la información del video, los comentarios o ambos.
- También se puede elegir la opción de exportar los datos a una base de datos SQL.

### 2. **CommXifier**

Esta aplicación está centrada en la clasificación de comentarios de YouTube usando machine learning.

#### Funcionalidades
- **Clasificación de Comentarios:**
  - Utiliza modelos de machine learning para clasificar los comentarios en categorías como "positivos", "negativos" o "neutros".
  - Aplica un modelo de regresión logística con TF-IDF para la representación de los comentarios.
- **Exportación de Resultados:**
  - Los resultados de la clasificación se pueden guardar en archivos CSV.
  - Posibilidad de almacenar los resultados en una base de datos SQL.

#### GUI
- La GUI permite cargar un archivo CSV con comentarios extraídos o ingresar una URL de video para extraer comentarios y clasificarlos.
- Ofrece la opción de visualizar los resultados de la clasificación directamente en la interfaz.

## Estructura del Proyecto

- `main_data_extractor.py`: Ejecuta la aplicación de extracción de datos.
- `main_comment_classifier.py`: Ejecuta la aplicación de clasificación de comentarios.
- `gui_data_extractor.py`: Contiene la interfaz gráfica de la aplicación de extracción de datos.
- `gui_comment_classifier.py`: Contiene la interfaz gráfica de la aplicación de clasificación de comentarios.
- `video_info_extractor.py`: Módulo para extraer información del video.
- `video_comment_extractor.py`: Módulo para extraer los comentarios del video.
- `model.py`: Módulo que contiene el modelo de clasificación de comentarios.
- `sql_connect.py`: Módulo para la conexión con una base de datos SQL.
- `sql_data_insert.py`: Módulo para insertar datos en la base de datos.
- `/data/`: Carpeta donde se almacenan los archivos CSV generados.

