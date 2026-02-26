import pandas as pd
import re
import os

def clean_game_name(text):
    if not text: return ""
    text = text.lower()

    # Mapeando números romanos para arábicos
    romans = {' iii': ' 3', ' ii': ' 2', ' iv': ' 4', ' v': ' 5', ' vi': ' 6', ' vii': ' 7', ' viii': ' 8', ' ix': ' 9', ' x': ' 10'}
    for rom, ara in romans.items():
        text = text.replace(rom, ara)

    # Removendo termos comuns que não são essenciais para a identificação do jogo
    terms_to_remove = [
        'edition', 'standard', 'enhanced', 'complete', 'gold', 'ultimate', 'deluxe', 'anthology', 'pack',
        'bundle', 'premium', 'director\'s cut', 'game of the year', 'goty', 'remastered', 'definitive', 'special',
        'anniversary', 'remake', 'collector\'s'
    ]
    for term in terms_to_remove:
        text = text.replace(term, '')

    # Removendo símbolos e caracteres especiais
    text = re.sub(r'[^a-z0-9\s]', '', text)

    # Removendo espaços extras
    return " ".join(text.split())

def run_global_analysis():
    steam = pd.read_csv('data/data_processed_steam.csv')
    gog = pd.read_csv('data/data_processed_gog.csv')
    epic = pd.read_csv('data/data_processed_epic.csv')

    # Adicionando identificador de loja antes de unir
    steam['store'] = 'Steam'
    gog['store'] = 'GOG'
    epic['store'] = 'Epic'

    stores_summary = []
    for df, name in zip([steam, gog, epic], ['Steam', 'GOG', 'Epic']):
        stores_summary.append({
            'Loja': name,
            'Total Jogos': len(df),
            'Preço Médio (R$)': round(df['price'].mean(), 2),
            'Desconto Médio (%)': round(df['discount'].mean(), 1),
            'Maior Desconto (%)': df['discount'].max()
        })
    
    df_market_share = pd.DataFrame(stores_summary)
    print("\n--- 📊 RESUMO GERAL DO MERCADO ---")
    print(df_market_share.to_string(index=False))

    # Normalização dos nomes para facilitar o cruzamento
    for df in [steam, gog, epic]:
        df['name_match'] = df['name'].apply(clean_game_name)

    # Criando o DataFrame Unificado
    merged = pd.merge(
        steam[['name_match', 'name','developer','publisher','price','initialprice','discount','ccu','positive','owners_midpoint','approval_rate','average_2weeks']], 
        gog[['name_match', 'name','developer','publisher','price','initialprice','discount','approval_rate']], 
        on='name_match', how='outer', suffixes=('_steam', '_gog')
    )
    
    final_df = pd.merge(
        merged, 
        epic[['name_match', 'name','developer','publisher','price','initialprice','discount','approval_rate']], 
        on='name_match', how='outer'
    )

    final_df = final_df.rename(columns={
        'price': 'price_epic', 'discount': 'discount_epic',
        'approval_rate': 'approval_rate_epic',
        'name': 'name_epic', 'developer': 'developer_epic',
        'publisher': 'publisher_epic', 'initialprice': 'initialprice_epic'
        })
    
    # Salvando o dataset unificado
    os.makedirs('reports', exist_ok=True)
    final_df.to_csv('reports/unified_prices.csv', index=False)

    # Relatório de cruzamentos
    matches_steam_gog = final_df[final_df['price_steam'].notna() & final_df['price_gog'].notna()]
    matches_steam_epic = final_df[final_df['price_steam'].notna() & final_df['price_epic'].notna()]
    matches_triple = final_df[final_df['price_steam'].notna() & final_df['price_gog'].notna() & final_df['price_epic'].notna()]

    print("\n--- 🤝 RELATÓRIO DE COINCIDÊNCIAS (MATCHES) ---")
    print(f"Jogos comuns Steam & GOG:  {len(matches_steam_gog)}")
    print(f"Jogos comuns Steam & Epic: {len(matches_steam_epic)}")
    print(f"Jogos comuns nas 3 lojas:  {len(matches_triple)}")
    
    print("\nRelatório detalhado salvo em: reports/unified_prices.csv")

if __name__ == "__main__":
    run_global_analysis()