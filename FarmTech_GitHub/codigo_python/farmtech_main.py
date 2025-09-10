# farmtech_main.py

import math
import csv
import os
import json  # Biblioteca para salvar/carregar dados complexos
import sys  # Biblioteca para encontrar o caminho do script

# --- Estrutura de Dados Principal ---
culturas = []
proximo_id = 1

# --- Bloco de Configuração de Arquivos (A GRANDE MUDANÇA ESTÁ AQUI) ---
# Constrói o caminho completo para os arquivos, garantindo que eles sejam salvos na mesma pasta do script.
# Isso resolve problemas de permissão e de pastas sincronizadas (como OneDrive).
try:
    caminho_script = os.path.dirname(os.path.abspath(sys.argv[0]))
except IndexError:
    caminho_script = os.getcwd()  # Fallback para ambientes onde sys.argv[0] não está disponível

ARQUIVO_JSON = os.path.join(caminho_script, 'farmtech_dados.json')
ARQUIVO_CSV = os.path.join(caminho_script, 'dados_culturas.csv')


# --- Funções de Persistência (Salvar e Carregar) ---

def salvar_dados():
    """Salva a lista completa de culturas no arquivo JSON."""
    try:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as file:
            json.dump(culturas, file, indent=4, ensure_ascii=False)
        salvar_dados_para_r()  # Mantém o CSV atualizado também
    except Exception as e:
        print(f"❌ ERRO CRÍTICO AO SALVAR JSON: {e}")


def carregar_dados():
    """Carrega os dados do arquivo JSON ao iniciar e atualiza o próximo ID."""
    global culturas, proximo_id
    if not os.path.exists(ARQUIVO_JSON):
        print("ℹ️ Nenhum arquivo de dados encontrado. Iniciando um novo registro.")
        culturas = []
        return

    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as file:
            # Verifica se o arquivo não está vazio antes de tentar carregar
            if os.path.getsize(ARQUIVO_JSON) > 0:
                culturas = json.load(file)
                if culturas:
                    max_id = max(c['id'] for c in culturas)
                    proximo_id = max_id + 1
                print("✅ Dados carregados com sucesso!")
            else:
                print("ℹ️ Arquivo de dados encontrado, mas está vazio. Iniciando novo registro.")
                culturas = []
    except json.JSONDecodeError:
        print("⚠️ Arquivo de dados corrompido ou vazio. Iniciando um novo registro.")
        culturas = []
    except Exception as e:
        print(f"❌ ERRO CRÍTICO AO CARREGAR JSON: {e}")
        culturas = []


def salvar_dados_para_r():
    """Salva os dados relevantes em um arquivo CSV."""
    try:
        with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'tipo_cultura', 'area_m2'])
            if culturas:
                for cultura in culturas:
                    writer.writerow([cultura['id'], cultura['tipo_cultura'], cultura['area_calculada_m2']])
    except Exception as e:
        print(f"❌ ERRO CRÍTICO AO SALVAR CSV: {e}")


# --- Funções de Exibição ---

def mostrar_detalhes_cultura(cultura):
    """Exibe os detalhes formatados de uma única cultura."""
    print("\n--- Detalhes da Cultura Cadastrada ---")
    print("-----------------------------------------")
    print(f"ID: {cultura['id']}")
    print(f"Cultura: {cultura['tipo_cultura'].capitalize()}")
    print(f"Área Calculada: {cultura['area_calculada_m2']} m²")
    dims = cultura['dimensoes']
    if cultura['forma_area'] == 'retangulo':
        print(f"Formato: Retângulo (Comprimento: {dims['comprimento']}m, Largura: {dims['largura']}m)")
    else:
        print(f"Formato: Círculo (Raio: {dims['raio']}m)")
    if cultura['insumos']:
        print("Insumos:")
        for i, insumo in enumerate(cultura['insumos'], 1):
            print(f"  [{i}] Produto: {insumo['produto']}")
            print(f"      Total Necessário: {insumo['total_necessario']} unidades")
    else:
        print("Insumos: Nenhum insumo cadastrado.")
    print("-----------------------------------------")


