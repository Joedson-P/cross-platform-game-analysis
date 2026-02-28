import requests
import pandas as pd
import os

def fetch_top_100_gog():
    print("Iniciando a extração dos dados da GOG...")

    url = 'https://catalog.gog.com/v1/catalog?limit=100&order=desc:bestselling&productType=in:game,pack&page=1&countryCode=BR&locale=en-US&currencyCode=BRL'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        products = data.get('products', [])

        if not products:
            print("Nenhum produto encontrado.")
            return None
        
        df = pd.DataFrame(products)

        return df
    
    except Exception as e:
        print(f"Erro ao extrair dados da GOG: {e}")
        return None
    
if __name__ == "__main__":
    df_gog = fetch_top_100_gog()

    if df_gog is not None:
        df_gog.to_csv("data/data_raw_gog.csv", index = False)

        print("Dados salvos em 'data/data_raw_gog.csv'")
        print("Amostras dos dados:")
        print(df_gog[['title', 'developers', 'price']].head(10))