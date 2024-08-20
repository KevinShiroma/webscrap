import requests # Fazer uma solicitação HTTP
from bs4 import BeautifulSoup # Para a manipulação de HTML
import pandas as pd # Criação de dataframes

def extrair_tabela(url):
    # Faz a requisição para obter o conteúdo da página
    resposta = requests.get(url)

    if resposta.status_code == 200:
        # Cria um objeto BeautifulSoup para parsear o HTML
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Encontra a primeira tabela na página
        tabela = soup.find("table")
        
        if tabela:
            # Extrai as linhas da tabela
            linhas = tabela.find_all("tr")
            
            # Inicializa uma lista para armazenar os dados
            dados = []
            
            # Itera sobre as linhas da tabela
            for linha in linhas:
                # Extrai as células de cada linha
                celulas = linha.find_all("td")
                # Extrai o texto de cada célula e adiciona à lista 'dados'
                dados.append([celula.get_text(strip=True) for celula in celulas])
            
            # Remove linhas vazias
            dados = [linha for linha in dados if any(linha)]

            # Criar o DataFrame com os dados extraídos
            tabela_autopista = pd.DataFrame(dados)
            
            
            return tabela_autopista
        else:
            print("Tabela não encontrada na página.")
            return None
    else:
        print(f"Falha ao acessar a página: {resposta.status_code}")
        return None


url_valores = "https://www.gov.br/antt/pt-br/assuntos/rodovias/concessionarias/lista-de-concessoes/concebra/tarifas-de-pedagio"
tabela_autopista = extrair_tabela(url_valores)
print(tabela_autopista)

############################################################################################################################################

# Retirando a primeira linha (que contém as praças)
# Extrair a primeira linha e transformá-la em uma nova coluna
tabela_autopista.insert(0, 'Nova_Coluna', tabela_autopista.iloc[1])
print(tabela_autopista['Nova_Coluna'])

# Remover a primeira linha (que já foi transformada em coluna)
tabela_autopista = tabela_autopista.drop(1).reset_index(drop=True)

# Renomear a nova coluna, se necessário
tabela_autopista = tabela_autopista.rename(columns={'Nova_Coluna': 'pracas_autopista'})
print(tabela_autopista)

# tabela_autopista.columns = tabela_autopista.iloc[1] # Seleciona a primeira linha do DataFrame e as colunas recebem os dados da primeira linha
# tabela_autopista = tabela_autopista.drop(0).reset_index(drop=True) # Remove a primeira linha do Dataframe e reseta a indexação.
# display(tabela_autopista)

