import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Cargar el dataset ===
df = pd.read_csv(r"dataset/MarburgData/02BM_vs_leukemia/datafrend2.csv")

# === 2. Confirmar categorías detectadas ===
print("Tipos de muestra detectados:", df["Sample_Type"].unique())

# === 3. Seleccionar los marcadores de interés ===
marcadores = ['CD34', 'CD13', 'CD33', 'CD45', 'CD56', 'CD117', 'HLA_DR']

# === 4. Calcular los promedios de cada marcador por tipo de muestra ===
promedios = df.groupby("Sample_Type")[marcadores].mean()

# === 5. Crear el heatmap ===
plt.figure(figsize=(8, 6))
sns.heatmap(promedios, annot=True, fmt=".2f", cmap="mako", cbar_kws={'label': 'Expresión media'})
plt.title("Comparación de expresión media de marcadores: BM vs Leucemia", fontsize=14)
plt.xlabel("Marcadores")
plt.ylabel("Tipo de muestra")

plt.tight_layout()
plt.show()
