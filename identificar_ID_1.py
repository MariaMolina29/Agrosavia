#ARCHIVO PARA FILTRAR LOS IDENTIFICADORES DE LOS RANGOS DE TILES (PASO 1) - Maria Alejandra Molina Giraldo
import subprocess
import os

def filter_and_check_quality(tile_range, input_fastq1, input_fastq2, output_dir, prefix):
    # Crear el directorio de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterar sobre el rango de tiles
    for tile_id in range(tile_range[0], tile_range[1] + 1):
        print(f"Procesando tile {tile_id}")
        
        # Convertir tile_id a string para usarlo en los comandos
        tile_id_str = str(tile_id)

        # Paso 1: Filtrar lecturas para el primer archivo de secuencia
        grep_command_1 = f"zcat {input_fastq1} | awk -F ':' '$5 == \"{tile_id_str}\" {{print $0}}' > {output_dir}/{prefix}{tile_id_str}_patron_1.txt"
        subprocess.run(grep_command_1, shell=True, check=True)
        print(f"Filtrado 1 para tile {tile_id_str} realizado")

        # Paso 2: Filtrar lecturas para el segundo archivo de secuencia
        grep_command_2 = f"zcat {input_fastq2} | awk -F ':' '$5 == \"{tile_id_str}\" {{print $0}}' > {output_dir}/{prefix}{tile_id_str}_patron_2.txt"
        subprocess.run(grep_command_2, shell=True, check=True)
        print(f"Filtrado 2 para tile {tile_id_str} realizado")

        # Paso 3: Eliminar el carácter "@" de las lecturas
        sed_command_1 = f"sed -i 's/@//g' {output_dir}/{prefix}{tile_id_str}_patron_1.txt"
        sed_command_2 = f"sed -i 's/@//g' {output_dir}/{prefix}{tile_id_str}_patron_2.txt"
        subprocess.run(sed_command_1, shell=True, check=True)
        subprocess.run(sed_command_2, shell=True, check=True)
        print(f"Eliminación de '@' para tile {tile_id_str} realizada")

        # Paso 4: Extraer los IDs de las lecturas (primera columna)
        awk_command_1 = f"awk '{{print $1}}' {output_dir}/{prefix}{tile_id_str}_patron_1.txt > {output_dir}/{prefix}{tile_id_str}_patron_1_2.txt"
        awk_command_2 = f"awk '{{print $1}}' {output_dir}/{prefix}{tile_id_str}_patron_2.txt > {output_dir}/{prefix}{tile_id_str}_patron_2_2.txt"
        subprocess.run(awk_command_1, shell=True, check=True)
        subprocess.run(awk_command_2, shell=True, check=True)
        print(f"Extracción de IDs para tile {tile_id_str} realizada")


# Variables de entrada

tile_range = (2383, 2403)#rango de tiles 
input_fastq1 = "~/polyg/B028_58_1_polyg.fq.gz"  # Ruta al archivo 1
input_fastq2 = "~/polyg/B028_58_2_polyG.fq.gz"  # Ruta al archivo 2
output_dir = "tiles_rango"  # Ruta al directorio de salida
prefix = "58_"  # Prefijo que se usará en los nombres de los archivos de salida

filter_and_check_quality(tile_range, input_fastq1, input_fastq2, output_dir, prefix)