# --- Análise Estatística do Projeto FarmTech ---

# Limpa o console para uma visualização limpa
cat("\014") 

print("--- Iniciando Análise de Dados da FarmTech ---")

# Define o nome do arquivo a ser lido
nome_arquivo <- "dados_culturas.csv"

# Verifica se o arquivo de dados existe no diretório
if (file.exists(nome_arquivo)) {
  
  # Lê os dados do arquivo CSV gerado pelo Python
  dados_culturas <- read.csv(nome_arquivo, header = TRUE)
  
  # Verifica se o arquivo tem dados para analisar (mais de 0 linhas)
  if (nrow(dados_culturas) > 0) {
    
    # --- EXIBIÇÃO DA TABELA DE DADOS FORMATADA ---
    
    # 1. Cria uma cópia da tabela apenas para exibição
    dados_para_exibir <- dados_culturas
    
    # 2. Formata a coluna de área para o padrão brasileiro
    dados_para_exibir$area_m2 <- format(round(dados_para_exibir$area_m2, 2), nsmall = 2, big.mark = ".", decimal.mark = ",")
    
    # 3. Renomeia as colunas para uma apresentação mais clara
    colnames(dados_para_exibir) <- c("ID", "Cultura", "Área (m²)") # <<< ALTERAÇÃO AQUI
    
    # 4. Exibe a tabela formatada
    cat("\n--------------------------------------------\n")
    cat("      DADOS CARREGADOS DO ARQUIVO CSV\n")
    cat("--------------------------------------------\n\n")
    print(dados_para_exibir, row.names = FALSE) # row.names = FALSE remove os números de linha do R
    cat("\n--------------------------------------------\n")
    
    # O restante do script continua usando a tabela original "dados_culturas" com os números puros
    
    # Extrai a coluna de área para os cálculos
    areas <- dados_culturas$area_m2
    
    # --- Cálculos Estatísticos Básicos ---
    
    media_areas <- mean(areas)
    
    if (length(areas) > 1) {
      desvio_padrao_areas <- sd(areas)
    } else {
      desvio_padrao_areas <- 0
    }
    
    # --- Exibição dos Resultados Finais (SEÇÃO FORMATADA) ---
    
    # Prepara os números para exibição
    media_formatada <- format(round(media_areas, 2), nsmall = 2, big.mark = ".", decimal.mark = ",")
    dp_formatado <- format(round(desvio_padrao_areas, 2), nsmall = 2, big.mark = ".", decimal.mark = ",")
    
    cat("\n\n============================================\n")
    cat("    RESULTADOS DA ANÁLISE ESTATÍSTICA\n")
    cat("============================================\n\n")
    cat(" >> Número total de áreas cadastradas:", length(areas), "\n\n")
    cat(" >> Média das áreas de plantio:", media_formatada, "m²\n")
    cat(" >> Desvio Padrão das áreas:", dp_formatado, "m²\n\n")
    cat("============================================\n")
    
  } else {
    print("O arquivo 'dados_culturas.csv' está vazio. Adicione culturas no programa Python primeiro.")
  }
  
} else {
  print(paste("Arquivo '", nome_arquivo, "' não encontrado.", sep=""))
  print("Execute o programa Python para gerar o arquivo de dados primeiro.")
}