def listar_culturas_resumido():
    """Exibe uma lista simplificada das culturas com seus IDs."""
    print("\n--- Culturas Disponíveis ---")
    for cultura in culturas:
        print(f"  ID: {cultura['id']} | Tipo: {cultura['tipo_cultura'].capitalize()}")
    print("----------------------------")


# --- Funções de Cálculo ---

def calcular_area(forma, dimensoes):
    """Calcula a área com base na forma geométrica."""
    if forma == "retangulo":
        return dimensoes["comprimento"] * dimensoes["largura"]
    elif forma == "circulo":
        return math.pi * (dimensoes["raio"] ** 2)
    return 0


# --- Funções do Menu (CRUD) ---

def adicionar_cultura():
    """Adiciona uma nova área de cultura e entra em um menu de contexto."""
    global proximo_id

    while True:
        print("\n--- Adicionar Nova Área de Cultura ---")
        print("(Digite '0' a qualquer momento para cancelar e voltar ao menu principal)")
        while True:
            tipo_cultura = input("Digite o tipo de cultura (soja/café): ").lower().strip()
            if tipo_cultura in ["soja", "café"]: break
            if tipo_cultura == "0": return
            print("❌ Cultura inválida. Por favor, escolha 'soja' ou 'café'.")

        forma_area = "retangulo" if tipo_cultura == "soja" else "circulo"
        dimensoes = {}

        if forma_area == "retangulo":
            while True:
                try:
                    entrada = input("Digite o comprimento (em metros): ").strip()
                    if entrada == '0': return
                    comprimento = float(entrada.replace(',', '.'))
                    if comprimento > 0: break
                    print("❌ O valor deve ser um número positivo.")
                except ValueError:
                    print("❌ Erro: Digite um número válido (use '.' para decimais).")
            while True:
                try:
                    entrada = input("Digite a largura (em metros): ").strip()
                    if entrada == '0': return
                    largura = float(entrada.replace(',', '.'))
                    if largura > 0: break
                    print("❌ O valor deve ser um número positivo.")
                except ValueError:
                    print("❌ Erro: Digite um número válido (use '.' para decimais).")
            dimensoes = {"comprimento": comprimento, "largura": largura}
        else:  # Círculo
            while True:
                try:
                    entrada = input("Digite o raio (em metros): ").strip()
                    if entrada == '0': return
                    raio = float(entrada.replace(',', '.'))
                    if raio > 0: break
                    print("❌ O valor deve ser um número positivo.")
                except ValueError:
                    print("❌ Erro: Digite um número válido (use '.' para decimais).")
            dimensoes = {"raio": raio}

        area = calcular_area(forma_area, dimensoes)
        insumos = []

        while True:
            add_insumo_choice = input("Deseja adicionar um insumo inicial para esta cultura? (s/n): ").lower().strip()
            if add_insumo_choice in ['s', 'n', '0']: break
            print("❌ Resposta inválida. Digite 's' ou 'n'.")

        if add_insumo_choice == 's':
            while True:
                produto = input("Nome do insumo: ")
                while True:
                    try:
                        entrada = input(f"Quantidade de '{produto}' por m²: ").strip()
                        qtd_por_metro = float(entrada.replace(',', '.'))
                        if qtd_por_metro > 0:
                            total_necessario = area * qtd_por_metro
                            insumos.append({
                                "produto": produto, "qtd_por_metro": qtd_por_metro,
                                "total_necessario": round(total_necessario, 2)
                            })
                            print(f"✅ Insumo '{produto}' adicionado.")
                            break
                        print("❌ A quantidade deve ser um número positivo.")
                    except ValueError:
                        print("❌ Erro: Digite um número válido (use '.' para decimais).")

                while True:
                    outro_insumo = input("Deseja adicionar outro insumo? (s/n): ").lower().strip()
                    if outro_insumo in ['s', 'n']: break
                    print("❌ Resposta inválida. Digite 's' ou 'n'.")

                if outro_insumo == 'n': break

        nova_cultura = {
            "id": proximo_id, "tipo_cultura": tipo_cultura, "forma_area": forma_area,
            "dimensoes": dimensoes, "area_calculada_m2": round(area, 2), "insumos": insumos
        }
        culturas.append(nova_cultura)
        proximo_id += 1
        salvar_dados()

        while True:
            mostrar_detalhes_cultura(nova_cultura)
            print("O que você deseja fazer agora?")
            print("[1] Adicionar outra cultura")
            print("[2] Editar insumos da cultura acima")
            print("[0] Voltar ao menu principal")

            escolha = input("Escolha uma opção: ").strip()

            if escolha == '1':
                break
            elif escolha == '2':
                editar_insumos(nova_cultura)
                salvar_dados()
            elif escolha == '0':
                return
            else:
                print("❌ Opção inválida.")

        continue


