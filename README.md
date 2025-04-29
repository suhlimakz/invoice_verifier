# Sistema de Validação de Notas Fiscais Eletrônicas (NF-e) 📊💼

## Descrição

Este projeto tem como objetivo desenvolver um **sistema automatizado** para **extrair** e **comparar** dados de **notas fiscais eletrônicas (NF-e)** a partir de **arquivos PDF** e de uma **planilha Excel**. O foco é validar informações chave, como **CNPJ**, **valor** e **data de emissão** das notas, garantindo a **consistência** e **integridade** dos dados. O sistema realiza comparações entre os dados extraídos dos PDFs e os valores presentes no Excel, **otimizando os processos de conferência e auditoria** de documentos fiscais. 🚀

![Automação de processo](https://media.giphy.com/media/3o6Zt7zV6VYfVRN2za/giphy.gif)

## Funcionalidades 🎯

- **Extração de Dados de PDFs**: 
  - Extração automática de **CNPJ**, **valor total** e **data de emissão** diretamente dos PDFs usando a biblioteca **pdfplumber**. 📄🔍
  - Utilização de **expressões regulares (regex)** para garantir precisão na extração. 🧑‍💻

- **Ajustes e Normalização de Dados**:
  - **Valor**: Conversão e ajuste dos valores extraídos, permitindo comparações precisas, incluindo pequenas variações (até 0.01) 💵.
  - **Data**: Ajuste de datas para o formato **DD/MM/YYYY** (padrão brasileiro), corrigindo inversões causadas pela leitura automática 📅.
  - **CNPJ**: Extração do **CNPJ** com regex para garantir que o formato esteja correto. 🏢

- **Comparação entre PDFs e Excel**:
  - Comparação dos dados extraídos dos PDFs com as informações na planilha Excel. ✔️
  - Validação de **CNPJs**, **valores** e **datas de emissão**, com verificações de pequenas discrepâncias. 🔍

- **Geração de Relatório**:
  - Geração de **relatório comparativo** exportado para um arquivo Excel, destacando as discrepâncias entre os dados. 📑📈

- **Tratamento de Exceções e Otimização**:
  - Tratamento de dados mal formatados ou ausentes, garantindo que o processo seja robusto e confiável. ⚙️
  - Conversão de formatos de dados para garantir que as comparações entre Excel e PDFs sejam feitas corretamente. 🔄

## Como Usar 🛠️

1. **Instale as dependências**:
   - Instale as bibliotecas necessárias para o projeto:
     ```bash
     pip install pdfplumber openpyxl pandas
     ```

2. **Estrutura de Diretórios**:
   - Coloque os arquivos **PDF das notas fiscais** na pasta `notas_fiscais` 📂.
   - Coloque a **planilha Excel** com os dados na raiz do projeto 🗂️.

3. **Execute o Script**:
   - Execute o script Python para realizar a extração, comparação e geração do relatório:
     ```bash
     python comparar_nfe.py
     ```

4. **Resultado**:
   - Um relatório comparativo será gerado em um arquivo Excel, indicando as discrepâncias encontradas (se houver). 📊

## Fluxo de Trabalho 🔄

1. O script percorre a pasta com os **PDFs das notas fiscais** 📂.
2. Para cada PDF, ele extrai os dados (**CNPJ**, **valor total**, **data de emissão**) 📄.
3. Os dados extraídos são comparados com as informações na **planilha Excel** 📊.
4. Um **relatório** é gerado com os resultados da comparação, destacando diferenças e validando a integridade dos dados 📝.

![Fluxo de trabalho](https://media.giphy.com/media/3o7aD2saZ5NqY3lQoc/giphy.gif)

## Objetivo 🎯

O objetivo principal deste projeto é **automatizar e otimizar** o processo de auditoria e conferência de **notas fiscais eletrônicas**, garantindo que os dados estejam consistentes e sem erros. 💼⚡

## Tecnologias Utilizadas 🛠️

- **Python** 🐍
- **pdfplumber** (para extração de dados dos PDFs) 📄🔍
- **pandas** (para manipulação de dados) 📊
- **openpyxl** (para manipulação de arquivos Excel) 📑
- **regex** (para extração de dados específicos) 🔎

## Contribuições 🤝

Contribuições são sempre bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhoria, fique à vontade para abrir uma **issue** ou enviar um **pull request**. ✨

## Licença 📜

Este projeto está licenciado sob a [MIT License](LICENSE).
