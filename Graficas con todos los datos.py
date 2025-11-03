import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# 1. Cargar y limpiar datos
# -----------------------------
ruta_archivo = r"dataset\DresdenData\datafrend.csv"
datafred = pd.read_csv(ruta_archivo, sep=",", skipinitialspace=True)
datafred.columns = datafred.columns.str.strip()  # Quitar espacios extra

# Crear columna legible del tipo de muestra si no existe
if 'Sample_Type' not in datafred.columns:
    datafred['Sample_Type'] = datafred['Categoria'].map({
        1: "Bone Marrow (BMD_DD)",
        2: "Peripheral Blood (pB)"
    })

# -----------------------------
# 2. Scatter FS vs SS usando todos los datos
# -----------------------------
plt.figure(figsize=(7,6))
sns.scatterplot(
    data=datafred,
    x='FS', y='SS',
    hue='Sample_Type',
    palette={'Peripheral Blood (pB)': 'blue', 'Bone Marrow (BMD_DD)': 'red'},
    alpha=0.2,  # transparencia para ver densidad real
    s=10        # puntos más pequeños
)
plt.title("FS vs SS (Tamaño vs Granularidad) - Todos los datos")
plt.xlabel("FS (Forward Scatter)")
plt.ylabel("SS (Side Scatter)")
plt.legend(title="Tipo de Muestra")
plt.tight_layout()
plt.show()

# -----------------------------
# 3. Boxplots de marcadores seleccionados
# -----------------------------
marcadores = ['CD34', 'CD13', 'CD33', 'CD45']  # marcadores clave

fig, axes = plt.subplots(1, len(marcadores), figsize=(18,5))
for i, marcador in enumerate(marcadores):
    sns.boxplot(
        data=datafred,
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
# 4. Pairplot personalizado con todos los datos
# -----------------------------
marcadores_pair = ['CD34','CD13','CD33','CD45']
n_marcadores = len(marcadores_pair)

fig, axes = plt.subplots(n_marcadores, n_marcadores, figsize=(12,12))

for i in range(n_marcadores):
    for j in range(n_marcadores):
        if i == j:
            # KDE en diagonal
            sns.kdeplot(
                data=datafred[datafred['Sample_Type']=='Peripheral Blood (pB)'],
                x=marcadores_pair[i],
                fill=True, color='blue', alpha=0.4,
                ax=axes[i,j], label='Sangre'
            )
            sns.kdeplot(
                data=datafred[datafred['Sample_Type']=='Bone Marrow (BMD_DD)'],
                x=marcadores_pair[i],
                fill=True, color='red', alpha=0.4,
                ax=axes[i,j], label='Médula'
            )
            axes[i,j].set_title(f'Distribución {marcadores_pair[i]}')
            axes[i,j].legend()
        elif i > j:
            # Scatter con jitter y transparencia
            for sample_type, color, alpha in [
                ('Peripheral Blood (pB)', 'blue', 0.3),
                ('Bone Marrow (BMD_DD)', 'red', 0.2)
            ]:
                subset = datafred[datafred['Sample_Type']==sample_type]
                jitter_x = subset[marcadores_pair[j]] + np.random.normal(0, 0.05, len(subset))
                jitter_y = subset[marcadores_pair[i]] + np.random.normal(0, 0.05, len(subset))
                axes[i,j].scatter(
                    jitter_x, jitter_y,
                    alpha=alpha, s=8, color=color
                )
            axes[i,j].set_xlabel(marcadores_pair[j])
            axes[i,j].set_ylabel(marcadores_pair[i])
        else:
            # Triángulo superior vacío
            axes[i,j].axis('off')

plt.suptitle("Pairplot de Marcadores Clave - Todos los datos", fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
