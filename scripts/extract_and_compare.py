import os
import pdfplumber
import pandas as pd 
import re 
from datetime import datetime

pasta_pdfs = "data/notas_fiscais/"
arquivo_excel = "data/excel/amostra.xlsx"

df_excel = pd.read_excel(arquivo_excel)


def extrair_data(texto):
    palavras_chave = ['data de emissão', 'emissão', 'data da emissão']

    texto_lower = texto.lower()

    for chave in palavras_chave:
        pos = texto_lower.find(chave)
        
        if pos != -1: 
            substring = texto[pos + len(chave):]
            
            for palavra in substring.split():
                try:
                    data_extraida = datetime.strptime(str(palavra), '%d/%m/%Y').date()
                    print(f"Data extraída: {data_extraida}")
                    data_brasileira = data_extraida.strftime('%d/%m/%Y')
                    return data_brasileira
                except ValueError:
                    continue 
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
  match = re.search(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b', texto)
  if match:
    cnpj = match.group()
    print(f"CNPJ extraído: {cnpj}")
    return cnpj
  return None

def extrair_numero_serie(texto):
  numero_nf = None
  serie_nf = None

  texto = ' '.join(texto.split())

  match_numero = re.search(r'(?i)(n[ºo]\s*)(\d{3}\.\d{3}\.\d{3})', texto)
  if match_numero:
    numero_nf = match_numero.group(2).replace('.', '')
    print(f"Número da nota: {numero_nf}")

  match_serie = re.search(r'(?i)s[ée]rie\s+(\d{1,4})', texto)
  if match_serie:
    serie_nf = match_serie.group(1)
    print(f"Série da nota: {serie_nf}")

  return numero_nf, serie_nf

def extrair_descricao_produtos_tabela(caminho_pdf):
    with pdfplumber.open(caminho_pdf) as pdf:
        tabelas = []
        for pagina in pdf.pages:
            tabelas.extend(pagina.extract_tables())

    for tabela in tabelas:
        header = tabela[0]
        if any('descrição' in str(c).lower() for c in header):
            indice_desc = [i for i, c in enumerate(header) if 'descrição' in str(c).lower()][0]
            descricoes = []
            for linha in tabela[1:]:
                valor = linha[indice_desc]
                if valor:
                    descricao_texto = valor.replace('\n', ' | ').replace('\r', ' | ').strip()
                    print(f"Descrição extraída: {descricao_texto}")
                    descricoes.append(descricao_texto)
            return descricoes
    return []
  
def extrair_cfop_tabela(caminho_pdf):
    cfops_encontrados = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                for linha in tabela:
                    for i, celula in enumerate(linha):
                        if celula:
                            if re.search(r'\bCFOP\b', celula, re.IGNORECASE):
                                # Encontrou o título da coluna
                                indice_cfop = i
                                break
                    else:
                        continue
                    break
                else:
                    continue

                # Se encontrou o índice, coleta os CFOPs abaixo da linha do cabeçalho
                for linha in tabela[1:]:  # pulando a primeira linha (cabeçalho)
                    if indice_cfop < len(linha):
                        cfop = linha[indice_cfop]
                        if cfop and re.match(r'^\d{4}$', cfop.strip()):
                            cfops_encontrados.append(cfop.strip())
                break  # Já encontrou uma tabela com CFOP, pode sair da página

    if cfops_encontrados:
        cfop_texto = ' | '.join(cfops_encontrados)
        print(f"CFOP(s) extraído(s): {cfop_texto}")
        return cfop_texto

    return None

def extrair_dados_pdf(caminho_pdf):
  with pdfplumber.open(caminho_pdf) as pdf:
    texto = ''
    for pagina in pdf.pages:
        texto += pagina.extract_text()
        
    texto = re.sub(r'\s+', ' ', texto)
  
    numero_estraido_nf, serie_estraida_nf = extrair_numero_serie(texto)
    cnpj_extraido_nf = extrair_cnpj(texto)
    valor_extraido_nf = extrair_valor(texto)
    data_extraida_nf=  extrair_data(texto)
    descricao_produto_extraido_nf = extrair_descricao_produtos_tabela(caminho_pdf)
    cfop_extraido_nf = extrair_cfop_tabela(caminho_pdf)
    
    return {
        'arquivo': os.path.basename(caminho_pdf),
        'numero_nf': numero_estraido_nf,
        'serie_nf': serie_estraida_nf,
        'cnpj': cnpj_extraido_nf,
        'valor_nf': valor_extraido_nf,
        'data_nf': data_extraida_nf,
        'descricao_produto_nf': descricao_produto_extraido_nf,
        'cfop_nf': cfop_extraido_nf
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

    data_existe = any(data == pd.Timestamp(data_pdf) for data in df_excel['DATA EMISSÃO'] if pd.notnull(data)) if data_pdf else False

    numero_existe = dados['numero_nf'] in df_excel['NÚMERO'].astype(str).values if dados.get('numero_nf') else False
    serie_existe = dados['serie_nf'] in df_excel['SÉRIE'].astype(str).values if dados.get('serie_nf') else False
    
    descricao_pdf = str(dados.get('descricao_produto_nf', '')).strip().lower()
    descricao_existe = descricao_pdf in df_excel['DESCRIÇÃO DO PRODUTO / SERVIÇO'].astype(str).str.strip().str.lower().values

    dados['cnpj_no_excel'] = cnpj_existe
    dados['numero_nf_no_excel'] = numero_existe
    dados['serie_nf_no_excel'] = serie_existe
    dados['valor_no_excel'] = valor_exato
    dados['valor_diferenca_ate_0_01'] = not valor_exato and valor_aproximado
    dados['data_no_excel'] = data_existe
    dados['descricao_produto_no_excel'] = descricao_existe
    
    resultados.append(dados)
  
df_resultados = pd.DataFrame(resultados)
print(df_resultados)

#df_resultados.drop(columns=['produtos'], inplace=True)

#df_resultados.to_excel('output/relatorio_comparacao.xlsx',index=False)
