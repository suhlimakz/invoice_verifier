# Análise Técnica do Layout de DANFE (Nota Fiscal Eletrônica)

## Objetivo
Mapear a estrutura visual e os padrões de formatação presentes no layout de uma DANFE específica, a fim de viabilizar a extração automatizada de dados via script.

---

## Estrutura Geral da DANFE
A DANFE analisada é composta por seções bem definidas, distribuídas em blocos de informações textuais e tabelares. A maioria dos campos segue um padrão consistente de posicionamento, formatação e escrita, embora existam desafios específicos na extração da tabela de itens, especialmente no tratamento de descrições com quebras e desalinhamentos.

---

## Mapeamento Detalhado por Seção

### 1. Barra Superior
- **Formato:** Lista horizontal com campos alinhados à esquerda e um campo à direita.
- **Campos:**
  - **Recebemos de**
  - **Data de Recebimento**
  - **Identificação e Assinatura do Recebedor**
  - **Dados da NF:**
    - **Número da NF-e**
      - Prefixo: `Nº.`
      - Formato: Numérico, sem pontos ou separadores.
    - **Série da NF-e**
      - Prefixo: `SÉRIE`
      - Formato: Numérico, sem pontos.

---

### 2. Identificação do Emitente
- **Formato:** Lista de informações textuais, com caixas delimitadas e seções agrupadas.
- **Campos:**
  - **Identificação do Emitente:** Caixa com dados e logo.
  - **DANFE:** Informações gerais sem delimitação rígida.
    - **Tipo de Operação:** 
      - Valor: `0 - Entrada` ou `1 - Saída`.
      - Dentro de um quadro delimitado.
    - **Número da NF:** 
      - Prefixo: `Nº`
      - Formato: Numérico, sem separadores.
    - **Série:** 
      - Prefixo: `SÉRIE`
      - Formato: Numérico, sem separadores.
    - **Contagem de Página:** `Página X de Y`
    - **Código de Barras:** Caixa delimitada.
    - **Chave de Acesso:** 
      - Descritivo: `Chave de acesso da NF-e`
      - Formato: 44 caracteres agrupados em blocos de 4, separados por espaços (11 blocos).
    - **Consulta de Autenticidade:** Caixa delimitada.
    - **Natureza da Operação:** Campo textual padrão.
    - **Protocolo de Autorização:** Texto.
    - **Inscrição Estadual:** Pode aparecer duas vezes (verificar origem e destino).
    - **CNPJ:** Formato tradicional `00.000.000/0000-00`.

---

### 3. Destinatário / Remetente
- **Formato:** Lista textual agrupada em uma caixa delimitada.
- **Campos:**
  - **Nome / Razão Social**
  - **CNPJ ou CPF:** 
    - CNPJ: `00.000.000/0000-00`
    - CPF: `000.000.000-00`
  - **Data de Emissão:** `dd/mm/aaaa`
  - **Data de Saída:** `dd/mm/aaaa`
  - **Endereço Completo**
  - **Município**
  - **UF:** Duas letras.
  - **CEP**
  - **Telefone**
  - **Inscrição Estadual**
  - **Hora de Saída**

---

### 4. Dados do Produto / Serviço
- **Formato:** 
  - Tabela estruturada com header delimitado por linha contínua.
  - Separação dos itens por linhas tracejadas horizontais.

- **Desafio Técnico:** 
  - A descrição do item pode apresentar **quebra de linha dentro da própria célula**.
  - Quando a descrição é muito extensa, ela pode extrapolar o espaço da coluna, alinhando abaixo da primeira coluna.
  - A separação entre itens ocorre por linha tracejada.

- **Headers e Campos:**

| Header                | Descrição                                         | Formatação                                                         |
|-----------------------|---------------------------------------------------|---------------------------------------------------------------------|
| Código                | Código do Item                                    | Texto ou numérico                                                  |
| Descrição             | Descrição do Produto                              | Texto em maiúsculas, com possibilidade de quebra de linha          |
| NCM/SH                | Código Fiscal                                     | Numérico                                                           |
| CST                   | Código da Situação Tributária                     | Numérico                                                           |
| CFOP                  | Código Fiscal da Operação                         | 4 dígitos                                                          |
| UN                    | Unidade de Medida                                 | 2 caracteres                                                       |
| QTDE                  | Quantidade                                        | Separador de milhar `.` e decimal `,` (ex.: `1.000,0000`)          |
| V.UNIT                | Valor Unitário                                    | Monetário                                                          |
| V.TOTAL               | Valor Total                                       | Monetário                                                          |
| BC ICMS               | Base de Cálculo ICMS                              | Monetário                                                          |
| Valor ICMS            | Valor do ICMS                                     | Monetário                                                          |
| V IPI                 | Valor do IPI                                      | Monetário                                                          |
| Aliquota ICMS         | Alíquota do ICMS                                  | Percentual                                                         |
| Aliquota IPI          | Alíquota do IPI                                   | Percentual                                                         |

---

### 5. Cálculo do Imposto
- Informações fiscais agregadas, geralmente posicionadas abaixo da tabela de produtos.

---

### 6. Transportador
- Dados referentes ao transporte, caso aplicável.

---

### 7. Fatura e Cobrança
- Informações financeiras sobre cobrança, valores totais, parcelas e vencimentos.

---

### 8. Dados Adicionais
- **Formato:** Caixa delimitada em formato de tabela simples.
- **Campos:**
  - **Informações Complementares**
  - **Reservado ao Fisco**

