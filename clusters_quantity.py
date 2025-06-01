import pandas as pd
import matplotlib.pyplot as plt

# Define rutas a tus archivos TSV
file_paths = {
    "WT": "WT_deepbgc/WT_deepbgc.bgc.tsv",
    "24": "24_deepbgc/24_deepbgc.bgc.tsv",
    "34": "34_deepbgc/34_deepbgc.bgc.tsv",
    "58": "58_deepbgc/58_deepbgc.bgc.tsv"
}

# Cargar datos
dfs = {key: pd.read_csv(path, sep='\t') for key, path in file_paths.items()}

# Concatenar y contar clusters por tipo y muestra
all_clusters = pd.concat([df[['product_class']].assign(sample=key) for key, df in dfs.items()])
counts_per_type = all_clusters.groupby(['sample', 'product_class']).size().unstack(fill_value=0)

# Graficar y guardar
ax = counts_per_type.plot(kind='bar', figsize=(10,6))
ax.set_xlabel('Muestra')
ax.set_ylabel('Número de clusters')
ax.set_title('Número de clusters por tipo de producto y muestra')
ax.legend(title='Tipo de producto', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('clusters_por_tipo_producto.png', dpi=300)
plt.close()

# Lista de actividades a evaluar
activities = ['antibacterial', 'antifungal', 'cytotoxic', 'inhibitor']

# Contar clusters por actividad con probabilidad >= 0.5
activity_counts_filtered = {}
for sample, df in dfs.items():
    df_filtered = df[(df[activities] >= 0.5).any(axis=1)]
    counts = (df_filtered[activities] >= 0.5).sum()
    activity_counts_filtered[sample] = counts

activity_counts_df = pd.DataFrame(activity_counts_filtered).T.fillna(0).astype(int)
activity_counts_df = activity_counts_df.loc[(activity_counts_df.sum(axis=1) > 0), :]

# Graficar y guardar
ax = activity_counts_df.plot(kind='bar', figsize=(10,6))
ax.set_xlabel('Muestra')
ax.set_ylabel('Número de clusters con actividad ≥ 0.5')
ax.set_title('Clusters por actividad biológica (≥ 0.5) y muestra')
plt.xticks(rotation=0)
plt.legend(title='Actividad')
plt.tight_layout()
plt.savefig('clusters_por_actividad_05.png', dpi=300)
plt.close()

