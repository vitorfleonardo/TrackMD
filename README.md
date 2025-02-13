# TrackMD
Script para gerar um PDF com as participações de cada integrante no projeto todo. Lebrem-se de ajustar os endereços de diretorórios e nomes de integrantes em cada script.

## Configurando ambiente

No terminal, navegue até sua pasta do projeto e depois crie e ative um ambiente virtual:

```
python3 -m venv venv
source venv/bin/activate  # Para Linux/macOS
```

Instale a biblioteca beatifulsoup4:

```
pip install markdown beautifulsoup4
```

Inicie o ambiente virtual:

```
source venv/bin/activate 
```

## Script para pegar as participações em cada arquivo .md do projeto

Rode o script:

```
python extrair_autores.py
```

Ao rodar o script, ele vai extrair o nome do arquivo, nome dos autores e revisores de cada arquivo dentro de /docs, gerando ao final um TXT para você. 

## Script para normalizar os nomes

Agora para formatar os nomes tem esse script:

```
python normalizar_nomes.py
```

Agora esse novo arquivo gerado contém as mesmas informações que o outro mas com apenas o nome de cada um dos integrantes, sem seus sobrenomes. 


## Script para gerar o PDF em formato de tabela

Rode o script:

```
python gerar_matriz_pdf.py
```
