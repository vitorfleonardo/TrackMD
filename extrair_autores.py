import os
import re
import markdown
from bs4 import BeautifulSoup

def find_markdown_files(directory):
    """Encontra todos os arquivos .md dentro de /docs."""
    md_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_authors_and_reviewers(md_file):
    """Extrai os autores e revisores do histórico de versão de um arquivo markdown."""
    with open(md_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Converte markdown para HTML para facilitar a extração
    html_content = markdown.markdown(content, extensions=["extra", "tables"])
    soup = BeautifulSoup(html_content, "html.parser")
    
    authors, reviewers = set(), set()
    
    # Procura tabelas dentro do histórico de versão
    version_section = soup.find_all("table")
    for table in version_section:
        rows = table.find_all("tr")[1:]  # Ignora o cabeçalho
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 6:
                author = columns[3].get_text(strip=True)
                reviewer = columns[5].get_text(strip=True)
                if author:
                    authors.add(author)
                if reviewer:
                    reviewers.add(reviewer)
    
    return list(authors), list(reviewers)

def main():
    repo_directory = "/home/feijo/Documents/2024.2-Bluesky/req-grupo1/docs"  # Caminho correto
    md_files = find_markdown_files(repo_directory)
    
    results = []
    output_file = "resultado.txt"
    
    with open(output_file, "w", encoding="utf-8") as f:
        for md_file in md_files:
            authors, reviewers = extract_authors_and_reviewers(md_file)
            result = {
                "file": os.path.basename(md_file),
                "authors": authors,
                "reviewers": reviewers
            }
            results.append(result)
            
            # Escrever no arquivo txt
            f.write(f"Arquivo: {result['file']}\n")
            f.write(f"Autores: {', '.join(result['authors'])}\n")
            f.write(f"Revisores: {', '.join(result['reviewers'])}\n")
            f.write("-" * 40 + "\n")
    
    print(f"Resultados salvos em {output_file}")

if __name__ == "__main__":
    main()
