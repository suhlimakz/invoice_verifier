import os
import pdfplumber
import pandas as pd 
import re 

pasta_pdfs = "data/notas_fiscais/"
arquivo_excel = "data/amostra.xlsx"

df_excel = pd.read_excel(arquivo_excel)

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

def extrair_dados_pdf(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        texto = ''
        for pagina in pdf.pages:
            texto += pagina.extract_text()

        texto = re.sub(r'\s+', ' ', texto)
      
        cnpj = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', texto)
        valor_extraido_nf = extrair_valor(texto)
        data_emissao =  re.search(r'(?i)(data\s+de\s+emiss[aã]o|emiss[aã]o|data\s+da\s+emiss[aã]o)[:\s]*([0-3]?\d/[0-1]?\d/\d{4})',texto)

        return {
            'arquivo': os.path.basename(caminho_pdf),
            'cnpj': cnpj.group() if cnpj else None,
            'valor_nf': valor_extraido_nf,
            'data_emissao': data_emissao.group(2) if data_emissao else None
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
    data_existe = dados['data_emissao'] in df_excel['DATA EMISSÃO'].astype(str).values if dados['data_emissao'] else False

    dados['cnpj_no_excel'] = cnpj_existe
    dados['valor_no_excel'] = valor_exato
    dados['valor_diferenca_ate_0_01'] = not valor_exato and valor_aproximado
    dados['data_no_excel'] = data_existe
    
    resultados.append(dados)
  
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

df_resultados.to_excel('output/relatorio_comparacao.xlsx',index=False)
