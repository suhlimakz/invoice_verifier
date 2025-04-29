import os
import pdfplumber
import pandas as pd 
import re 

pasta_pdfs = "data/notas_fiscais/"
arquivo_excel = "amostra.xlsx"

df_excel = pd.read_excel(arquivo_excel)

def extrair_dados_pdf(caminho_pdf):
  with pdfplumber.open(caminho_pdf) as pdf:
    texto = ''
    for pagina in pdf.pages:
      texto += pagina.extract_text()
      
      cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}',texto)
      valor = re.search(r'Valor\s+Total[^\d]*([\d\.,]+)',texto)
      
      return {
        'arquivo': os.path.basename(caminho_pdf),
        'cnpj': cnpj.group() if cnpj else None,
        'valor': valor.group(1).replace('.','').replace(',','.') if valor else None
      }

resultados = []

for arquivo in os.listdir(pasta_pdfs):
  if arquivo.lower().endswith('.pdf'):
    caminho_pdf = os.path.join(pasta_pdfs, arquivo)
    dados = extrair_dados_pdf(caminho_pdf)
  
    cnpj_existe = dados['cnpj'] in df_excel['CPF/CNPJ Emitente'].astype(str).values if dados['cnpj'] else False
  
    dados['cnpj_no_excel'] = cnpj_existe
    resultados.append(dados)
  
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

df_resultados.to_excel('output/relatorio_comparacao.xlsx',index=False)