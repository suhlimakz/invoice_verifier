import os
import pdfplumber
from  layout_siagri_erp_extractor import ( 
                                          extrair_chave_acesso,
                                          extrair_uf_emitente,
                                          extrair_tipo_movimentacao,
                                          extrair_cnpj_da_chave,
                                          extrair_serie,
                                          extrair_numero_nf,
                                          extrair_natureza_operacao,
                                          extrair_linha_nome_razao_social_cnpj_cpf_data,
                                          extrair_destinatario,
                                          extrair_cnpj_cpf_destinatario,
                                          extrair_data_emissao,
                                          extrair_municipio_destinatario,
                                          extrair_uf_destinatario
)

def main():
  base_dir = os.path.dirname(os.path.abspath(__file__))

  pasta_pdfs = os.path.join(base_dir, '..', 'data', 'notas_fiscais', 'siagri-erp')

  pasta_pdfs = os.path.abspath(pasta_pdfs)

  print(f"📂 Lendo arquivos da pasta: {pasta_pdfs}")

  arquivos_pdf = [
    f for f in os.listdir(pasta_pdfs) if f.lower().endswith('.pdf')
  ]

  if not arquivos_pdf:
    print("Nenhum arquivo PDF encontrado na pasta.")
    return

  resultados = []

  for arquivo in arquivos_pdf:
    caminho_pdf = os.path.join(pasta_pdfs, arquivo)
    print(f"\n📄 Processando: {arquivo}")
    
    try:
      with pdfplumber.open(caminho_pdf) as pdf:
        texto = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        
        chave = extrair_chave_acesso(texto)
        linha_dados = extrair_linha_nome_razao_social_cnpj_cpf_data(texto)
        dados = {
          'arquivo': arquivo,
          'chave_acesso': chave,
          'tipo_movimentacao':  extrair_tipo_movimentacao(chave),
          'uf_emitente': extrair_uf_emitente(chave),
          'cnpj_emitente': extrair_cnpj_da_chave(chave),
          'serie_nf': extrair_serie(chave),
          'numero_nf': extrair_numero_nf(chave),
          'natureza_operacao': extrair_natureza_operacao(texto),
          'nome_destinatario': extrair_destinatario(linha_dados),
          'cnpj_cpf_destinatario': extrair_cnpj_cpf_destinatario(linha_dados),
          'data_emissao_nfe': extrair_data_emissao(linha_dados),
          'municipio_destinatario': extrair_municipio_destinatario(texto),
          'uf_destinatario': extrair_uf_destinatario(texto)
        }
        
        resultados.append(dados)
        
        print(f"✔️ Chave de acesso: {dados['chave_acesso']}")
        print(f"✔️ Tipo de movimentação: {dados['tipo_movimentacao']}")
        print(f"✔️ UF emitente: {dados['uf_emitente']}")
        print(f"✔️ CNPJ emitente: {dados['cnpj_emitente']}")
        print(f"✔️ Série NF-e: {dados['serie_nf']}")
        print(f"✔️ Número NF-e: {dados['numero_nf']}")
        print(f"✔️ Natureza da operação: {dados['natureza_operacao']}")
        print(f"✔️ Nome do destinatário: {dados['nome_destinatario']}")
        print(f"✔️ CNPJ/CPF do destinatário: {dados['cnpj_cpf_destinatario']}")
        print(f"✔️ Data de emissão NF-e: {dados['data_emissao_nfe']}")
        print(f"✔️ Municipio do destinatário: {dados['municipio_destinatario']}")
        print(f"✔️ UF do destinatário: {dados['uf_destinatario']}")
        
        
        
        
    except Exception as e:
      print(f"❌ Erro ao processar {arquivo}: {e}")
            
    print("\n🎯 Dados extraídos de todos os PDFs:")
    for item in resultados:
      print(item)
        
    return resultados
  

  
if __name__ == "__main__":
  main()