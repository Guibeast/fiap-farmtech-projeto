# fiap-farmtech-projeto
Projeto de Agricultura Digital - FIAP
# Projeto FarmTech Solutions - Agricultura Digital (FIAP)

Projeto acadêmico desenvolvido para a disciplina da FIAP, simulando uma solução de agricultura digital para a empresa fictícia FarmTech Solutions.

## 📝 Descrição do Projeto

Esta solução permite o gerenciamento de áreas de cultivo de soja e café, calculando a área de plantio e a necessidade de insumos. Os dados coletados são analisados estatisticamente com um script em R, que também consulta uma API de clima para obter dados meteorológicos relevantes.

## 🛠️ Tecnologias Utilizadas

*   **Python:** Para a aplicação principal de entrada e gerenciamento de dados (CRUD).
*   **R:** Para análise estatística (média, desvio padrão) e consulta a uma API de clima.
*   **GitHub:** Para versionamento de código e simulação de trabalho em equipe.

## 📂 Estrutura do Repositório

```
.
├── codigo_python/      # Contém a aplicação principal em Python
│   └── farmtech_main.py
├── codigo_r/           # Contém o script de análise em R
│   └── analise_farmtech.R
├── resumo_academico/   # Contém o resumo do artigo científico
│   └── resumo_artigo_embrapa.pdf
├── .gitignore          # Especifica arquivos a serem ignorados pelo Git
└── README.md           # Este arquivo
```

## 🚀 Como Executar o Projeto

### Pré-requisitos

*   Python 3.x
*   R e RStudio

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/fiap-farmtech-projeto.git
    cd fiap-farmtech-projeto
    ```

2.  **Execute a aplicação Python:**
    *   Navegue até a pasta `codigo_python`.
    *   Execute o comando: `python farmtech_main.py`
    *   Use o menu interativo para adicionar, listar e gerenciar as áreas de cultura. Isso irá gerar o arquivo `dados_culturas.csv` na mesma pasta.

3.  **Execute a análise em R:**
    *   **Mova o arquivo `dados_culturas.csv`** da pasta `codigo_python/` para a pasta `codigo_r/`.
    *   Abra o arquivo `analise_farmtech.R` no RStudio.
    *   Defina o diretório de trabalho para a localização do arquivo (Session > Set Working Directory > To Source File Location ).
    *   Clique em "Source" para executar o script e ver a análise no console.

## 👥 Autores (Equipe Fictícia)

*   **Seu Nome** - *Desenvolvedor Python & Gerente de Projeto*
*   **Nome Colega 1** - *Analista de Dados & Desenvolvedor R*
*   **Nome Colega 2** - *Pesquisador & Documentação*
