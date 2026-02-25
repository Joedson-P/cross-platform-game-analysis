import requests
import pandas as pd

def fetch_top_100_steam():
    print("Iniciando a extração dos dados da Steam...")

    url = 'https://steamspy.com/api.php?request=top100in2weeks'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame.from_dict(data, orient='index')

        df.reset_index(inplace=True)
        df.rename(columns={'index':'appid'}, inplace=True)
        print(f"Sucesso! {len(df)} jogos extraídos.")
        return df
    
    except Exception as e:
        print(f"Erro ao extrair dados da Steam: {e}")
        return None
    
if __name__ == "__main__":
        df_games = fetch_top_100_steam()

        if df_games is not None:
            df_games.to_csv("data/data_raw_steam.csv", index = False)
            print("Dados salvos em 'data/data_raw_steam.csv'")

            print("Amostras dos dados:")
            print(df_games[['name', 'developer', 'price']].head(10))