def editar_insumos(cultura):
    """Permite adicionar ou remover insumos de uma cultura."""
    while True:
        print("\n--- Editando Insumos ---")
        if cultura['insumos']:
            print("Insumos atuais:")
            for i, insumo in enumerate(cultura['insumos'], 1):
                print(f"  [{i}] {insumo['produto']} ({insumo['total_necessario']} unidades)")
        else:
            print("Nenhum insumo cadastrado.")

        print("\n[1] Adicionar um novo insumo")
        print("[2] Remover um insumo")
        print("[0] Concluir edição")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            produto = input("Nome do novo insumo: ")
            while True:
                try:
                    entrada = input(f"Quantidade de '{produto}' por m²: ").strip()
                    qtd_por_metro = float(entrada.replace(',', '.'))
                    if qtd_por_metro > 0:
                        total_necessario = cultura['area_calculada_m2'] * qtd_por_metro
                        cultura['insumos'].append({
                            "produto": produto, "qtd_por_metro": qtd_por_metro,
                            "total_necessario": round(total_necessario, 2)
                        })
                        print(f"✅ Insumo '{produto}' adicionado.")
                        break
                    print("❌ A quantidade deve ser um número positivo.")
                except ValueError:
                    print("❌ Erro: Digite um número válido (use '.' para decimais).")

        elif escolha == '2':
            if not cultura['insumos']:
                print("Não há insumos para remover.")
                continue
            while True:
                try:
                    idx_str = input("Digite o número do insumo a ser removido: ").strip()
                    idx = int(idx_str)
                    if 1 <= idx <= len(cultura['insumos']):
                        removido = cultura['insumos'].pop(idx - 1)
                        print(f"✅ Insumo '{removido['produto']}' removido.")
                        break
                    else:
                        print(f"❌ Número inválido. Escolha um número entre 1 e {len(cultura['insumos'])}.")
                except ValueError:
                    print("❌ Por favor, digite apenas o número correspondente.")

        elif escolha == '0':
            print("Edição de insumos concluída.")
            break
        else:
            print("❌ Opção inválida.")


def listar_culturas():
    """Exibe todas as áreas de cultura cadastradas com detalhes."""
    print("\n--- Lista de Áreas de Cultura Cadastradas ---")
    if not culturas:
        print("Nenhuma cultura cadastrada no momento.")
        return

    for cultura in culturas:
        mostrar_detalhes_cultura(cultura)


def encontrar_cultura_por_id(id_busca):
    """Encontra uma cultura na lista pelo seu ID."""
    for cultura in culturas:
        if cultura["id"] == id_busca:
            return cultura
    return None


