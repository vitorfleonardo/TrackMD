import re

def normalize_names(file_path, output_path):
    """Normaliza os nomes mantendo apenas o primeiro nome e gera um novo arquivo."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    new_lines = []
    for line in lines:
        if line.startswith("Autores:") or line.startswith("Revisores:"):
            # Extrai os nomes e mantém apenas o primeiro nome
            key, names = line.split(":", 1)
            names_list = [name.strip() for name in names.split(", ") if name.strip()]  # Remove espaços extras e vazios
            normalized_names = ", ".join([name.split()[0] if name.split() else "" for name in names_list])  # Evita erro
            new_lines.append(f"{key}: {normalized_names}\n")
        else:
            new_lines.append(line)
    
    # Salva o arquivo corrigido
    with open(output_path, "w", encoding="utf-8") as file:
        file.writelines(new_lines)
    
    print(f"Arquivo normalizado salvo em: {output_path}")

# Caminhos dos arquivos de entrada e saída
input_file = "resultado.txt"  # Arquivo original
output_file = "resultado_normalizado.txt"  # Arquivo de saída corrigido

normalize_names(input_file, output_file)
