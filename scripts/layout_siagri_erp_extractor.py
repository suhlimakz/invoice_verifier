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

def extrair_cnpj_da_chave(chave):
	if chave and len(chave) == 45:
		cnpj_puro = chave[7:21] 
		cnpj_formatado = f'{cnpj_puro[0:2]}.{cnpj_puro[2:5]}.{cnpj_puro[5:8]}/{cnpj_puro[8:12]}-{cnpj_puro[12:14]}'
		return cnpj_formatado
	else:
		print(f"Aviso: chave inválida para extrair CNPJ → {chave}")
		return None