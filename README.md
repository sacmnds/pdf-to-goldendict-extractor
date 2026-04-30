# 📚 pdf-to-goldendict-extractor -> Pipeline de Extração Lexical

Este repositório contém um conjunto de scripts em Python para transformar dicionários, enciclopédias e glossários PDF em arquivos de banco de dados interativos (`.dict`, `.idx`, `.ifo`) para leitura no software **GoldenDict**.
Foi desenvolvido como parte da minha pesquisa metodológica de tcc. O intuito era que eu pudesse formartar diversas obras a fim de ver definições para um mesmo conceito de diferentes autores, além de checar jargões, nomes de referência e conceitos teóricos, mesmo que eu não tivesse acesso à internet.

## 🗂️ Arquivos do Projeto

* `pdf_to_goldendict.py`: O script principal. Ele varre o PDF usando uma "janela deslizante", limpa o texto, injeta formatação HTML e usa o PyGlossary para gerar o arquivo final.
* `descobrir_padrao.py`: Uma ferramenta de diagnóstico ("lupa") para ajudar o pesquisador a descobrir como o texto do PDF está estruturado antes da extração.
* `requirements.txt`: Lista de bibliotecas necessárias (`pypdf`, `pandas`, `pyglossary`).

## ☁️ Como usar (Via Google Colab - Sem instalar nada)

Apesar de colocar esse arquivo no Github, sei que talvez vc que precisa dele pode não saber programar ou não quer instalar o Python no seu computador caso ele seja uma torradeira. Se for esse o caso, você pode rodar este projeto direto no navegador usando o Google Colab.

1. Abra o [Google Colab](https://colab.research.google.com/).
2. Crie um "Novo Notebook".
3. Faça o upload do seu PDF e dos scripts deste repositório na aba de arquivos (ícone de pasta na lateral esquerda).
4. Em uma célula de código, instale as dependências:
   ```python
   !pip install -r requirements.txt
   ```

### Passo 1: Diagnóstico (Reconhecimento do Terreno)
Cada livro tem uma diagramação diferente. O robô precisa saber como o autor separa o "Nome do Verbete" do "Texto da Definição" (ex: ele usa *s.m.*? Usa *Etim.*? Usa *[Subst]*?).

Rode o script de diagnóstico para ver como o algoritmo enxerga o seu PDF:
```python
!python descobrir_padrao.py
```
*Ele vai imprimir as linhas do livro na tela. Anote qual é a palavra ou sigla que sempre aparece logo abaixo do nome do verbete.*

### Passo 2: Calibragem (Ajustando a Regex)
Abra o arquivo `pdf_to_goldendict.py` (dando dois cliques nele no Colab) e vá até a função `is_meta_line(s)`. 
Modifique as Expressões Regulares (`re.match`) para incluir a sigla que você descobriu no Passo 1. 

*(O script já vem configurado para um "Dicionário de Comunicação" aí).*

### Passo 3: Extração e Conversão
Rode o script principal:
```python
!python pdf_to_goldendict.py
```
O script vai gerar três arquivos (`.ifo`, `.idx`, e `.dict`). Baixe os três, coloque em uma pasta no seu computador e adicione essa pasta nas configurações do seu aplicativo **GoldenDict**, como faria normalmente com outro dicionário já formatado. 

Pronto! Agora você tem o dicionário offline e com busca instantânea. 

Qualquer erro, bug, ou otimização, entre em contato: sacmnds@gmail.com
