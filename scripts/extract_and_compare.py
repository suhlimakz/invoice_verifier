import os
import pdfplumber
import pandas as pd 
import re 

pasta_pdfs = "data/notas_fiscais/"
arquivo_excel = "data/amostra.xlsx"

df_excel = pd.read_excel(arquivo_excel)

def extrair_dados_pdf(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        texto = ''
        for pagina in pdf.pages:
            texto += pagina.extract_text()

        cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto)
        valor = re.search(r'(?i)valor\s+total.*?([\d\.]+\,[\d]{2})', texto)
        data_emissao =  re.search(r'(?i)(data\s+de\s+emiss[aã]o|emiss[aã]o|data\s+da\s+emiss[aã]o)[:\s]*([0-3]?\d/[0-1]?\d/\d{4})',texto)

        return {
            'arquivo': os.path.basename(caminho_pdf),
            'cnpj': cnpj.group() if cnpj else None,
            'valor': float(valor.group(1).replace('.', '').replace(',', '.')) if valor else None,
            'data_emissao': data_emissao.group(2) if data_emissao else None
        }

resultados = []

for arquivo in os.listdir(pasta_pdfs):
  if arquivo.lower().endswith('.pdf'):
    caminho_pdf = os.path.join(pasta_pdfs, arquivo)
    dados = extrair_dados_pdf(caminho_pdf)
  
    cnpj_existe = dados['cnpj'] in df_excel['CPF/CNPJ Emitente'].astype(str).values if dados['cnpj'] else False
    valor_existe = dados['valor'] in df_excel['VALOR NOTA FISCAL'].astype(str).values if dados['valor'] else False
    data_existe = dados['data_emissao'] in df_excel['DATA EMISSÃO'].astype(str).values if dados['data_emissao'] else False
    
    dados['cnpj_no_excel'] = cnpj_existe
    dados['valor_no_excel'] = valor_existe
    dados['data_no_excel'] = data_existe
    
    resultados.append(dados)
  
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

df_resultados.to_excel('output/relatorio_comparacao.xlsx',index=False)