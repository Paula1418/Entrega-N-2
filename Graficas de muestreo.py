import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------
# 1. Cargar y limpiar datos
# -----------------------------
ruta_archivo = r"dataset\DresdenData\datafrend.csv"
datafred = pd.read_csv(ruta_archivo, sep=",", skipinitialspace=True)
datafred.columns = datafred.columns.str.strip()  # Quitar espacios extra

# Crear columna legible de tipo de muestra si no existe
if 'Sample_Type' not in datafred.columns:
    datafred['Sample_Type'] = datafred['Categoria'].map({
        1: "Bone Marrow (BMD_DD)",
        2: "Peripheral Blood (pB)"
    })

# Muestreo para agilizar gráficos grandes
data_sample = datafred.groupby('Sample_Type').apply(
    lambda x: x.sample(min(len(x), 2000), random_state=42)
).reset_index(drop=True)

# -----------------------------
# 2. Scatter FS vs SS
# -----------------------------
plt.figure(figsize=(7,6))
sns.scatterplot(
    data=data_sample,
    x='FS', y='SS',
    hue='Sample_Type',
    palette={'Peripheral Blood (pB)': 'blue', 'Bone Marrow (BMD_DD)': 'red'},
    alpha=0.5, s=20
)
plt.title("FS vs SS (Tamaño vs Granularidad)")
plt.xlabel("FS (Forward Scatter)")
plt.ylabel("SS (Side Scatter)")
plt.legend(title="Tipo de Muestra")
plt.tight_layout()
plt.show()

# -----------------------------
# 3. Boxplots de marcadores
# -----------------------------
marcadores = ['CD34', 'CD13', 'CD33']  # Ejemplo de 3 marcadores importantes

fig, axes = plt.subplots(1, len(marcadores), figsize=(15,5))
for i, marcador in enumerate(marcadores):
    sns.boxplot(
        data=data_sample,
        x='Sample_Type',
        y=marcador,
        palette={'Peripheral Blood (pB)': 'blue', 'Bone Marrow (BMD_DD)': 'red'},
        ax=axes[i]
    )
    axes[i].set_title(f'{marcador} por Tipo de Muestra')
    axes[i].set_xlabel('')
    axes[i].set_ylabel('Expresión')

plt.tight_layout()
plt.show()

# -----------------------------
# 3b. Catplot para todos los marcadores
# -----------------------------
marcadores_all = ['CD34','CD13','CD7','CD33','CD56','CD117','CD45','HLA_DR']

# Transformar a formato "largo" para catplot
data_melt = datafred.melt(
    id_vars=['Sample_Type'],
    value_vars=marcadores_all,
    var_name='Marcador',
    value_name='Expresión'
)

sns.set_theme(style="whitegrid")

g = sns.catplot(
    data=data_melt,
    kind="bar",
    x="Marcador",
    y="Expresión",
    hue="Sample_Type",
    errorbar="sd",
    palette={'Peripheral Blood (pB)': 'blue', 'Bone Marrow (BMD_DD)': 'red'},
    alpha=.7,
    height=6,
    aspect=2
)

# Ajustes visuales
g.despine(top=True)
g.set_axis_labels("Marcador", "Nivel de Expresión")
g.legend.set_title("Tipo de Muestra")
g.legend.set_loc('upper right')
g.set_titles("Comparación de Marcadores entre Sangre Periférica y Médula Ósea")
plt.xticks(rotation=60)
plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# 4. Pairplot de marcadores clave con títulos en la diagonal
# ----------------------------------------------------------
import numpy as np

marcadores_pair = ['CD34', 'CD13', 'CD33', 'CD45']

g = sns.pairplot(
    data=data_sample[marcadores_pair + ['Sample_Type']],
    hue='Sample_Type',
    palette={'Peripheral Blood (pB)': 'blue', 'Bone Marrow (BMD_DD)': 'red'},
    corner=True,
    diag_kind="kde",
    plot_kws={'alpha': 0.5, 's': 20}
)

# Añadir marcos y cuadrículas
for ax in g.axes.flatten():
    if ax is not None:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('black')
            spine.set_linewidth(1.2)
        ax.grid(True, linestyle='--', linewidth=0.4, alpha=0.6, color='gray')

# Títulos en las diagonales
for i, variable in enumerate(marcadores_pair):
    if g.diag_axes is not None and i < len(g.diag_axes):
        ax_diag = g.diag_axes[i]
        ax_diag.set_title(f"Distribución {variable}", fontsize=10, pad=10, fontweight='bold')

# Título general
plt.suptitle("Pairplot de Marcadores Clave con Títulos de Distribución",
             y=1.02, fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
