import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo Excel
archivo = "C:\\Users\\bryan.mery\\Desktop\\Analisis CV  - TRL.xlsx"  # Ajusta la ruta
df = pd.read_excel(archivo, sheet_name='Consolidado')

# Excluir filas con "No aplica" o "-" en las columnas C y E
df = df[(df['Nivel de desarrollo alcanzado según ejecutivo'] != 'No aplica') & 
        (df['TRL esperado al finalizar el proyecto'] != 'No aplica') & 
        (df['Nivel de desarrollo alcanzado según ejecutivo'] != '-') & 
        (df['TRL esperado al finalizar el proyecto'] != '-')]

# Actualización de la tabla de homologación
homologacion_trl = {
    'Concepto o idea': ['TRL 1 - Principios básicos estudiados', 'TRL 2 - Concepto tecnológico formulado', 'TRL 3 - Prueba de concepto experimental'],
    'Prototipo': ['TRL 4 -Tecnología validada en laboratorio'],
    'Prototipo Funcional': ['TRL 5 - Tecnología validada en un entorno relevante'],
    'Producto Mínimo Viable': ['TRL 6 - Modelo de sistema / subsistema o demostración de prototipo en un entorno relevante (terreno o espacio)', 
            'TRL 7 - Demostración de sistema o prototipo completo demostrado en entorno operacional'],
    'Producto Funcional': ['TRL 8 - Sistema completo y certificado a través de pruebas y demostraciones'],
    'Escalando en ventas': ['TRL 9 - Sistema real probado en un entorno operacional real']
}

# Función para obtener la categoría de homologación en función del TRL
def obtener_categoria_trl(trl_descripcion):
    for categoria, trls in homologacion_trl.items():
        if trl_descripcion in trls:
            return categoria
    return None  # Cambiado de 'No homologado' a None para mantener el nivel original si no coincide

# Aplicar la función para obtener la categoría del TRL alcanzado (columna C) y esperado (columna E)
df['Categoria alcanzado'] = df['Nivel de desarrollo alcanzado según ejecutivo'].apply(obtener_categoria_trl)
df['Categoria esperado'] = df['TRL esperado al finalizar el proyecto'].apply(obtener_categoria_trl)

# Si no hay coincidencias en la tabla de homologación, mantén los valores originales
df['Categoria alcanzado'].fillna(df['Nivel de desarrollo alcanzado según ejecutivo'], inplace=True)
df['Categoria esperado'].fillna(df['TRL esperado al finalizar el proyecto'], inplace=True)

# Función para verificar si el TRL alcanzado cumple o supera el TRL esperado
def cumple_trl(categoria_alcanzado, categoria_esperado):
    categorias_ordenadas = list(homologacion_trl.keys())
    if categoria_alcanzado in categorias_ordenadas and categoria_esperado in categorias_ordenadas:
        # Comprobar si la categoría alcanzada está en una posición igual o superior a la esperada
        return categorias_ordenadas.index(categoria_alcanzado) >= categorias_ordenadas.index(categoria_esperado)
    else:
        # Si alguna de las categorías no está en la homologación, se devuelve False
        return False

# Aplicar la función para verificar si el nivel alcanzado cumple o supera el esperado
df['Cumple'] = df.apply(lambda row: cumple_trl(row['Categoria alcanzado'], row['Categoria esperado']), axis=1)

# Análisis: Proyectos que cumplen o no con el TRL esperado
df_aprobar = df[['Código', 'Nivel de desarrollo alcanzado según ejecutivo', 'TRL esperado al finalizar el proyecto', 'Cumple']]

print("\nProyectos que cumplen o no con el TRL esperado:")
print(df_aprobar)

# Gráfico: Proyectos que cumplen o no con el TRL esperado
def generar_grafico_trl(df):
    proyectos_cumplen = df[df['Cumple']].shape[0]
    total_proyectos = df.shape[0]
    
    if total_proyectos > 0:
        labels = ['Cumplen con el TRL esperado', 'No cumplen con el TRL esperado']
        sizes = [proyectos_cumplen, total_proyectos - proyectos_cumplen]
        colors = ['lightgreen', 'lightcoral']
        
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, colors=colors, autopct=lambda p: '{:.1f}%\n({:d})'.format(p, int(p * total_proyectos / 100)),
                startangle=90, shadow=True)
        plt.title('Proyectos que Cumplen/No Cumplen con el TRL Esperado')
        plt.axis('equal')
        plt.show()
    else:
        print("No hay proyectos que analizar.")

# Generar gráfico con los proyectos que cumplen y no cumplen
generar_grafico_trl(df_aprobar)