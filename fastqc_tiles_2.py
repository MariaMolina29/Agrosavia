#ARCHIVO PARA COMBINAR LOS PATRONES HECHOS Y FILTRAR DE LAS SEC'S (PASO 2) - Maria Alejandra Molina Giraldo
import subprocess
import os

def combine_patterns(tile_range, output_dir, prefix):
    # Crear archivos combinados de patrones
    combined_patron_1 = os.path.join(output_dir, f"{prefix}combined_patron_1_2.txt")
    combined_patron_2 = os.path.join(output_dir, f"{prefix}combined_patron_2_2.txt")
    
    # Inicializar los archivos combinados
    with open(combined_patron_1, 'w') as out_1, open(combined_patron_2, 'w') as out_2:
        for tile_id in range(tile_range[0], tile_range[1] + 1):
            tile_id_str = str(tile_id)
            
            # Leer los archivos de patrones específicos de cada tile y combinar
            patron_1 = os.path.join(output_dir, f"{prefix}{tile_id_str}_patron_1_2.txt")
            patron_2 = os.path.join(output_dir, f"{prefix}{tile_id_str}_patron_2_2.txt")
            
            # Agregar los contenidos de los archivos de patrones a los combinados
            with open(patron_1, 'r') as f1:
                out_1.write(f1.read())
            with open(patron_2, 'r') as f2:
                out_2.write(f2.read())

    print(f"Archivos de patrones combinados: {combined_patron_1} y {combined_patron_2}")
    return combined_patron_1, combined_patron_2

def filter_and_check_quality(tile_range, input_fastq1, input_fastq2, output_dir, prefix):
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Paso 1: Combinar todos los archivos de patrones
    combined_patron_1, combined_patron_2 = combine_patterns(tile_range, output_dir, prefix)

    # Paso 2: Filtrar las lecturas correspondientes para el primer archivo usando el archivo combinado
    seqkit_command_1 = f"seqkit grep -f {combined_patron_1} -o {output_dir}/{prefix}1_2_tiles.fastq {input_fastq1}"
    subprocess.run(seqkit_command_1, shell=True, check=True)
    print(f"Filtrado de {input_fastq1} realizado")

    # Paso 3: Filtrar las lecturas correspondientes para el segundo archivo usando el archivo combinado
    seqkit_command_2 = f"seqkit grep -f {combined_patron_2} -o {output_dir}/{prefix}2_2_tiles.fastq {input_fastq2}"
    subprocess.run(seqkit_command_2, shell=True, check=True)
    print(f"Filtrado de {input_fastq2} realizado")

    # Paso 4: Ejecutar FastQC sobre las lecturas filtradas para el primer archivo
    fastqc_command_1 = f"fastqc {output_dir}/{prefix}1_2_tiles.fastq -o ./fastqc_output"
    subprocess.run(fastqc_command_1, shell=True, check=True)

    # Paso 5: Ejecutar FastQC sobre las lecturas filtradas para el segundo archivo
    fastqc_command_2 = f"fastqc {output_dir}/{prefix}2_2_tiles.fastq -o ./fastqc_output"
    subprocess.run(fastqc_command_2, shell=True, check=True)

    print(f"FastQC completado para ambos archivos. Resultados en {output_dir}/")

# Variables de entrada
tile_range = (2383, 2403)  # Rango de tiles
input_fastq1 = "~/polyg/B028_58_1_polyg.fq.gz"  # Ruta al archivo 1
input_fastq2 = "~/polyg/B028_58_2_polyG.fq.gz"  # Ruta al archivo 2
output_dir = "tiles_rango"  # Ruta al directorio de salida
prefix = "58_"  # Prefijo que se usará en los nombres de los archivos de salida

# Filtrar las lecturas y ejecutar FastQC
filter_and_check_quality(tile_range, input_fastq1, input_fastq2, output_dir, prefix)