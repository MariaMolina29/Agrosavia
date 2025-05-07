# ARCHIVO PARA EDITAR UN SOLO TILE - Maria Alejandra Molina Giraldo

import subprocess
import os

def filter_and_check_quality(tile_id, input_fastq1, input_fastq2, output_dir, prefix):
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Paso 1: Filtrar lecturas para el primer archivo de secuencia
    grep_command_1 = f"zcat {input_fastq1} | awk -F ':' '$5 == \"{tile_id.strip(':')}\" {{print $0}}' > {output_dir}/{prefix}patron_1.txt"
    subprocess.run(grep_command_1, shell=True, check=True)
    print(f"Filtrado 1 realizado")
    
    # Paso 2: Filtrar lecturas para el segundo archivo de secuencia
    grep_command_2 = f"zcat {input_fastq2} | awk -F ':' '$5 == \"{tile_id.strip(':')}\" {{print $0}}' > {output_dir}/{prefix}patron_2.txt"
    subprocess.run(grep_command_2, shell=True, check=True)
    print(f"Filtrado 2 realizado")

    # Paso 3: Eliminar el carácter "@" de las lecturas
    sed_command_1 = f"sed -i 's/@//g' {output_dir}/{prefix}patron_1.txt"
    sed_command_2 = f"sed -i 's/@//g' {output_dir}/{prefix}patron_2.txt"
    subprocess.run(sed_command_1, shell=True, check=True)
    subprocess.run(sed_command_2, shell=True, check=True)

    # Paso 4: Extraer los IDs de las lecturas (primera columna)
    awk_command_1 = f"awk '{{print $1}}' {output_dir}/{prefix}patron_1.txt > {output_dir}/{prefix}patron_1_2.txt"
    awk_command_2 = f"awk '{{print $1}}' {output_dir}/{prefix}patron_2.txt > {output_dir}/{prefix}patron_2_2.txt"
    subprocess.run(awk_command_1, shell=True, check=True)
    subprocess.run(awk_command_2, shell=True, check=True)
    print(f"Extracción ID realizado")

    # Paso 5: Filtrar las lecturas correspondientes para el primer archivo 
    
    seqkit_command_1 = f"seqkit grep -f {output_dir}/{prefix}patron_1_2.txt -o {output_dir}/{prefix}1_tiles.fastq {input_fastq1}"
    subprocess.run(seqkit_command_1, shell=True, check=True)
    print(f"Filtrado de {input_fastq1} realizado")

    # Paso 6: Filtrar las lecturas correspondientes para el segundo archivo 
    seqkit_command_2 = f"seqkit grep -f {output_dir}/{prefix}patron_2_2.txt -o {output_dir}/{prefix}2_tiles.fastq {input_fastq2}"
    subprocess.run(seqkit_command_2, shell=True, check=True)
    print(f"Filtrado de {input_fastq2} realizado")

    # Paso 7: FastQC sobre las lecturas filtradas para el primer archivo
    fastqc_command_1 = f"fastqc {output_dir}/{prefix}1_tiles.fastq"
    subprocess.run(fastqc_command_1, shell=True, check=True)

    # Paso 8: FastQC sobre las lecturas filtradas para el segundo archivo
    fastqc_command_2 = f"fastqc {output_dir}/{prefix}2_tiles.fastq"
    subprocess.run(fastqc_command_2, shell=True, check=True)

    print(f"Proceso completado. Resultados de FastQC en {output_dir}/")

#Variables de entrada

tile_id = "2289"  # Este es el ID del tile específico
input_fastq1 = "~/polyg/B028_WT_1_polyg.fq.gz"  # Ruta al archivo 1
input_fastq2 = "~/polyg/B028_WT_2_polyG.fq.gz"  # Ruta al archivo 2
output_dir = "2289"  # Ruta al directorio de salida
prefix = "WT_"  # Prefijo que se usará en los nombres de los archivos de salida

filter_and_check_quality(tile_id, input_fastq1, input_fastq2, output_dir, prefix)
