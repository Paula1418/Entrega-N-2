import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === 1. Cargar el dataset ===
df = pd.read_csv(r"dataset/MarburgData/02BM_vs_leukemia/datafrend2.csv")

# === 2. Seleccionar los marcadores de interés ===
marcadores = ['CD34', 'CD13', 'CD33', 'CD45', 'CD56', 'CD117', 'HLA_DR']

# === 3. Calcular el promedio por tipo de muestra ===
promedios = df.groupby("Sample_Type")[marcadores].mean().reset_index()

# === 4. Transformar a formato largo (para usar con seaborn) ===
df_long = promedios.melt(id_vars="Sample_Type",
                         value_vars=marcadores,
                         var_name="Marcador",
                         value_name="Expresión_media")

# === 5. Graficar tipo línea ===
sns.set_theme(style="darkgrid")

plt.figure(figsize=(8, 6))
sns.lineplot(
    data=df_long,
    x="Marcador",
    y="Expresión_media",
    hue="Sample_Type",
    marker="o",
    linewidth=2.5,
    palette={"Bone Marrow (BMD_DD)": "red", "Leukemia": "blue"}
)

# === 6. Personalizar ===
plt.title("Expresión promedio de marcadores: Médula Ósea vs Leucemia", fontsize=14)
plt.xlabel("Marcadores")
plt.ylabel("Nivel de Expresión Promedio")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