def atualizar_cultura():
    """Atualiza os dados de uma cultura existente."""
    print("\n--- Atualizar Dados de uma Área ---")
    if not culturas:
        print("Nenhuma cultura para atualizar.")
        return

    listar_culturas_resumido()

    while True:
        try:
            id_str = input("Digite o ID da área que deseja atualizar (ou 0 para voltar): ").strip()
            if id_str == '0': return
            id_busca = int(id_str)
            cultura = encontrar_cultura_por_id(id_busca)
            if not cultura:
                print(f"❌ Erro: Nenhuma cultura encontrada com o ID {id_busca}.")
                continue
            break
        except ValueError:
            print("❌ Erro: ID inválido. Por favor, insira um número.")

    print(f"\nAtualizando dados da cultura ID {id_busca} ({cultura['tipo_cultura']}).")
    print("Deixe em branco para não alterar o valor.")

    try:
        if cultura['forma_area'] == 'retangulo':
            novo_comp_str = input(f"Novo comprimento (atual: {cultura['dimensoes']['comprimento']}): ").strip()
            if novo_comp_str: cultura['dimensoes']['comprimento'] = float(novo_comp_str.replace(',', '.'))

            nova_larg_str = input(f"Nova largura (atual: {cultura['dimensoes']['largura']}): ").strip()
            if nova_larg_str: cultura['dimensoes']['largura'] = float(nova_larg_str.replace(',', '.'))
        else:
            novo_raio_str = input(f"Novo raio (atual: {cultura['dimensoes']['raio']}): ").strip()
            if novo_raio_str: cultura['dimensoes']['raio'] = float(novo_raio_str.replace(',', '.'))

        cultura['area_calculada_m2'] = round(calcular_area(cultura['forma_area'], cultura['dimensoes']), 2)
        for insumo in cultura['insumos']:
            insumo['total_necessario'] = round(cultura['area_calculada_m2'] * insumo['qtd_por_metro'], 2)

        salvar_dados()
        print("\n✅ Dados atualizados com sucesso!")
        mostrar_detalhes_cultura(cultura)

    except ValueError:
        print("❌ Erro: Valor inválido. A atualização foi cancelada.")


def excluir_cultura():
    """Remove uma cultura do sistema pelo seu ID."""
    print("\n--- Excluir uma Área de Cultura ---")
    if not culturas:
        print("Nenhuma cultura para excluir.")
        return

    listar_culturas_resumido()

    while True:
        try:
            id_str = input("Digite o ID da área que deseja excluir (ou 0 para voltar): ").strip()
            if id_str == '0': return
            id_busca = int(id_str)
            cultura = encontrar_cultura_por_id(id_busca)
            if not cultura:
                print(f"❌ Erro: Nenhuma cultura encontrada com o ID {id_busca}.")
                continue
            break
        except ValueError:
            print("❌ Erro: ID inválido. Por favor, insira um número.")

    while True:
        confirmacao = input(f"Tem certeza que deseja excluir a área ID {id_busca}? (s/n): ").lower().strip()
        if confirmacao == 's':
            culturas.remove(cultura)
            salvar_dados()
            print("\n✅ Área de cultura excluída com sucesso!")
            return
        elif confirmacao == 'n':
            print("Operação cancelada.")
            return
        else:
            print("❌ Resposta inválida! Digite 's' ou 'n'.")


def menu():
    """Exibe o menu principal."""
    print("\n" + "=" * 45)
    print("===   FarmTech Solutions - Agricultura Digital   ===")
    print("=" * 45)
    print("[1] Adicionar nova área de cultura")
    print("[2] Listar áreas de cultura")
    print("[3] Atualizar dados de uma área")
    print("[4] Excluir uma área de cultura")
    print("[5] Sair do programa")
    print("=" * 45)

    while True:
        escolha = input("Escolha uma opção (1-5): ").strip()
        if escolha in ['1', '2', '3', '4', '5']:
            return escolha
        else:
            print("❌ Opção inválida! Digite um número de 1 a 5.")


def main():
    """Função principal que executa o loop do programa."""
    carregar_dados()

    while True:
        escolha = menu()
        if escolha == '1':
            adicionar_cultura()
        elif escolha == '2':
            listar_culturas()
        elif escolha == '3':
            atualizar_cultura()
        elif escolha == '4':
            excluir_cultura()
        elif escolha == '5':
            print("\nSaindo do programa. Até logo!")
            break

        if escolha in ['2', '3', '4']:
            input("\nPressione Enter para voltar ao menu principal...")


if __name__ == "__main__":
    main()