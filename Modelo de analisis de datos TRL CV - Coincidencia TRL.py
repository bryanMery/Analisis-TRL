import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo Excel
file_path = r'C:\\Users\\bryan.mery\\Desktop\\Analisis CV  - TRL.xlsx'
sheet_name = 'Consolidado'

# Leer la hoja "Consolidado" del archivo
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Eliminar filas con "No aplica" o "-"
df_filtered = df[~df['¿Cuál es el nivel actual de desarrollo de su propuesta o solución?'].isin(['No aplica', '-'])]
df_filtered = df_filtered[~df_filtered['Nivel actual de TRL'].isin(['No aplica', '-'])]

# Tabla de homologación
homologation_table = {
    'Concepto o idea': ['TRL 1 - Principios básicos estudiados', 'TRL 2 - Concepto tecnológico formulado', 'TRL 3 - Prueba de concepto experimental'],
    'Prototipo': ['TRL 4 -Tecnología validada en laboratorio'],
    'Prototipo Funcional': ['TRL 5 - Tecnología validada en un entorno relevante'],
    'Producto Mínimo Viable': ['TRL 6 - Modelo de sistema / subsistema o demostración de prototipo en un entorno relevante (terreno o espacio)', 'TRL 7 - Demostración del prototipo del sistema'],
    'Producto Funcional': ['TRL 8 - Sistema completo y certificado a través de pruebas y demostraciones'],
    'Escalando en ventas': ['TRL 9 - Sistema real probado en un entorno operacional real']
}

# Función para verificar si coinciden los niveles fila por fila
def check_trl(row):
    nivel_desarrollo = row['¿Cuál es el nivel actual de desarrollo de su propuesta o solución?']
    nivel_trl = row['Nivel actual de TRL']
    trls_permitidos = homologation_table.get(nivel_desarrollo, [])
    return nivel_trl in trls_permitidos

# Aplicar la función a las filas filtradas
df_filtered['Coincide'] = df_filtered.apply(check_trl, axis=1)

# Resumen global: Número de filas y porcentaje de coincidencias
total_filas = len(df_filtered)
filas_que_coinciden = df_filtered['Coincide'].sum()
porcentaje_coincidencia = (filas_que_coinciden / total_filas) * 100

# Mostrar el resumen global
print(f'Total de filas analizadas: {total_filas}')
print(f'Número de filas que coinciden: {filas_que_coinciden}')
print(f'Número de filas que no coinciden: {total_filas - filas_que_coinciden}')
print(f'Porcentaje de coincidencias: {porcentaje_coincidencia:.2f}%')

# Graficar el porcentaje de coincidencia con cantidades
labels = ['Coinciden', 'No coinciden']
sizes = [filas_que_coinciden, total_filas - filas_que_coinciden]
colors = ['skyblue', 'lightcoral']

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=[f'{l} ({s})' for l, s in zip(labels, sizes)], colors=colors, autopct='%1.1f%%', startangle=90)
plt.title('Porcentaje y cantidad de coincidencias TRL por nivel de desarrollo')
plt.axis('equal')  # Asegura que el gráfico sea un círculo

# Mostrar gráfico
plt.show()

# Mostrar 10 filas aleatorias que coinciden
print("\n10 ejemplos que coinciden:")
coinciden = df_filtered[df_filtered['Coincide']].sample(10)
print(coinciden[['¿Cuál es el nivel actual de desarrollo de su propuesta o solución?', 'Nivel actual de TRL']])

# Mostrar 10 filas aleatorias que no coinciden
print("\n10 ejemplos que no coinciden:")
no_coinciden = df_filtered[~df_filtered['Coincide']].sample(10)
print(no_coinciden[['¿Cuál es el nivel actual de desarrollo de su propuesta o solución?', 'Nivel actual de TRL']])
