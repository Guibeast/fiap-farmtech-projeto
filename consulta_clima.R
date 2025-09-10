# --- Consulta de Clima Inteligente com Memória e Desambiguação ---

# Carrega os pacotes necessários
library(httr)
library(jsonlite)

# Nome do arquivo para guardar a última localização
ARQUIVO_CONFIG <- "ultima_localizacao.json"

# --- Funções Auxiliares ---

carregar_localizacao <- function() {
  if (file.exists(ARQUIVO_CONFIG)) {
    tryCatch({ return(read_json(ARQUIVO_CONFIG)) }, error = function(e) { return(NULL) })
  }
  return(NULL)
}

salvar_localizacao <- function(localizacao) {
  write_json(localizacao, ARQUIVO_CONFIG, auto_unbox = TRUE)
}

# Função para obter uma nova localização do usuário
obter_nova_localizacao <- function() {
  while (TRUE) {
    cat("\n--- Definir Nova Localidade ---\n")
    cidade <- readline(prompt = "Digite o nome da Cidade (ou 0 para cancelar): ")
    if (cidade == "0") return(NULL)
    
    termo_busca <- paste(cidade, "Brasil", sep = ", ")
    cat("\nBuscando possíveis localizações para '", cidade, "'...\n", sep = "")
    
    url_geocoding <- "https://nominatim.openstreetmap.org/search"
    resposta_geo <- GET(url_geocoding, query = list(q = termo_busca, format = "json", limit = 5, countrycodes = "br"),
                        add_headers("User-Agent" = "ProjetoFIAP/1.0"))
    
    if (status_code(resposta_geo) == 200) {
      dados_geo <- fromJSON(content(resposta_geo, "text"))
      
      if (length(dados_geo) > 0 && !is.null(dados_geo$lat)) {
        
        localizacao_escolhida <- NULL
        
        if (nrow(dados_geo) == 1) {
          localizacao_escolhida <- dados_geo[1, ]
        } else {
          cat("Encontramos múltiplas localidades. Por favor, escolha a correta:\n")
          for (i in 1:nrow(dados_geo)) {
            cat("[", i, "] ", dados_geo$display_name[i], "\n", sep = "")
          }
          cat("[0] Nenhuma das opções / Tentar novamente\n")
          
          while(TRUE) {
            escolha_num_str <- readline(prompt = "Digite o número da opção desejada: ")
            if (escolha_num_str == "0") {
              localizacao_escolhida <- NULL
              break
            }
            escolha_num <- as.numeric(escolha_num_str)
            if (!is.na(escolha_num) && escolha_num %in% 1:nrow(dados_geo)) {
              localizacao_escolhida <- dados_geo[escolha_num, ]
              break
            } else {
              cat("❌ Opção inválida. Tente novamente.\n")
            }
          }
        }
        
        if (!is.null(localizacao_escolhida)) {
          # --- LÓGICA INTELIGENTE PARA LIMPAR O NOME ---
          full_display_name <- localizacao_escolhida$display_name
          parts <- strsplit(full_display_name, ", ")[[1]]
          
          # Remove partes que são apenas CEPs
          parts <- parts[!grepl("^[0-9-]+$", parts)]
          
          # Pega a cidade, o estado (geralmente antepenúltimo) e o país (último)
          cidade_limpa <- localizacao_escolhida$name
          pais_limpo <- parts[length(parts)]
          estado_limpo <- parts[length(parts) - 2] # Pega o antepenúltimo item da lista
          
          nome_final <- paste(cidade_limpa, estado_limpo, pais_limpo, sep = ", ")
          
          localizacao <- list(
            nome_exibicao = nome_final,
            latitude = as.numeric(localizacao_escolhida$lat),
            longitude = as.numeric(localizacao_escolhida$lon)
          )
          cat("✅ Localização definida para:", localizacao$nome_exibicao, "\n")
          return(localizacao)
        }
        
      } else {
        cat("❌ Erro: Nenhuma localização encontrada para '", cidade, "'. Por favor, tente novamente.\n", sep="")
      }
    } else {
      cat("❌ Erro: Falha na conexão com o serviço de geocodificação.\n")
      return(NULL)
    }
  }
}

# Função para buscar e exibir o clima
exibir_clima <- function(localizacao) {
  cat("\nBuscando clima para", localizacao$nome_exibicao, "...\n")
  
  url_clima <- paste0("https://api.open-meteo.com/v1/forecast?latitude=", localizacao$latitude,
                      "&longitude=", localizacao$longitude, "&current_weather=true")
  
  resposta_clima <- GET(url_clima)
  
  if (status_code(resposta_clima) == 200) {
    dados_clima <- fromJSON(content(resposta_clima, "text"))
    
    cat("\n--- Condições do Tempo Atuais ---\n")
    cat("Local:", localizacao$nome_exibicao, "\n")
    cat("Data e Hora da Consulta:", format(Sys.time(), "%d/%m/%Y %H:%M:%S"), "\n")
    cat("Temperatura:", dados_clima$current_weather$temperature, "°C\n")
    cat("Velocidade do Vento:", dados_clima$current_weather$windspeed, "km/h\n")
    cat("------------------------------------\n")
  } else {
    cat("Erro: Não foi possível obter os dados do clima.\n")
  }
}

# --- Lógica Principal do Programa ---

cat("\014") 
print("--- Aplicação de Consulta de Clima ---")

localizacao_atual <- carregar_localizacao()

if (is.null(localizacao_atual)) {
  cat("Bem-vindo! Parece que é a sua primeira vez aqui.\n")
  localizacao_atual <- obter_nova_localizacao()
  if (!is.null(localizacao_atual)) {
    salvar_localizacao(localizacao_atual)
  }
}

if (!is.null(localizacao_atual)) {
  while (TRUE) {
    exibir_clima(localizacao_atual)
    
    cat("\nEscolha uma opção:\n")
    cat("[1] Atualizar clima da localidade atual\n")
    cat("[2] Trocar localidade\n")
    cat("[0] Sair\n")
    
    escolha <- readline(prompt = "Opção: ")
    
    if (escolha == "1") {
      next
    } else if (escolha == "2") {
      nova_localizacao <- obter_nova_localizacao()
      if (!is.null(nova_localizacao)) {
        localizacao_atual <- nova_localizacao
        salvar_localizacao(localizacao_atual)
      }
    } else if (escolha == "0") {
      cat("Saindo do programa. Até logo!\n")
      break
    } else {
      cat("Opção inválida. Tente novamente.\n")
    }
  }
} else {
  cat("Não foi possível definir uma localização. O programa será encerrado.\n")
}