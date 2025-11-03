import pandas as pd
import os
from io import StringIO

archivo_numerico = "dataset/DresdenData/01SampleDresdenD10n440K.lrn"
archivo_clases = "dataset/DresdenData/01SampleDresdenN440K.cls"

print("Cargando archivo con nombres de columnas y categorías...")

try:
    # ===========================================================================
    # 1. CARGAR DATOS NUMÉRICOS (archivo .lrn)
    # ===========================================================================

    # Leer todo el archivo .lrn
    with open(archivo_numerico, 'r') as f:
        lineas = f.readlines()

    # Extraer nombres de columnas de la línea 5
    linea_encabezados = lineas[4]  # Línea 5 (índice 4)
    nombres_columnas = linea_encabezados.replace('%', '').strip().split('\t')
    print(f"Nombres de columnas: {nombres_columnas}")

    # Filtrar líneas de datos (saltar líneas 1-5 que son metadatos)
    lineas_datos = lineas[5:]  # Desde la línea 6 en adelante

    print(f"Líneas totales en .lrn: {len(lineas)}")
    print(f"Líneas de datos: {len(lineas_datos)}")

    # Crear DataFrame con nombres de columnas
    datos_texto = ''.join(lineas_datos)
    df_num = pd.read_csv(StringIO(datos_texto), sep="\t", header=None, names=nombres_columnas)

    print("✓ Datos numéricos cargados exitosamente")
    print(f"Dimensiones datos: {df_num.shape}")

    # ===================================================================
    # 2. CARGAR CATEGORÍAS (archivo .cls)
    # ===================================================================

    print(f"\nCargando categorías desde: {archivo_clases}")

    # Leer archivo .cls
    with open(archivo_clases, 'r') as f:
        lineas_cls = [l.strip() for l in f if l.strip() and not l.startswith(('%', '#'))]

    categorias = []

    for linea in lineas_cls:
        partes = linea.split()
        if len(partes) == 1:
            # Solo hay una columna -> usar ese valor
            try:
                categorias.append(int(partes[0]))
            except ValueError:
                pass
        elif len(partes) >= 2:
            # Hay dos o más columnas -> tomar la última (clase)
            try:
                categorias.append(int(partes[-1]))
            except ValueError:
                pass

    print(f"Total categorías leídas: {len(categorias)}")
    print(f"Valores únicos de categoría: {sorted(set(categorias))}")

    # ===========================================================================
    # 3. VERIFICAR Y AGREGAR CATEGORÍAS AL DATAFRAME
    # ===========================================================================

    if len(categorias) == len(df_num):
        # Agregar categorías como nueva columna
        df_num['Categoria'] = categorias
        print(f"✓ Categorías agregadas exitosamente")
        print(f"Dimensiones finales: {df_num.shape}")

        # Agregar columna descriptiva según categoría
        mapeo_categoria = {1: "Bone Marrow (BMD_DD)", 2: "Peripheral Blood (pB)"}
        df_num['Sample_Type'] = df_num['Categoria'].map(mapeo_categoria)

        print("\nPrimeras filas con Sample_Type:")
        print(df_num[['Categoria', 'Sample_Type']].head(10))

        # Mostrar distribución de categorías
        print(f"\nDistribución de categorías:")
        print(df_num['Categoria'].value_counts().sort_index())

    elif len(categorias) > 0:
        print(
            f"⚠ Advertencia: Número de categorías ({len(categorias)}) no coincide con número de filas ({len(df_num)})")
        print("Usando las primeras categorías que coincidan...")
        df_num['Categoria'] = categorias[:len(df_num)]
    else:
        print("✗ No se pudieron extraer categorías del archivo .cls")

    # ===========================================================================
    # 4. MOSTRAR RESULTADO FINAL
    # ===========================================================================

    print(f"\n" + "=" * 60)
    print("DATASET FINAL CON CATEGORÍAS")
    print("=" * 60)
    print(f"Dimensiones: {df_num.shape}")
    print(f"Columnas: {list(df_num.columns)}")
    print(f"\nPrimeras 10 filas del dataset:")
    print(df_num.head(10))

    print(f"\nInformación del dataset:")
    print(df_num.info())

    # Guardar DataFrame completo como CSV
    ruta_salida = "dataset/DresdenData/datafrend.csv"
    df_num.to_csv(ruta_salida, index=False)
    print(f"✓ Dataset guardado como '{ruta_salida}'")

except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()