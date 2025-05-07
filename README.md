# Agrosavia
Archivos que usé en la pasantía en Bioinformática para hacer un análisis de calidad de las secuencias. 
### Flujo.ipynb
Análisis de calidad de subsecuencias (Trimmomatic, TrimGalore, FastQC, Fastp, Lighter, Kraken2)
### filter_ID_per_tile.py
Identifica las lecturas que están asociadas al tile # para poderlas analizar en un FastQC aparte y más detallado (FastQC, seqkit, awk) en secuencias pareadas
### identificar_ID_1.py
Identifica todos las lecturas que están asociadas a un rango de tiles. Es el primer paso donde se guardan los patrones en secuencias pareadas.
### fastqc_tiles_2.py
Crea un FastQC de un rango de tiles continuo para verlo más detallado en secuencias pareadas.
