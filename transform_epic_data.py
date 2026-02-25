import pandas as pd
import json
import os

def transform_epic_data():
    input_path = 'data/epic_response.json'
    output_path = 'data/data_processed_epic.csv'

    if not os.path.exists(input_path):
        print(f"Erro: O arquivo {input_path} não foi encontrado.")
        return

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    offers = data.get('data', {}).get('Storefront', {}).get('collectionLayout', {}).get('collectionOffers', [])

    processed_games = []

    for game in offers:
        # Tratando os preços
        price_info = game.get('price', {}).get('totalPrice', {})
        decimals = price_info.get('currencyInfo', {}).get('decimals', 2)
        divisor = 10 ** decimals
        final_price = price_info.get('discountPrice', 0) / divisor
        initial_price = price_info.get('originalPrice', 0) / divisor
        discount_perc = 0
        if initial_price > 0:
            discount_perc = round((initial_price - final_price) / initial_price * 100, 0)

        # Buscando o desenvolvedor
        developer = game.get('developerDisplayName')
        if not developer:
            developer = game.get('seller', {}).get('name')
            if not developer:
                for attribute in game.get('customAttributes', []):
                    if attribute.get('key') == 'developerName':
                        developer = attribute.get('value')
                        break

        processed_games.append({
            'name': game.get('title'),
            'developer': developer or 'Unknown',
            'publisher': game.get('publisherDisplayName') or 'Unknown',
            'price': round(final_price, 2),
            'initialprice': round(initial_price, 2),
            'discount': int(discount_perc),
            'approval_rate': None  # Epic não fornece publicamente no catálogo
        })

    # Criando o DataFrame
    df_epic =  pd.DataFrame(processed_games)

    # Salvando o arquivo processado
    df_epic.to_csv(output_path, index=False)
    print(f"Dados transformados e salvos em {output_path}")

    # Exibindo resumo dos dados processados
    print("\nResumo dos dados processados:")
    print(df_epic[['name', 'developer', 'price', 'discount']].head())

if __name__ == "__main__":
    transform_epic_data()