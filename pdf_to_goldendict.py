"""
Conversor de Dicionários em PDF para StarDict (GoldenDict)
Script desenvolvido para análise de conteúdo e estruturação de bases de dados textuais.
"""

import os
import re
import subprocess
import pandas as pd
from pypdf import PdfReader

# ==========================================
# CONFIGURAÇÕES
# ==========================================
# O script pergunta ao usuário qual o PDF e a página de início
PDF_PATH = input("Digite o nome exato do arquivo PDF (ex: meu_livro.pdf): ")
pagina_input = input("Em qual página começam os verbetes de fato? (ex: 28): ")
PAGINA_INICIAL_VERBETES = int(pagina_input)

# O Python cria os nomes de saída automaticamente tirando o ".pdf"
NOME_BASE = PDF_PATH.replace(".pdf", "").replace(".PDF", "")
TSV_OUTPUT = f"{NOME_BASE}_Formatado.tsv"
DICT_NAME = f"{NOME_BASE}_GoldenDict"

def extrair_texto_pdf(caminho_pdf, pagina_inicial):
    """Lê o PDF e extrai o texto a partir da página onde começam os verbetes."""
    print("Lendo o PDF...")
    reader = PdfReader(caminho_pdf)
    paginas = []
    
    for i in range(pagina_inicial, len(reader.pages)):
        texto = reader.pages[i].extract_text()
        if texto:
            paginas.append(texto)
            
    return "\n".join(paginas)

def is_meta_line(s):
    """Verifica se a linha é uma assinatura gramatical ou etimológica oficial do dicionário."""
    s = s.strip()
    return (
        re.match(r'^\(?(loc\.|s\.|adj\.|adv\.|v\.)', s, re.I) is not None
        or re.match(r'^Etim\.?', s, re.I) is not None
        or re.match(r'^\d{4}(?:-\d{2,4})?\s+Dados biográficos', s, re.I) is not None
    )

def is_valid_term(s):
    """Filtra ruídos e garante que a linha tem formato de um cabeçalho de verbete."""
    s = s.strip()
    if len(s) < 2 or len(s) > 80: return False
    if s.endswith((".", ":", ";", ",")): return False
    if s.lower() in ["índice", "agradecimentos", "comunicacao", "comunicação", "bibliografia"]: return False
    if "Compre agora e leia" in s: return False # Propaganda comum em PDFs digitais
    return True

def limpar_e_estruturar_verbetes(texto_bruto):
    """Aplica regras de extração e Expressões Regulares para separar os verbetes."""
    print("Processando e estruturando os verbetes...")
    
    # Limpeza de numeração de páginas perdidas no OCR
    linhas = [ln.strip() for ln in texto_bruto.splitlines()]
    linhas = [ln for ln in linhas if ln and not re.fullmatch(r"\d+", ln)]

    entries = []
    current_term = None
    current_buffer = []

    i = 0
    while i < len(linhas) - 1:
        line = linhas[i]
        next_line = linhas[i + 1]

        # Detecta um novo verbete: termo válido + marcador de dicionário logo em seguida
        if is_valid_term(line) and is_meta_line(next_line):
            if current_term is not None:
                entries.append({
                    "termo": current_term,
                    "definicao": " ".join(current_buffer).strip()
                })
            current_term = line
            current_buffer = [next_line]
            i += 2
            continue

        if current_term is not None:
            current_buffer.append(line)
        i += 1

    # Adiciona o último verbete da varredura
    if current_term is not None:
        entries.append({
            "termo": current_term,
            "definicao": " ".join(current_buffer).strip()
        })

    df = pd.DataFrame(entries)
    
    # Tratamento de dados (Data Cleaning)
    df = df.drop_duplicates(subset=["termo"], keep="last").copy()
    df = df[~df["termo"].str.lower().isin(["temas próximos", "temas correlatos", "ver também"])]
    
    df["definicao"] = (
        df["definicao"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace("", "", regex=False)
        .str.replace(r"\bEtim\s*\.", "Etim.", regex=True)
    )
    
    # Estruturação HTML para interface visual no GoldenDict
    df["html"] = (
        '<h3 style="color:#2c3e50; font-family:sans-serif; margin-bottom:5px;">' 
        + df["termo"] + 
        '</h3>'
        '<div style="font-family:serif; font-size:14px; line-height:1.5;">' 
        + df["definicao"] + 
        '</div>'
    )
    
    return df

def exportar_para_tsv(df, caminho_saida):
    """Salva os dados no formato TSV aceito pelo PyGlossary."""
    print(f"Exportando {len(df)} verbetes formatados...")
    df[["termo", "html"]].to_csv(caminho_saida, sep="\t", index=False, header=False, encoding="utf-8")

def compilar_stardict(tsv_path, dict_name):
    """Usa o PyGlossary em linha de comando para converter para o GoldenDict."""
    print("Convertendo banco de dados para formato StarDict...")
    ifo_path = f"{dict_name}.ifo"
    
    comando = [
        "pyglossary", tsv_path, ifo_path,
        "--read-format=Tabfile",
        "--write-format=Stardict",
        "--source-lang=pt",
        "--target-lang=pt"
    ]
    
    try:
        subprocess.run(comando, check=True)
        print(f"Sucesso! Arquivos do dicionário criados ({dict_name}.ifo, .idx, .dict).")
    except Exception as e:
        print(f"Erro na conversão: {e}\nCertifique-se de que o PyGlossary está instalado.")

# ==========================================
# EXECUÇÃO DO FLUXO
# ==========================================
if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        print(f"ERRO: Coloque o arquivo '{PDF_PATH}' na mesma pasta que o script.")
    else:
        texto = extrair_texto_pdf(PDF_PATH, PAGINA_INICIAL_VERBETES)
        df_verbetes = limpar_e_estruturar_verbetes(texto)
        exportar_para_tsv(df_verbetes, TSV_OUTPUT)
        compilar_stardict(TSV_OUTPUT, DICT_NAME)
