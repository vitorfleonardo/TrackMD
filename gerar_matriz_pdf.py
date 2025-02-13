from fpdf import FPDF
import pandas as pd

def parse_result_file(file_path):
    """Lê o arquivo resultado_normalizado.txt e estrutura os dados para a matriz."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    data = {}
    all_contributors = set()
    participation_count = {}
    current_file = ""
    authors = []
    reviewers = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("Arquivo:"):
            if current_file:
                data[current_file] = {name: "A" for name in authors}
                for rev in reviewers:
                    if rev in data[current_file]:
                        data[current_file][rev] = "A/R"
                    else:
                        data[current_file][rev] = "R"
                
                # Atualiza contagem de participação
                for person in authors + reviewers:
                    participation_count[person] = participation_count.get(person, 0) + 1
            
            current_file = line.replace("Arquivo: ", "").strip()
            authors = []
            reviewers = []
        elif line.startswith("Autores:"):
            authors = line.replace("Autores:", "").strip().split(", ")
            all_contributors.update(authors)
        elif line.startswith("Revisores:"):
            reviewers = line.replace("Revisores:", "").strip().split(", ")
            all_contributors.update(reviewers)
    
    if current_file:
        data[current_file] = {name: "A" for name in authors}
        for rev in reviewers:
            if rev in data[current_file]:
                data[current_file][rev] = "A/R"
            else:
                data[current_file][rev] = "R"
        
        # Atualiza contagem de participação
        for person in authors + reviewers:
            participation_count[person] = participation_count.get(person, 0) + 1
    
    return data, sorted(all_contributors), participation_count

def generate_pdf(data, contributors, participation_count, output_path):
    """Gera um PDF com a matriz de autoria e revisão, adicionando total de participações na última linha."""
    pdf = FPDF(orientation='L', unit='mm', format='A4')  # Modo paisagem para melhor ajuste
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(0, 10, "Matriz de Autoria e Revisão", ln=True, align='C')
    pdf.ln(5)
    
    # Manter apenas as colunas desejadas
    valid_contributors = ["Carla", "Davi", "Eduarda", "João", "Renata"]
    contributors = [c for c in contributors if c in valid_contributors]
    
    # Criar DataFrame para manipulação
    df = pd.DataFrame.from_dict(data, orient='index', columns=contributors).fillna("")
    df = df.sort_index()
    
    # Ajustar largura das colunas dinamicamente
    page_width = pdf.w - 20  # Considera margem de 10mm de cada lado
    col_width = page_width / (len(contributors) + 1)
    row_height = 8
    
    # Criar cabeçalho corrigido com célula em branco na primeira posição
    pdf.cell(col_width, row_height, "", border=1, align='C')  # Célula vazia para dobra da tabela
    for header in contributors:
        pdf.cell(col_width, row_height, header, border=1, align='C')
    pdf.ln()
    
    # Adicionar linhas da tabela
    for index, row in df.iterrows():
        pdf.cell(col_width, row_height, index, border=1, align='C')  # Nome do arquivo
        for col in contributors:
            value = row[col] if col in row else ""
            pdf.cell(col_width, row_height, value if value else "", border=1, align='C')
        pdf.ln()
    
    # Adicionar linha de total de participações
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(col_width, row_height, "Total Participações", border=1, align='C')
    for col in contributors:
        pdf.cell(col_width, row_height, str(participation_count.get(col, 0)), border=1, align='C')
    pdf.ln()
    
    pdf.output(output_path)
    print(f"PDF salvo em: {output_path}")

def main():
    # Caminho do arquivo de entrada
    input_file = "resultado_normalizado.txt"
    output_pdf = "matriz_autoria_revisao.pdf"
    
    # Processar dados
    data, contributors, participation_count = parse_result_file(input_file)
    
    # Gerar PDF
    generate_pdf(data, contributors, participation_count, output_pdf)

if __name__ == "__main__":
    main()