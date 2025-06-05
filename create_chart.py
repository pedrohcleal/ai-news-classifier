import plotly.express as px
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Carregar os dados do JSON
with open('analises_2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Converter para DataFrame
df = pd.DataFrame(data)

# Converter a coluna de data para datetime
df['dt_pub_noticia'] = pd.to_datetime(df['dt_pub_noticia'])

# Lista de empresas únicas
empresas = df['empresa'].unique()

def plot_empresa(empresa):
    # Filtrar dados da empresa
    df_empresa = df[df['empresa'] == empresa].copy()

    # Converter e ordenar por data
    df_empresa['mes'] = df_empresa['dt_pub_noticia'].dt.to_period('M')
    df_empresa = df_empresa.sort_values('dt_pub_noticia')

    # Agrupar por mês e calcular médias de sense
    df_sense = df_empresa.groupby('mes').agg({
        'sense_title': 'mean',
        'sense_description': 'mean'
    }).reset_index()
    df_sense['mes'] = df_sense['mes'].astype(str)

    size = (16,6)
    # Gráfico de linha para SENSE
    plt.figure(figsize=size)
    plt.plot(df_sense['mes'], df_sense['sense_title'], marker='o', label='Sense Title')
    plt.plot(df_sense['mes'], df_sense['sense_description'], marker='o', label='Sense Description')
    plt.title(f'Evolução do sentimento de notícias para {empresa}')
    plt.xlabel('Mês')
    plt.ylabel('Sentimento (mais negativo) 1-5 (mais positivo)')
    plt.ylim(0, 6)
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig(f'frequencia_Sense-{empresa}.png', dpi=300, bbox_inches='tight')

    # ---------- Frequência mensal histórica para class_title ----------
    df_title_freq = df_empresa.groupby(['mes', 'class_title']).size().reset_index(name='frequencia')
    df_title_freq['mes'] = df_title_freq['mes'].astype(str)
    pivot_title = df_title_freq.pivot(index='mes', columns='class_title', values='frequencia').fillna(0)

    classes_title = pivot_title.columns.tolist()
    n_classes_title = len(classes_title)
    colors_title = cm.get_cmap('tab20', n_classes_title)  # até 20 cores

    plt.figure(figsize=size)
    for i, cls in enumerate(classes_title):
        plt.plot(pivot_title.index, pivot_title[cls], marker='o', label=cls, color=colors_title(i))
    plt.title(f'Frequência mensal de categorias do título de notícias para {empresa}')
    plt.xlabel('Mês')
    plt.ylabel('Frequência da categoria')
    plt.xticks(rotation=45)
    plt.legend(title='Class Title', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # ---------- Frequência mensal histórica para class_description ----------
    # df_desc_freq = df_empresa.groupby(['mes', 'class_description']).size().reset_index(name='frequencia')
    # df_desc_freq['mes'] = df_desc_freq['mes'].astype(str)
    # pivot_desc = df_desc_freq.pivot(index='mes', columns='class_description', values='frequencia').fillna(0)

    # classes_desc = pivot_desc.columns.tolist()
    # n_classes_desc = len(classes_desc)
    # colors_desc = cm.get_cmap('tab20', n_classes_desc)

    # plt.figure(figsize=size)
    # for i, cls in enumerate(classes_desc):
    #     plt.plot(pivot_desc.index, pivot_desc[cls], marker='o', label=cls, color=colors_desc(i))
    # plt.title(f'Frequência mensal de categorias da descrição de notícias para {empresa}')
    # plt.xlabel('Mês')
    # plt.ylabel('Frequência da categoria')
    # plt.xticks(rotation=45)
    # plt.legend(title='Class Description', bbox_to_anchor=(1.05, 1), loc='upper left')
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()


# Gerar gráficos para cada empresa
for empresa in empresas:
    print(f"\nAnálise para a empresa: {empresa}")
    plot_empresa(empresa)
