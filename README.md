# Agrosavia Bioinformatics Pipeline

Este repositorio contiene un conjunto de scripts y notebooks diseñados para el procesamiento, análisis y visualización de datos genómicos y metagenómicos usando diversas herramientas (FastQC, DeepBGC, bedtools, Kraken, Prokka, etc.). A continuación se describe la estructura general del repositorio y el propósito de cada archivo.

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)  
2. [Requisitos](#requisitos)  
3. [Estructura de Carpetas y Archivos](#estructura-de-carpetas-y-archivos)  
   - [Scripts Bash](#scripts-bash)  
   - [Scripts Python](#scripts-python)  
   - [Notebooks (Jupyter)](#notebooks-jupyter)  
---

## Descripción General

Este repositorio agrupa varias etapas de un flujo de trabajo genómico/metagenómico:
- **Filtrado de lecturas por “tiles” de secuenciación** (identificar lecturas según el identificador de “tile” en la cabecera FASTQ).  
- **Análisis de calidad** posterior al filtrado mediante FastQC.  
- **Extracción de regiones de interés** (genes específicos) desde archivos GFF y conversión a formato BED para extraer secuencias con bedtools.  
- **Anotación y reporte de bacterias** (Prokka, Kraken) para caracterización taxonómica y funcional.  
- **Visualización y conteo de clusters de metabolitos/BCG** generados por DeepBGC.  
- **Alineamientos múltiples** de secuencias de genes homólogos extraídos de diferentes muestras.  

---

## Requisitos

Antes de ejecutar los scripts y notebooks, se deben tener instaladas las siguientes herramientas y librerías:

- **Bash utilities**: `grep`, `awk`, `sed`, `bedtools`, `seqtk`, `clustalo`  
- **FastQC** (para control de calidad de lecturas)  
- **Python 3.7+** con las siguientes librerías:
  - `pandas`
  - `matplotlib`
  - `subprocess`
- **SeqKit** (para filtrar FASTQ con listas de IDs)  
- **Prokka** (para anotación de genomas bacterianos)  
- **Kraken2** (para clasificación taxonómica)  
- **Jupyter Notebook** (para abrir y ejecutar los .ipynb)  

---

## Estructura de Carpetas y Archivos

A continuación se listan los archivos principales (en el nivel raíz) y una breve descripción de su contenido.

### Scripts Bash

- **`extract_beds.sh`**  
  - Extrae regiones de genes específicos desde un archivo GFF (`24_filtrado.gff`) y genera archivos BED para cada gen listado.  
  - Uso típico:  
    ```bash
    chmod +x extract_beds.sh
    ./extract_beds.sh
    ```  
  - Genera archivos `.bed` nombrados como `24_<GEN>.bed` dentro de `data/`.

- **`procesar_gen.sh`**  
  - Automatiza el procesamiento de uno o varios genes (`genes=("dhbA" "dhbF" "dhbB" "dhbD")`) para múltiples muestras (`24`, `34`, `58`, `WT`).  
  - Para cada gen, extrae secuencias nucleotídicas y proteicas desde las anotaciones Prokka (`*.gff`, `*.fna`, `*.faa`), las renombra agregando prefijos de muestra, y luego:
    1. Une todas las secuencias nucleotídicas de cada muestra en un solo FASTA.
    2. Alinea dichas secuencias con Clustal Omega (`clustalo`).
    3. Repite lo mismo para las secuencias proteicas.  
  - Uso típico:  
    ```bash
    chmod +x procesar_gen.sh
    ./procesar_gen.sh
    ```  
  - Salidas:
    - Archivos `.gff` por gen y muestra (e.g., `dhbA_genes_24.gff`)
    - FASTA nucleotídico y proteico con prefijo de muestra
    - Alineamientos finales:  
      - `<GEN>_aligned_nucleotidos.fasta`  
      - `<GEN>_aligned_proteinas.faa`

---

### Scripts Python

- **`identificar_ID_1.py`**  
  - Primer paso para filtrar lecturas de un rango de “tiles” en archivos FASTQ comprimidos (`.fq.gz` o `.fastq.gz`).
  - Itera sobre un rango de tiles (`tile_range = (2383, 2403)`) y, para cada tile:
    1. Extrae líneas de FASTQ cuyo identificador de tile coincide (usando `awk` y `zcat`).
    2. Elimina el carácter `@` de las cabeceras.
    3. Guarda los IDs (campo 1) en archivos de texto (`<prefix><tile>_patron_1_2.txt` y `<prefix><tile>_patron_2_2.txt`).
  - Variables configurables (dentro del script):
    - `tile_range`: rango de tiles a procesar.
    - `input_fastq1`, `input_fastq2`: rutas a los archivos FASTQ de lectura 1 y 2.
    - `output_dir`: directorio donde se almacenan los patrones.
    - `prefix`: prefijo para nombrar los archivos de salida.  
  - Uso:  
    ```bash
    python3 identificar_ID_1.py
    ```

- **`filter_ID_per_tile.py`**  
  - Variante para filtrar un solo tile específico (`tile_id = "2289"`).  
  - Pasos:
    1. Filtra lecturas de `tile_id` para cada archivo FASTQ (1 y 2).
    2. Elimina el carácter `@`.
    3. Extrae los IDs y genera archivos de patrones (`<prefix>patron_1_2.txt`, `<prefix>patron_2_2.txt`).
    4. Usa SeqKit para extraer de los FASTQ originales sólo las lecturas cuyos IDs están en la lista de patrones, generando `<prefix>1_tiles.fastq` y `<prefix>2_tiles.fastq`.
    5. Ejecuta FastQC sobre esas lecturas filtradas para obtener reportes de calidad.  
  - Variables configurables:
    - `tile_id`, `input_fastq1`, `input_fastq2`, `output_dir`, `prefix`.  
  - Uso:  
    ```bash
    python3 filter_ID_per_tile.py
    ```

- **`fastqc_tiles_2.py`**  
  - Filtra lecturas de un rango de tiles similar a `identificar_ID_1.py`, pero combina primero todos los patrones de todos los tiles en dos archivos (`combined_patron_1_2.txt`, `combined_patron_2_2.txt`) y luego:
    1. Usa SeqKit para extraer lecturas del rango completo en un solo conjunto (`<prefix>1_2_tiles.fastq` y `<prefix>2_2_tiles.fastq`).
    2. Corre FastQC sobre ambos archivos filtrados.
  - Variables configurables:
    - `tile_range = (2383, 2403)`.
    - `input_fastq1`, `input_fastq2`: archivos FASTQ originales.
    - `output_dir`: directorio de salida donde se generarán los patrones combinados y los FASTQ filtrados.
    - `prefix`: prefijo para los nombres de archivos de salida.
  - Uso:  
    ```bash
    python3 fastqc_tiles_2.py
    ```

- **`clusters_quantity.py`**  
  - Genera gráficos de barras para visualizar:
    1. **Número de clusters por tipo de producto** para muestras `WT`, `24`, `34`, `58`, usando archivos TSV de DeepBGC (`*.bgc.tsv`).
    2. **Número de clusters por actividad biológica** (actividades filtradas con probabilidad ≥ 0.5: `antibacterial`, `antifungal`, `cytotoxic`, `inhibitor`).
  - Leer rutas en el diccionario `file_paths`, donde cada clave corresponde a una muestra y el valor es la ruta al TSV generado por DeepBGC.
  - Salidas:
    - `clusters_por_tipo_producto.png`
    - `clusters_por_actividad_05.png`
  - Requiere:  
    ```python
    import pandas as pd
    import matplotlib.pyplot as plt
    ```  
  - Uso:  
    ```bash
    python3 clusters_quantity.py
    ```

---

### Notebooks (Jupyter)

- **`Flujo.ipynb`**  
  - Notebook que documenta y ejecuta el flujo de trabajo genómico completo: desde la lectura de datos brutos hasta el análisis final.
  - Incluye secciones para cargar datos, ejecutar pasos de filtrado, análisis de calidad y/o anotaciones automáticas.
  - Contiene fragmentos de código Python y/o Bash integrados para ilustrar el pipeline general.

- **`Prokka.ipynb`**  
  - Notebook dedicado a la **anotación de genomas** bacterianos usando Prokka.
  - Pasos típicos:
    1. Llamada a Prokka con parámetros de entrada (genoma en FASTA).
    2. Procesamiento y visualización de resultados (archivos `.gff`, `.fna`, `.faa`).
    3. Extraer estadísticas del proceso (número de genes anotados, RNAs, etc.).
  - Sirve de plantilla para configurar nuevas anotaciones Prokka en diferentes muestras.

- **`Pruebas_secuencias.ipynb`**  
  - Notebook para **pruebas y validación de secuencias** (posiblemente control de calidad, inspección de lecturas FASTQ/FASTA o reconciliación de IDs).
  - Puede incluir visualizaciones adicionales o ejemplos de filtrado de secuencias antes de alimentar herramientas de ensamblaje o anotación.

- **`Reportes_kraken.ipynb`**  
  - Notebook para **generar y visualizar reportes de clasificación taxonómica** usando Kraken2.
  - Pasos comunes:
    1. Cargar archivo de reporte (`*.kraken.report` o similar).
    2. Analizar la distribución taxonómica (phylum, genus, species).
    3. Graficar abundancias relativas o crear tablas de frecuencia de taxa.
  - Útil para inspeccionar resultados de Kraken para cada muestra y generar estadísticas resumidas.

