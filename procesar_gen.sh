#!/bin/bash

# Lista de genes a procesar
#genes=("alsS"  "baeE" "baeD" "baeC" "baeB" "dhbC" "dhbE" "yusV" "gtaB"  "bdhA"  "srfAA" "srfAD" "srfAB" "srfAC")
genes=("dhbA" "dhbF" "dhbB" "dhbD")
# Directorio base con anotaciones
BASE_ANNOT="../../../anotacion"

# Muestras a procesar
BASE_SAMPLE_DIRS=("24" "34" "58" "WT")

# Carpeta base para todos los resultados

for GENE in "${genes[@]}"
do
  echo "=== Procesando gen: $GENE ==="

  # Carpeta para resultados de este gen
  RESULT_DIR="${GENE}"
  mkdir -p "$RESULT_DIR"

  for SAMPLE in "${BASE_SAMPLE_DIRS[@]}"
  do
    echo "Procesando muestra $SAMPLE para el gen $GENE..."

    SAMPLE_DIR="${RESULT_DIR}/${GENE}_${SAMPLE}"
    mkdir -p "$SAMPLE_DIR"
    cd "$SAMPLE_DIR" || exit 1

    # Archivos de entrada
    GFF_IN="${BASE_ANNOT}/${SAMPLE}_resultado_prokka/${SAMPLE}_filtrado.gff"
    FNA_IN="${BASE_ANNOT}/${SAMPLE}_resultado_prokka/${SAMPLE}_filtrado.fna"
    FAA_IN="${BASE_ANNOT}/${SAMPLE}_resultado_prokka/${SAMPLE}_filtrado.faa"

    # 1) Extraer secuencias nucleotídicas con bedtools
    grep -i "$GENE" "$GFF_IN" > "${GENE}_genes_${SAMPLE}.gff"
    bedtools getfasta -fi "$FNA_IN" -bed "${GENE}_genes_${SAMPLE}.gff" -fo "${GENE}_genes_${SAMPLE}.fasta"
    sed -i "s/^>/>${SAMPLE}_/" "${GENE}_genes_${SAMPLE}.fasta"

    # 2) Extraer secuencias proteicas con seqtk
    grep -i "$GENE" "$GFF_IN" | awk '{print $9}' | sed 's/.*ID=\([^;]*\).*/\1/' > gene_ids.txt
    seqtk subseq "$FAA_IN" gene_ids.txt > "${GENE}_proteinas_${SAMPLE}.faa"
    sed -i "s/^>/>${SAMPLE}_/" "${GENE}_proteinas_${SAMPLE}.faa"

    cd - > /dev/null
  done

  # Unir y alinear nucleótidos
  echo "Uniendo secuencias nucleotídicas de $GENE..."
  cat "${RESULT_DIR}/${GENE}"_*/*.fasta > "${RESULT_DIR}/${GENE}_all_samples_nucleotidos.fasta"
  echo "Alineando nucleótidos de $GENE..."
  clustalo -i "${RESULT_DIR}/${GENE}_all_samples_nucleotidos.fasta" -o "${RESULT_DIR}/${GENE}_aligned_nucleotidos.fasta" --threads=8 --force

  # Unir y alinear proteínas
  echo "Uniendo secuencias proteicas de $GENE..."
  cat "${RESULT_DIR}/${GENE}"_*/*.faa > "${RESULT_DIR}/${GENE}_all_samples_proteinas.faa"
  echo "Alineando proteínas de $GENE..."
  clustalo -i "${RESULT_DIR}/${GENE}_all_samples_proteinas.faa" -o "${RESULT_DIR}/${GENE}_aligned_proteinas.faa" --threads=8 --force

  echo "=== Fin procesamiento gen: $GENE ==="
done

echo "Todos los genes procesados."

