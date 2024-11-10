
import pandas as pd
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from psycopg2 import sql



def iniciar_conexion(host,user,password,port,nombre_basedatos):
    """
    Establece una conexión a una base de datos PostgreSQL con los parámetros especificados.

    La función intenta conectarse a la base de datos utilizando las credenciales y configuraciones proporcionadas.
    En caso de éxito, la conexión se establece con autocommit habilitado. Si ocurre un error en la conexión,
    se imprime el mensaje de error.

    Args:
        host (str): Dirección del servidor de la base de datos.
        user (str): Nombre de usuario para la autenticación.
        password (str): Contraseña del usuario.
        port (int): Puerto del servidor de la base de datos.
        nombre_basedatos (str): Nombre de la base de datos a la que se conectará.

    Returns:
        psycopg2.extensions.connection: Objeto de conexión a la base de datos PostgreSQL.
    """
    try: 
        conexion= psycopg2.connect(
            database= nombre_basedatos,
            user= user,
            password= password,
            host= host,
            port= port
        )
        conexion.autocommit = True
        return conexion
    except psycopg2.Error as e:
        return print(f"Ocurrió el error {e}")
    


def asignar_visualizacion(row):
    """
    Asigna una etiqueta de visualización completa o incompleta a un registro basado en los minutos vistos
    en comparación con la duración total del contenido.

    La función verifica si los minutos vistos son mayores o iguales a la duración total del contenido.
    Si es así, asigna la etiqueta "visualización completa", de lo contrario, asigna "visualización incompleta".

    Args:
        row (pandas.Series): Fila de un DataFrame que contiene los valores de "minutos_vistos" y "duracion_contenido".

    Returns:
        str: "visualizacion completa" si los minutos vistos son mayores o iguales a la duración del contenido,
             de lo contrario, "visualizacion incompleta".
    """
    if row["minutos_vistos"] >= row["duracion_contenido"]:
        return "visualizacion completa"
    else:
        return "visualizacion incompleta"