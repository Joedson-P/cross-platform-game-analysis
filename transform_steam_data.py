import pandas as pd
import os

def parse_owners(owners_str):
    try:
        low, high = owners_str.replace(',', '').split(' .. ')
        return (int(low) + int(high)) / 2
    except:
        return 0

def transform_data():
    input_path = 'data/data_raw_steam.csv'
    output_path = 'data/data_processed_steam.csv'

    if not os.path.exists(input_path):
        print(f"Arquivo {input_path} não encontrado.")
        return
    
    # Carregando os dados
    df = pd.read_csv(input_path)

    # Tratando os preços
    df[['price', 'initialprice']] = df[['price', 'initialprice']] / 100  # Convertendo de centavos para dólares

    # Criando Taxa de Aprovação (Score de 0 a 100)
    df['total_reviews'] = df['positive'] + df['negative']
    df['approval_rate'] = (df['positive'] / df['total_reviews'] * 100).round(2)
    df['approval_rate'] = df['approval_rate'].fillna(0)

    # Aplicando a função auxiliar
    df['owners_midpoint'] = df['owners'].apply(parse_owners)

    # Selecionando as colunas relevantes
    cols_to_keep = ['name', 'developer', 'publisher', 'price', 'initialprice', 'discount', 'ccu', 'positive',
                    'owners_midpoint','approval_rate', 'average_2weeks']
    df_clean = df[cols_to_keep].copy()

    # Ordenando pelas avaliações (com pelo menos 1000 avaliações)
    df_clean = df_clean[df_clean['positive'] >= 1000].sort_values('approval_rate', ascending=False)

    # Salvando o arquivo processado
    df_clean.to_csv(output_path, index=False)
    print(f"Dados transformados e salvos em {output_path}")

    # Exibindo o Top 5 com melhores avaliações
    print("\nTop 5 jogos com melhores avaliações:")
    print(df_clean[['name', 'approval_rate', 'price']].head(5))

if __name__ == "__main__":
    transform_data()