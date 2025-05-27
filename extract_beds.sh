#!/usr/bin/env bash

# Archivo GFF de entrada y directorio de salida
GFF="../data/24_filtrado.gff"
OUTDIR="data"

# Lista de genes que quieres extraer
genes=("feu" "bae" "sfp" "dhb" "yusV" "yfiY" "sfp" "gtaB" "fetB" "bdhA" "alsD" "srf")

# Asegúrate de que el directorio de salida exista
mkdir -p "${OUTDIR}"

for gene in "${genes[@]}"; do
  # Construye el nombre del archivo BED
  BED="${OUTDIR}/24_${gene}.bed"
  
  # Filtra el GFF por Name=GEN y convierte a BED
  grep -i "Name=${gene}" "${GFF}" | \
    awk 'BEGIN{OFS="\t"}{
      # partes del campo 9 (atributos)
      split($9,a,";")
      name=""
      for(i in a){
        if(a[i] ~ /^Name=/){
          split(a[i],b,"=")
          name=b[2]
        }
      }
      # GFF es 1-based inclusive, BED es 0-based half-open
      print $1, $4-1, $5, name
    }' > "${BED}"
  
  echo "-> generado ${BED}"
done

