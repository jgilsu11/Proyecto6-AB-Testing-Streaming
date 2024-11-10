
import pandas as pd
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


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
    



def histograma_normal(df,ejex, titulo, control, tratamiento):
    """
    Genera histogramas comparativos para dos grupos de datos (control y tratamiento) dentro de un DataFrame, 
    mostrando la distribución de una variable específica.

    Parámetros:
    -----------
    df : pandas.DataFrame
        El DataFrame que contiene los datos a visualizar.
    ejex : str
        Nombre de la columna en `df` que se utilizará en el eje x de los histogramas.
    titulo : str
        Título general para la figura que contiene ambos histogramas.
    control : str
        Etiqueta del grupo de control en la columna `recomendacion_usuario`.
    tratamiento : str
        Etiqueta del grupo de tratamiento en la columna `recomendacion_usuario`.

    Detalles:
    ---------
    La función crea una figura con dos subgráficos (histogramas) lado a lado, 
    donde cada histograma representa la distribución de `ejex` para un grupo 
    específico de `recomendacion_usuario` (control y tratamiento).

    Retorno:
    --------
    None
        La función muestra la figura con los histogramas y no retorna ningún valor.

    """

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 5), sharey=True)
    axes = axes.flat
    sns.histplot(x=ejex, data=df[df["recomendacion_usuario"]== tratamiento], ax= axes[0])
    axes[0].set_xlabel(tratamiento)
    sns.histplot(x=ejex, data=df[df["recomendacion_usuario"]== control], ax= axes[1])
    axes[1].set_xlabel(control)
    fig.suptitle(titulo)
    plt.tight_layout()





def usar_whitney(df,columna_grupo , columna_metrica):
    lista_generos=df[columna_grupo].unique()
    combinaciones=list(combinations(lista_generos,2))
    for indice, valor in enumerate(combinaciones):
        estadistico, p_value= stats.mannwhitneyu(df[df[columna_grupo]== valor[0]][columna_metrica],df[df[columna_grupo]== valor[1]][columna_metrica])
        print(f"La evaluación de la hipótesis entre {valor[0]} y {valor[1]} da un p-value de {p_value}")
        if p_value >= 0.05:
            print("No hay diferencia")
            print(".................")
        else:
            print("Hay diferencia")
            print(".................")





def usar_kolmogorov(df,columna_grupo , columna_metrica):
    lista_genero= df[columna_grupo].unique().tolist()
    for indice, genero in enumerate(lista_genero):
        normalizale = df[df[columna_grupo] == genero][columna_metrica]
        media, desviacion = stats.norm.fit(normalizale) #esto se hace para ajustar los datos a una distribucion normal 
        estadistico, p_value = stats.kstest(normalizale, 'norm',args=(media,desviacion))   #aqui se almacene el estadístico y en la otra solo el p-value
        resultado = p_value > 0.05
        print(f"la metrica {columna_metrica} para {genero} sigue una distribución normal según el test de Kolmogorov-Smirnov. Esta afirmación es {resultado}")




def usar_bartlett(df, columna_grupos, columna_metrica):
    unicos=df[columna_grupos].unique()   #lista de grupos
    for grupo in unicos:
        df_metrica= df[df[columna_grupos]== grupo][columna_metrica]
        globals()[grupo] = df_metrica                                   #globals permite poner un parametro de una funcion en la variable a definir (de normal no se puede)
                                                                        #basicamente el globals lo empaqueta en un especie de diccionario en la que lo unico que se almacena en unicos (lista_grupo) son los nombres A B y C


    estadistico, p_value= stats.bartlett(*[globals()[var] for var in unicos])                 #al desempaquetar, de la A obtenemos sus estadisticos el * es para quitar la lista
    resultado = p_value > 0.05
    print(f"la metrica {columna_metrica} para {grupo} es homocedástica según el test de Bartlett. Esta afirmación es {resultado} con p-value de {p_value}")



def usar_ttest(df, columna_grupos, columna_metrica):
    unicos=df[columna_grupos].unique()   #lista de grupos
    for grupo in unicos:
        df_metrica= df[df[columna_grupos]== grupo][columna_metrica]
        globals()[grupo] = df_metrica                                   #globals permite poner un parametro de una funcion en la variable a definir (de normal no se puede)
                                                                        #basicamente el globals lo empaqueta en un especie de diccionario en la que lo unico que se almacena en unicos (lista_grupo) son los nombres A B y C
    estadistico, p_value= stats.ttest_ind(*[globals()[var] for var in unicos])                 #al desempaquetar, de la A obtenemos sus estadisticos el * es para quitar la lista
    resultado = p_value > 0.05
    if resultado ==True:
        print(f"Dado que el p_value es {p_value}, no hay evidencia suficiente para rechazar Ho con lo que no hay diferencia entre grupos de {columna_grupos} para {columna_metrica}")
    else:
        print(f"Dado que el p_value es {p_value}, hay evidencia suficiente para rechazar Ho con lo que hay diferencia entre grupos de {columna_grupos} para {columna_metrica}")




def graph_diferencias_entre_grupos(grupo,metrica,df,palette,titulo,ylabel):
    plt.figure(figsize=(8,5))
    sns.barplot(x=grupo,y=metrica,data=df, palette=palette)
    plt.title(titulo)
    plt.ylabel(ylabel)
    plt.tight_layout()