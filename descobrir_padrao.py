"""
Lupa de Diagnóstico de Dicionários em PDF
Use este script para ver como o texto do seu PDF está sendo extraído pela máquina.
Isso ajudará você a descobrir qual padrão (Regex) usar na função is_meta_line do script principal.
"""

from pypdf import PdfReader

PDF_PATH = input("Digite o nome do seu PDF: ")
TEST_PAGE = int(input("Digite o número de uma página que tenha uns 3 ou 4 verbetes: "))

print("\n" + "="*50)
print("COMO O ROBÔ ENXERGA O SEU PDF:")
print("="*50 + "\n")

reader = PdfReader(PDF_PATH)
# Extrai a página solicitada e a seguinte para garantir que pegamos texto suficiente
texto = reader.pages[TEST_PAGE].extract_text()
texto += "\n" + reader.pages[TEST_PAGE+ 1].extract_text()

# Imprime as primeiras 60 linhas numeradas para o usuário analisar
linhas = [ln.strip() for ln in texto.splitlines() if ln.strip()]

for i, linha in enumerate(linhas[:60]):
    print(f"Linha {i:02d} | {linha}")

print("\n" + "="*50)
print("DICA DE ANÁLISE:")
print("Olhe as linhas acima. Encontre onde está o nome do verbete.")
print("O que está escrito exatamente na linha DEBAIXO do nome do verbete?")
print("É isso que você deve colocar na função 'is_meta_line' do script principal!")