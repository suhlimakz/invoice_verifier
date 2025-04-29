import os
import pdfplumber
import pandas as pd 
import re 
from datetime import datetime

pasta_pdfs = "data/notas_fiscais/"
arquivo_excel = "data/amostra.xlsx"

df_excel = pd.read_excel(arquivo_excel)


def extrair_data(texto):
    # Defina uma lista de palavras-chave relacionadas à data
    palavras_chave = ['data de emissão', 'emissão', 'data da emissão']

    # Converter o texto para minúsculas para facilitar a busca
    texto_lower = texto.lower()

    # Procurar pelas palavras-chave
    for chave in palavras_chave:
        pos = texto_lower.find(chave)
        
        if pos != -1:  # Se a palavra-chave foi encontrada
            # Pega a parte do texto que segue a palavra-chave
            substring = texto[pos + len(chave):]
            
            # Tenta extrair uma data que esteja no formato dd/mm/yyyy
            for palavra in substring.split():
                try:
                    # Garantir que a palavra seja tratada como string antes de tentar a conversão
                    data_extraida = datetime.strptime(str(palavra), '%d/%m/%Y').date()
                    print(f"Data extraída: {data_extraida}")
                    data_brasileira = data_extraida.strftime('%d/%m/%Y')
                    return data_brasileira
                except ValueError:
                    continue  # Se não for uma data, continue procurando

    return None

def extrair_valor(texto):
    valor_match = re.search(r'(?i)valor\s+total.*?([\d\.]+\,[\d]{2})', texto)
    if valor_match:
        valor_bruto = valor_match.group(1)
        valor_limpo = valor_bruto.replace('.', '').replace(',', '.')
        try:
            valor_extraido = float(valor_limpo)
            print(f"Valor extraído: {valor_extraido}") 
            return float(valor_limpo)
        except ValueError:
            print("Erro ao converter o valor para float")
            return None
    return None
  
def extrair_cnpj(texto):
    match = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto)
    if match:
        cnpj = match.group()
        print(f"CNPJ extraído: {cnpj}")
        return cnpj
    return None

def extrair_dados_pdf(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        texto = ''
        for pagina in pdf.pages:
            texto += pagina.extract_text()

        texto = re.sub(r'\s+', ' ', texto)
      
        cnpj_extraido_nf = extrair_cnpj(texto)
        valor_extraido_nf = extrair_valor(texto)
        data_extraida_nf=  extrair_data(texto)

        return {
          'arquivo': os.path.basename(caminho_pdf),
          'cnpj': cnpj_extraido_nf,
          'valor_nf': valor_extraido_nf,
          'data_nf': data_extraida_nf
        }
resultados = []

for arquivo in os.listdir(pasta_pdfs):
  if arquivo.lower().endswith('.pdf'):
    caminho_pdf = os.path.join(pasta_pdfs, arquivo)
    dados = extrair_dados_pdf(caminho_pdf)
    
    df_excel['VALOR NOTA FISCAL'] = df_excel['VALOR NOTA FISCAL'].apply(lambda x: float(str(x).replace(',', '.').replace(' ', '')) if isinstance(x, str) else x)
    
    df_excel['VALOR NOTA FISCAL'] = df_excel['VALOR NOTA FISCAL'].apply(lambda x: round(x, 2))
     
    valor_pdf = dados['valor_nf']

    valor_exato = valor_pdf in df_excel['VALOR NOTA FISCAL'].values if valor_pdf is not None else False
    valor_aproximado = any(
        abs(valor_pdf - x) < 0.01 for x in df_excel['VALOR NOTA FISCAL'].dropna()
    ) if valor_pdf is not None else False
    

    cnpj_existe = dados['cnpj'] in df_excel['CPF/CNPJ Emitente'].astype(str).values if dados['cnpj'] else False
    data_pdf = None
    if dados['data_nf']:
        try:
            data_pdf = datetime.strptime(dados['data_nf'], '%d/%m/%Y').date()
        except ValueError:
            print(f"Data inválida no PDF: {dados['data_nf']}")

    if not pd.api.types.is_datetime64_any_dtype(df_excel['DATA EMISSÃO']):
        df_excel['DATA EMISSÃO'] = pd.to_datetime(df_excel['DATA EMISSÃO'], dayfirst=True).dt.date

    data_existe = any(data_pdf == data for data in df_excel['DATA EMISSÃO'] if pd.notnull(data)) if data_pdf else False


    dados['cnpj_no_excel'] = cnpj_existe
    dados['valor_no_excel'] = valor_exato
    dados['valor_diferenca_ate_0_01'] = not valor_exato and valor_aproximado
    dados['data_no_excel'] = data_existe
    
    resultados.append(dados)
  
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

df_resultados.to_excel('output/relatorio_comparacao.xlsx',index=False)
