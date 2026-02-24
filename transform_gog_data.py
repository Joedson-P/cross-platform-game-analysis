import pandas as pd
import ast
import os

def parse_price(price_data):
    try:
        if isinstance(price_data, str):
            price_data = ast.literal_eval(price_data)

        final_price = float(price_data.get('final', '0').replace('R$', ''))
        base_price = float(price_data.get('base', '0').replace('R$', ''))
        discount_str = str(price_data.get('discount', '0'))
        if discount_str.lower() == 'none':
            discount = '0'
        else:
            discount = float(discount_str.replace('%', '').replace('-', '').strip())

        return final_price, base_price, discount   

    except Exception as e:
        print(f"Erro ao processar o preço: {e}. Dados: {price_data}")
        return 0.0, 0.0, 0.0 
    
def normalize_rating(rating):
    return rating * 2
    
def transform_data():
    input_path = 'data/data_raw_gog.csv'
    output_path = 'data/data_processed_gog.csv'

    if not os.path.exists(input_path):
        print("Arquivo não encontrado.")
        return
    
    # Carregando os dados
    df = pd.read_csv(input_path)

    # Tratando os preços
    price_stats = df['price'].apply(parse_price)
    df[['price', 'initialprice', 'discount']] = pd.DataFrame(price_stats.tolist(), index=df.index)

    # Limpeza de listas
    for col in ['developers', 'publishers']:
        df[col] = df[col].str.replace(r"[\[\]']", "", regex=True)

    # Criando a coluna de avaliação normalizada
    df['approval_rate'] = df['reviewsRating'].apply(normalize_rating).round(2)

    # Renomeando colunas para manter consistência
    df_clean = df.rename(columns = {
        'title': 'name',
        'developers': 'developer',
        'publishers': 'publisher',
    })

    # Ordenando pelas avaliações
    df_clean = df_clean.sort_values('approval_rate', ascending=False)

    # Selecionando as colunas relevantes
    cols_to_keep = ['name', 'developer', 'publisher', 'price', 'initialprice', 'discount', 'approval_rate']
    df_final = df_clean[cols_to_keep].copy()

    # Salvando o arquivo processado
    df_final.to_csv(output_path, index=False)
    print(f"Dados transformados e salvos em {output_path}")

    # Exibindo o Top 5 com melhores avaliações
    print("\nTop 5 jogos com melhores avaliações:")
    print(df_final[['name', 'approval_rate', 'price']].head(5))

if __name__ == "__main__":
    transform_data()