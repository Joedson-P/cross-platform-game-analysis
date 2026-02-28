import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visuals():
    try:
        df = pd.read_csv('reports/best_deals.csv')
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return

    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = [12, 7]

    top_10 = df.sort_values(by='price_difference', ascending=False).head(10)

    # Preparar dados para o gráfico de barras empilhadas ou agrupadas
    plot_data = top_10.melt(id_vars='name_match', 
                           value_vars=['price_steam', 'price_gog', 'price_epic'],
                           var_name='Loja', value_name='Preço (R$)')
    
    # Limpar nomes das lojas para a legenda
    plot_data['Loja'] = plot_data['Loja'].str.replace('price_', '').str.title()

    plt.figure()
    ax = sns.barplot(data=plot_data, x='Preço (R$)', y='name_match', hue='Loja', palette='viridis')
    plt.title('Comparativo de Preços: Onde o Jogo é Mais Barato?', fontsize=16, pad=20)
    plt.ylabel('Nome do Jogo', fontsize=12)
    plt.xlabel('Preço em Reais (R$)', fontsize=12)
    plt.legend(title='Plataforma', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig('reports/price_comparison_chart.png')
    print("Gráfico de comparação de preços salvo.")

    plt.figure(figsize=(8, 8))
    best_counts = df['best_store'].value_counts()
    
    colors = sns.color_palette('pastel')[0:len(best_counts)]
    plt.pie(best_counts, labels=best_counts.index, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title('Qual loja venceu mais vezes no Preço?', fontsize=16)
    
    plt.savefig('reports/best_store_winrate.png')
    print("Gráfico de 'Win-Rate' das lojas salvo.")

    plt.show()

if __name__ == "__main__":
    generate_visuals()