import os
import pdfplumber
import pandas as pd
import re

def extrair_chave_acesso(texto):

	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		if 'Chave de acesso da NF-e' in linha:
			if i + 1 < len(linhas):
				linha_chave = linhas[i + 1]
				chave = ''.join(c for c in linha_chave if c.isdigit())
				if len(chave) == 45:
					return chave
				else:
					print(f"Aviso: chave encontrada com tamanho diferente de 45 → {chave}")
					return chave
	return None

def extrair_tipo_movimentacao(chave):
  tipo_movimentacao = chave[0]

  if tipo_movimentacao == '0':
    return "Entrada"
  elif tipo_movimentacao == '1':
    return "Saída"
  else:
    print(f"⚠️ Valor inesperado para tipo de movimentação: {tipo_movimentacao}")
    return None

def extrair_uf_emitente(chave):
	chave = ''.join(c for c in chave if c.isdigit())

	if len(chave) != 45:
		print(f"❌ Chave inválida para extrair UF emitente → {chave}")
		return None

	uf_codigo = chave[1:3]

	ufs = {
		'11': 'Rondônia – RO',
		'12': 'Acre – AC',
		'13': 'Amazonas – AM',
		'14': 'Roraima – RR',
		'15': 'Pará – PA',
		'16': 'Amapá – AP',
		'17': 'Tocantins – TO',
		'21': 'Maranhão – MA',
		'22': 'Piauí – PI',
		'23': 'Ceará – CE',
		'24': 'Rio Grande do Norte – RN',
		'25': 'Paraíba – PB',
		'26': 'Pernambuco – PE',
		'27': 'Alagoas – AL',
		'28': 'Sergipe – SE',
		'29': 'Bahia – BA',
		'31': 'Minas Gerais – MG',
		'32': 'Espírito Santo – ES',
		'33': 'Rio de Janeiro – RJ',
		'35': 'São Paulo – SP',
		'41': 'Paraná – PR',
		'42': 'Santa Catarina – SC',
		'43': 'Rio Grande do Sul – RS',
		'50': 'Mato Grosso do Sul – MS',
		'51': 'Mato Grosso – MT',
		'52': 'Goiás – GO',
		'53': 'Distrito Federal – DF'
	}

	uf_nome = ufs.get(uf_codigo)

	if uf_nome:
		uf_sigla = uf_nome.split('–')[-1].strip()
		return uf_sigla
	else:
		print(f"⚠️ Código de UF não encontrado → {uf_codigo}")
		return None

  
def extrair_cnpj_da_chave(chave):
	if chave and len(chave) == 45:
		cnpj_puro = chave[7:21] 
		cnpj_formatado = f'{cnpj_puro[0:2]}.{cnpj_puro[2:5]}.{cnpj_puro[5:8]}/{cnpj_puro[8:12]}-{cnpj_puro[12:14]}'
		return cnpj_formatado
	else:
		print(f"Aviso: chave inválida para extrair CNPJ → {chave}")
		return None

def extrair_serie(chave):
	if chave and len(chave) == 45:
		serie_nf = chave[23:26] 
		return serie_nf
	else:
		print(f"Aviso: chave inválida para extrair SÉRIE NF_e → {chave}")
		return None

def extrair_numero_nf(chave):
	if chave and len(chave) == 45:
		numero_nf = chave[26:35] 
		return numero_nf
	else:
		print(f"Aviso: chave inválida para extrair NÚMERO NF-e → {chave}")
		return None

def extrair_natureza_operacao(texto):
	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		if 'Natureza da Operação' in linha:
			parts = linha.split(':')
			if len(parts) > 1 and parts[1].strip():
				natureza = parts[1].strip()
			else:
				natureza = linhas[i + 1].strip() if i + 1 < len(linhas) else ''

			natureza_limpa = ''
			for palavra in natureza.split():
				if palavra.isdigit() and len(palavra) >= 8:
					break
				if '/' in palavra and palavra.count('/') == 2:
					break
				if ':' in palavra and palavra.count(':') == 2:
					break
				natureza_limpa += palavra + ' '

			return natureza_limpa.strip()

	print("❌ Campo 'Natureza da Operação' não encontrado no texto.")
	return None

def extrair_linha_nome_razao_social_cnpj_cpf_data(texto):
	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		linha_lower = linha.lower().strip()
		if 'nome / razão social' in linha_lower:
			if i + 1 < len(linhas):
				linha_dados = linhas[i + 1].strip()
				return linha_dados
			else:
				print("⚠️ Não há linha abaixo do campo 'Nome / Razão Social'.")
				return None

	print("❌ Campo 'Nome / Razão Social' não encontrado no texto.")
	return None

def extrair_destinatario(linha_dados):
	if linha_dados:
		partes = linha_dados.split()
		nome = []
		for parte in partes:
			if '.' in parte or '/' in parte or '-' in parte and len(parte) >= 11:
				break
			nome.append(parte)
		return ' '.join(nome) if nome else None

	return None

def extrair_cnpj_cpf_destinatario(linha_dados):
	if linha_dados:
		partes = linha_dados.split()
		for parte in partes:
			if parte.count('.') == 2 and '-' in parte:
				return parte
			if parte.count('.') == 2 and '/' in parte and '-' in parte:
				return parte
	return None

def extrair_data_emissao(linha_dados):
	if linha_dados:
		partes = linha_dados.split()
		for parte in partes:
			if '/' in parte and parte.count('/') == 2:
				return parte
	return None

