import pandas as pd
import numpy as np

def find_best_deals(df):
    try:
        df = pd.read_csv('reports/unified_prices.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return

    price_cols = ['price_steam', 'price_gog', 'price_epic']
    df['stores_count'] = df[price_cols].notna().sum(axis=1)

    comparables = df[df['stores_count'] > 1].copy()

    if comparables.empty:
        print("Nenhum jogo disponível em mais de uma plataforma.")
        return

    comparables['best_price'] = comparables[price_cols].min(axis=1)

    # Identificar a plataforma com o melhor preço
    def idenfity_best_store(row):
        stores = []
        if row['price_steam'] == row['best_price']:
            stores.append('Steam')
        if row['price_gog'] == row['best_price']:
            stores.append('GOG')
        if row['price_epic'] == row['best_price']:
            stores.append('Epic Games')
        return " & ".join(stores)
    
    comparables['best_store'] = comparables.apply(idenfity_best_store, axis=1)

    # Calculando a diferença de preço entre a melhor oferta e as outras
    comparables['max_price'] = comparables[price_cols].max(axis=1)
    comparables['price_difference'] = comparables['max_price'] - comparables['best_price']

    # Exibindo rankings dos melhores negócios
    print(f"Comparativo de preços: {len(comparables)} jogos disponíveis em mais de uma plataforma.")

    top_savings = comparables.sort_values(by='price_difference', ascending=False).head(10)
    print(f"{'Jogo':<30} {'Melhor Preço':<15} {'Plataforma(s)':<10} {'Diferença de Preço':<10}")
    print("-" * 70)

    for _, row in top_savings.iterrows():
        print(f"{str(row['name_match'])[:30]:<30} | R${row['best_price']:>7.2f} | {row['best_store']:<15} | R${row['price_difference']:<10.2f}")

    # Salvando as recomendações
    comparables.to_csv('reports/best_deals.csv', index=False)
    print("Recomendações de melhores ofertas salvas.")

if __name__ == "__main__":
    find_best_deals(None)