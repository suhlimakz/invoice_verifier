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