def extrair_municipio_destinatario(texto):
	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		linha_lower = linha.lower()
  # 	⚠️ O cabeçalho no PDF a palavra município está escrita errada, 
  # 	se não encontrar o dado, verifique se a grafia foi corrigida. 
		if 'munícipio' in linha_lower and 'uf' in linha_lower:
			if i + 1 < len(linhas):
				linha_dados = linhas[i + 1].strip()
				partes = linha_dados.split()
				if len(partes) >= 1:
					return partes[0]
				else:
					print("❌ Linha de dados não tem município.")
					return None
			else:
				print("❌ Linha de dados não encontrada após cabeçalho.")
				return None

	print("❌ Cabeçalho com 'Município' e 'UF' não encontrado.")
	return None

def extrair_uf_destinatario(texto):
	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		linha_lower = linha.lower()
		if 'munícipio' in linha_lower and 'uf' in linha_lower:
			if i + 1 < len(linhas):
				linha_dados = linhas[i + 1].strip()
				partes = linha_dados.split()
				if len(partes) >= 3:
					return partes[2]
				else:
					print("❌ Linha de dados não tem UF.")
					return None
			else:
				print("❌ Linha de dados não encontrada após cabeçalho.")
				return None

	print("❌ Cabeçalho com 'Município' e 'UF' não encontrado.")
	return None

def extrair_valor_total_produtos(texto):
	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		linha_lower = linha.lower()
		if 'valor total dos produtos' in linha_lower:
			if i + 1 < len(linhas):
				linha_dados = linhas[i + 1].strip()
				valores = linha_dados.split()
				if valores:
					return valores[-1] 
				else:
					print("❌ Não encontrou valores na linha de dados.")
					return None
			else:
				print("❌ Linha de dados não encontrada após o cabeçalho.")
				return None

	print("❌ Cabeçalho com 'Valor total dos produtos' não encontrado.")
	return None

def extrair_valor_total_descontos(texto):
	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		linha_lower = linha.lower()
		if 'desconto' in linha_lower and 'valor total da nota' in linha_lower:
			if i + 1 < len(linhas):
				linha_dados = linhas[i + 1].strip()
				valores = linha_dados.split()
				if len(valores) >= 3:
					return valores[2]
				else:
					print("❌ Não encontrou valores suficientes na linha de dados.")
					return None
			else:
				print("❌ Linha de dados não encontrada após o cabeçalho.")
				return None

	print("❌ Cabeçalho com 'Desconto' e 'Valor total da Nota' não encontrado.")
	return None

def extrair_valor_total_nota(texto):
	linhas = texto.splitlines()

	for i, linha in enumerate(linhas):
		linha_lower = linha.lower()
		if 'valor total da nota' in linha_lower:
			if i + 1 < len(linhas):
				linha_dados = linhas[i + 1].strip()
				valores = linha_dados.split()
				if valores:
					return valores[-1] 
				else:
					print("❌ Não encontrou valores na linha de dados.")
					return None
			else:
				print("❌ Linha de dados não encontrada após o cabeçalho.")
				return None

	print("❌ Cabeçalho com 'Valor total da Nota' não encontrado.")
	return None

def extrair_tabela_produtos(caminho_pdf):
	produtos = []

	with pdfplumber.open(caminho_pdf) as pdf:
		for pagina in pdf.pages:
			texto = pagina.extract_text()

			if not texto:
				continue

			if 'DADOS DO PRODUTO / SERVIÇO' in texto and 'DADOS ADICIONAIS' in texto:
				bloco = texto.split('DADOS DO PRODUTO / SERVIÇO')[1].split('DADOS ADICIONAIS')[0]
				linhas = bloco.strip().split('\n')

				i = 1
				while i < len(linhas):
					linha = linhas[i]

					if re.match(r'^\d{7}', linha):
						padrao = re.compile(
							r'^(?P<cod_item>\d{7})\s+'
							r'(?P<descricao>.+?)\s+'
							# r'(?P<ncm>\d{4}\.\d{2}\.\d{2})\s+'
							# r'(?P<cst>\d{3})\s+'
							r'(?P<cfop>\d{4})\s+'
							r'(?P<un>\w+)\s+'
							r'(?P<qtde>[\d.,]+)\s+'
							r'(?P<v_unit>[\d.,]+)\s+'
							r'(?P<v_total>[\d.,]+)\s+'
							# r'(?P<bc_icms>[\d.,]+)\s+'
							# r'(?P<v_icms>[\d.,]+)\s+'
							# r'(?P<v_ipi>[\d.,]+)\s+'
							# r'(?P<al_icms>[\d.,]+)\s+'
							# r'(?P<al_ipi>[\d.,]+)'
						)

						match = padrao.search(linha)

						if match:
							desc_complemento = ''
							j = i + 1
							while j < len(linhas):
								linha_seg = linhas[j]
								if re.match(r'^\d{7}', linha_seg):
									break
								desc_complemento += ' ' + linha_seg.strip()
								j += 1

							descricao_completa = (match.group('descricao') + ' ' + desc_complemento).strip()

							produtos.append({
								'Arquivo': os.path.basename(caminho_pdf),
								'Cód. Item': match.group('cod_item'),
								'Descrição': descricao_completa,
								# 'NCM/SH': match.group('ncm'),
								# 'CST': match.group('cst'),
								'CFOP': match.group('cfop'),
								'UN': match.group('un'),
								'QTDE': match.group('qtde'),
								'V. UNIT': match.group('v_unit'),
								'V. TOTAL': match.group('v_total'),
								# 'BC ICMS': match.group('bc_icms'),
								# 'V. ICMS': match.group('v_icms'),
								# 'V. IPI': match.group('v_ipi'),
								# 'AL ICMS': match.group('al_icms'),
								# 'AL IPI': match.group('al_ipi')
							})

							i = j
							continue
						else:
							print(f"⚠️ Linha não casou com o padrão: {linha}")

					i += 1

	return pd.DataFrame(produtos)
