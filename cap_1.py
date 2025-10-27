#%%
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.ticker as mticker
from matplotlib.ticker import FuncFormatter

#%%Preparo dos dados
df = pd.read_csv(r"D:\FLP\Mestrado\etapa_1\data\areas_rix_fire_lulc_year_v2.csv")

df = df.drop(columns=['.geo', 'system:index'])

municipality_code_to_name = { 
    1500602: 'Altamira',
    1505650: 'Placas',
    1508159: 'Uruará',
    1504455: 'Medicilândia',
    1501725: 'Brasil Novo',
    1505908: 'Porto de Moz',
    1508357: 'Vitória do Xingu',
    1507805: 'Senador José Porfírio',
    1500859: 'Anapu',
    1505486: 'Pacajá'
}

id_to_class = {
    3: 'Formação Florestal',
    4: 'Formação Savânica',
    9: 'Silvicultura',
    11: 'Campo Alagado e Área Pantanosa',
    12: 'Formação Campestre',
    15: 'Pastagem',
    24: 'Área Urbanizada',
    29: 'Afloramento Rochoso',
    30: 'Mineração',
    33: "Corpo D'água",
    39: 'Soja',
    41: 'Outras Lavouras Temporárias',
    48: 'Outras Lavouras Perenes'
}

id_to_lev1 = {
    'Formação Florestal': 'Natural',
    'Formação Savânica': 'Natural',
    'Silvicultura': 'Antrópico',
    'Campo Alagado e Área Pantanosa': 'Natural',
    'Formação Campestre': 'Natural',
    'Pastagem': 'Antrópico',
    'Soja': 'Antrópico',
    'Outras Lavouras Temporárias': 'Antrópico',
    'Outras Lavouras Perene': 'Antrópico'
}

df['NM_MUN'] = df['CD_MUN_NUM'].map(municipality_code_to_name)

df['class_name'] = df['class'].map(id_to_class)

df['class_lev1'] = df['class_name'].map(id_to_lev1)

print(df.head())

#%% Distribuição Anual

df_fire_year = df.groupby('year')['area'].sum().reset_index()

# Cálculo da média
media_area_queimada = df_fire_year["area"].mean()

# Cálculo da tendência linear
slope, intercept, r_value, p_value, std_err = stats.linregress(df_fire_year.index, df_fire_year["area"])

# Adicionando a tendência linear ao DataFrame
df_fire_year['trend'] = intercept + slope * df_fire_year.index

# Configurando a fonte globalmente
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# Plotando os dados, a tendência e a linha da média
ax = plt.figure(figsize=(10, 6))
plt.plot(df_fire_year["year"], df_fire_year["area"], label='Área Queimada (km²)', marker='o', color='red')
plt.plot(df_fire_year["year"], df_fire_year["trend"], label='Tendência Linear', linestyle='--', color='black')
plt.axhline(y=media_area_queimada, color='blue', linestyle='-', label='Média Área Queimada')

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

plt.xlabel('Ano')
plt.ylabel('Área Queimada (km²)')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Retornando valores para análise de tendência
slope, intercept, r_value**2, p_value

#%%
df_fire_month = pd.read_csv(r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\areas_month_rix_fire_lulc_year.csv")

df_fire_month = df_fire_month.drop(columns=['.geo', 'system:index'])

month = {
    1: 'Jan',
    2: 'Fev',
    3: 'Mar',
    4: 'Abr',
    5: 'Mai',
    6: 'Jun',
    7: 'Jul',
    8: 'Ago',
    9: 'Set',
    10: 'Out',
    11: 'Nov',
    12: 'Dez'
}

df_fire_month['month'] = df_fire_month['class'].map(month)

df_fire_month = df_fire_month.groupby(['year', 'month'])['area'].sum().reset_index()

df_fire_month['area'] = df_fire_month['area'].round(4)
print(df_fire_month.head)

df_soi_index = pd.read_csv(r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\soi_index_adjusted.csv")

soi_month = {
    'JAN': 'Jan',
    'FEB': 'Fev',
    'MAR': 'Mar',
    'APR': 'Abr',
    'MAY': 'Mai',
    'JUN': 'Jun',
    'JUL': 'Jul',
    'AUG': 'Ago',
    'SEP': 'Set',
    'OCT': 'Out',
    'NOV': 'Nov',
    'DEC': 'Dez'
}

df_soi_index['month'] = df_soi_index['month'].map(soi_month)

print(df_soi_index.head())

df_soi_fire = pd.merge(df_fire_month, df_soi_index, on=['year', 'month'], how='left')

print(df_soi_fire)

#%% Gráfico Mensal

df_fire_month_grouped = df_fire_month.groupby('month')['area'].sum().reset_index()
total_area_yearly = df_fire_month_grouped['area'].sum()
df_fire_month_grouped['percentage'] = (df_fire_month_grouped['area'] / total_area_yearly) * 100

month_id = {
    'Jan': 1,
    'Fev': 2,
    'Mar': 3,
    'Abr': 4,
    'Mai': 5,
    'Jun': 6,
    'Jul': 7,
    'Ago': 8,
    'Set': 9,
    'Out': 10,
    'Nov': 11,
    'Dez': 12 
}
# Configurando a fonte globalmente
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')


df_fire_month_grouped['month_id'] = df_fire_month_grouped['month'].map(month_id)
df_fire_month_grouped.sort_values('month_id', inplace=True)

# Configurando a fonte para Times New Roman, tamanho 12
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

fig, ax1 = plt.subplots(figsize=(14, 10))
sns.barplot(x='month', y='area', data=df_fire_month_grouped, color='red', ax=ax1)
ax1.set_xlabel('Mês')
ax1.set_ylabel('Área Queimada (km²)')

# Adicionando etiquetas com porcentagens e valores
for i, (index, row) in enumerate(df_fire_month_grouped.iterrows()):
    ax1.text(i, row['area'], f"{row['area']/1000:.2f}k\n({row['percentage']:.2f}%)", color='black', ha="center", va='bottom')

# Ajuste do formato do eixo Y para utilizar ponto como separador de milhar
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))

plt.tight_layout()
plt.show()

#%% % Fogo - Mês - Ano (%)
# Calculando o total de área queimada por ano
total_area_per_year = df_fire_month.groupby('year')['area'].transform('sum')

# Calculando a porcentagem da área por mês em relação ao total anual
df_fire_month['percentage'] = (df_fire_month['area'] / total_area_per_year) * 100

df_fire_month['month_id'] = df_fire_month['month'].map(month_id)
df_fire_month.sort_values('month_id', inplace=True, ascending=True)

# Criando um DataFrame com todas as combinações possíveis de anos e meses
years = df_fire_month['year'].unique()
months = range(1, 13)  # 1 a 12 para representar todos os meses
month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Criando uma lista com todas as combinações possíveis de ano e mês
from itertools import product
all_combinations = list(product(years, months))

# Convertendo para DataFrame
all_comb_df = pd.DataFrame(all_combinations, columns=['year', 'month_id'])

# Mesclando com o df_fire_month original
# Isso garante que todos os meses de cada ano estejam presentes, mesmo que não haja dados
df_fire_month_full = pd.merge(all_comb_df, df_fire_month, on=['year', 'month_id'], how='left')

# Preenchendo os valores NaN com 0
df_fire_month_full['area'].fillna(0, inplace=True)
df_fire_month_full['percentage'].fillna(0, inplace=True)  # Assumindo que 'percentage' também precisa ser ajustado

# Garantindo que os nomes dos meses estejam presentes (opcional, depende do seu uso)
df_fire_month_full['month'] = df_fire_month_full['month_id'].apply(lambda x: month_names[x-1])

# Ordenando os dados para melhor visualização
df_fire_month_full.sort_values(by=['year', 'month_id'], inplace=True)

# Criando a figura
fig, ax = plt.subplots(figsize=(25, 10))

# Plotando o heatmap com a ordem invertida para os valores do eixo y e usando o gradiente de cores "Reds"
sns.heatmap(data=df_fire_month_full.pivot_table(index="month_id", columns="year", values="percentage")[::-1],
            annot=True, fmt=".0f", cmap="Reds", ax=ax, cbar_kws={'label': 'Área Queimada (%)'})

# Definindo labels
ax.set_xlabel("Ano")
ax.set_ylabel("Mês")

# Ajustando os labels do eixo y para mostrar os nomes dos meses na ordem correta após a inversão
# Supondo que você tenha um dicionário ou lista que mapeia month_id para nomes de meses, por exemplo, month_names
month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
ax.set_yticklabels(month_names[::-1])

# Rotacionando labels do eixo x
plt.xticks(rotation=45)

# Adicionando título
plt.title("Área Queimada Mensal")

# Mostrando o gráfico
plt.show()


#%% km2 Fogo - Mês - Ano

df_fire_month['month_id'] = df_fire_month['month'].map(month_id)
df_fire_month.sort_values('month_id', inplace=True, ascending=True)

# Criando um DataFrame com todas as combinações possíveis de anos e meses
years = df_fire_month['year'].unique()
months = range(1, 13)  # 1 a 12 para representar todos os meses
month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Criando uma lista com todas as combinações possíveis de ano e mês
from itertools import product
all_combinations = list(product(years, months))

# Convertendo para DataFrame
all_comb_df = pd.DataFrame(all_combinations, columns=['year', 'month_id'])

# Mesclando com o df_fire_month original
# Isso garante que todos os meses de cada ano estejam presentes, mesmo que não haja dados
df_fire_month_full = pd.merge(all_comb_df, df_fire_month, on=['year', 'month_id'], how='left')

# Preenchendo os valores NaN com 0
df_fire_month_full['area'].fillna(0, inplace=True)
df_fire_month_full['area'].fillna(0, inplace=True)  # Assumindo que 'percentage' também precisa ser ajustado

# Garantindo que os nomes dos meses estejam presentes (opcional, depende do seu uso)
df_fire_month_full['month'] = df_fire_month_full['month_id'].apply(lambda x: month_names[x-1])

# Ordenando os dados para melhor visualização
df_fire_month_full.sort_values(by=['year', 'month_id'], inplace=True)

# Criando a figura
fig, ax = plt.subplots(figsize=(25, 10))

# Plotando o heatmap com a ordem invertida para os valores do eixo y e usando o gradiente de cores "Reds"
sns.heatmap(data=df_fire_month_full.pivot_table(index="month_id", columns="year", values="area")[::-1],
            annot=True, fmt=".0f", cmap="Reds", ax=ax, cbar_kws={'label': 'Área Queimada km²)'})

# Definindo labels
ax.set_xlabel("Ano")
ax.set_ylabel("Mês")

# Ajustando os labels do eixo y para mostrar os nomes dos meses na ordem correta após a inversão
# Supondo que você tenha um dicionário ou lista que mapeia month_id para nomes de meses, por exemplo, month_names
month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
ax.set_yticklabels(month_names[::-1])

# Rotacionando labels do eixo x
plt.xticks(rotation=45)

# Adicionando título
plt.title("Área Queimada Mensal")

# Mostrando o gráfico
plt.show()

#%% Uso e Cobertura
# Agrupando os dados por ano e classe de uso e cobertura do solo
area_por_classe_ano = df.pivot_table(values='area', index='year', columns='class_name', aggfunc='sum', fill_value=0)

# Definindo a ordem específica e as cores para cada classe de uso e cobertura do solo
ordem_classes = [
    'Formação Florestal', 
    'Formação Campestre', 
    'Campo Alagado e Área Pantanosa', 
    'Formação Savânica', 
    'Outras Lavouras Perenes', 
    'Outras Lavouras Temporárias', 
    'Pastagem', 
    'Silvicultura', 
    'Soja'
]

cores_classes = {
    'Formação Florestal': '#1f8d49',
    'Formação Campestre': '#d6bc74',
    'Campo Alagado e Área Pantanosa': '#519799',
    'Formação Savânica': '#7dc975',
    'Outras Lavouras Perenes': '#e6ccff',
    'Outras Lavouras Temporárias': '#f54ca9',
    'Pastagem': '#edde8e',
    'Silvicultura': '#7a5900',
    'Soja': '#f5b3c8', 
    'Agricultura': '#E974ED',
    'Área Urbanizada': '#d4271e',
    "Corpo Dágua": '#0000FF',
    'Afloramento Rochoso':'#ffaa5f',
    'Mineração': '#9c0027'
}

# Configurando a fonte globalmente
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

# Reorganizando as colunas do DataFrame de acordo com a ordem definida
area_por_classe_ano_ordenado = area_por_classe_ano[ordem_classes]

# Gerando o gráfico de barras empilhadas
fig, ax = plt.subplots(figsize=(18, 10))
area_por_classe_ano_ordenado.plot(kind='bar', stacked=True, color=[cores_classes[col] for col in ordem_classes], ax=ax)

# Formatando o eixo y para usar ponto como separador de milhar
ax.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))

plt.xlabel('Ano')
plt.ylabel('Área Queimada (km²)')
# Ajustando a legenda para 2 linhas centralizadas
leg = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=int(len(ordem_classes)/2 + 0.5), frameon=False)
leg.set_title(None)  # Removendo o título da legenda
plt.tight_layout()

plt.show()

#%% Uso do Solo Normalizado
# Normalizando os dados para que cada coluna empilhada some 100%
area_normalizada = area_por_classe_ano_ordenado.div(area_por_classe_ano_ordenado.sum(axis=1), axis=0) * 100

# Configurando a fonte globalmente
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

# Gerando o gráfico de barras empilhadas normalizado com a legenda ajustada para 2 linhas centralizadas abaixo do gráfico
fig, ax = plt.subplots(figsize=(18, 10))
area_normalizada.plot(kind='bar', stacked=True, color=[cores_classes[col] for col in ordem_classes], ax=ax)

plt.xlabel('Ano', fontname='Times New Roman')
plt.ylabel('Percentual da Área Queimada (%)', fontname='Times New Roman')
# Ajustando a legenda para 2 linhas centralizadas
leg = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=int(len(ordem_classes)/2 + 0.5), frameon=False)
leg.set_title(None)  # Removendo o título da legenda

for text in leg.get_texts():
    text.set_fontname('Times New Roman')

# Ajustando a fonte dos valores dos eixos para Times New Roman
for tick in ax.get_xticklabels():
    tick.set_fontname('Times New Roman')
for tick in ax.get_yticklabels():
    tick.set_fontname('Times New Roman')


plt.tight_layout()

plt.show()

# %% Gráfico Rosca Uso e Cobertura do Solo
class_name_custom = {
    "Campo Alagado e Área Pantanosa": "Campo Alagado e Área Pantanosa",
    "Formação Campestre": "Formação Campestre",
    "Formação Florestal": "Formação Florestal",
    "Formação Savânica": "Formação Savânica",
    "Pastagem": "Pastagem",
    "Soja": "Outros Usos Agropecuários",
    "Silvicultura": "Outros Usos Agropecuários",
    "Outras Lavouras Perenes": "Outros Usos Agropecuários",
    "Outras Lavouras Temporárias": "Outros Usos Agropecuários"
}

# Criar um DataFrame a partir dos dados fornecidos
df['class_name_v2'] = df['class_name'].map(class_name_custom)

df_grouped_by_class = df.groupby(['class_name_v2'])['area'].sum().reset_index()

# Cores personalizadas para cada classe
colors_custom = {
    "Campo Alagado e Área Pantanosa": "#519799",
    "Formação Campestre": "#d6bc74",
    "Formação Florestal": "#1f8d49",
    "Formação Savânica": "#7dc975",
    "Pastagem": "#edde8e",
    "Outros Usos Agropecuários": "#FFFFB2"
}

# Função de formatação personalizada para autopct que usa vírgula como separador decimal
def autopct_format(values):
    def my_format(pct):
        return '{v:,}'.format(v=pct.round(1)).replace('.', ',') + '%'
    return my_format
    
# Definir as configurações da fonte para usar em todo o gráfico
font_settings = {'family': 'Times New Roman', 'size': 12}
plt.rc('font', **font_settings)

# Criar o gráfico de rosca com as configurações de fonte ajustadas
plt.figure(figsize=(10, 6))
patches, texts, autotexts = plt.pie(df_grouped_by_class['area'], labels=df_grouped_by_class['class_name_v2'], autopct=autopct_format(df_grouped_by_class['area']),
                                    startangle=180, pctdistance=0.85, colors=[colors_custom[label] for label in df_grouped_by_class['class_name_v2']],
                                    wedgeprops=dict(width=0.4))

# Ajustar a fonte para Times New Roman, tamanho 12 para todos os textos
for text in texts + autotexts:
    text.set_fontsize(12)
    text.set_fontname('Times New Roman')

# Desenhar um círculo no centro para tornar o gráfico um gráfico de rosca
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()


# %% Gráfico Precipitação Área Queimada

precipitation_df = pd.read_csv(r'C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\mean_precipitation_rix_1985_2022.csv')

# Agrupar os dados somente por 'year', somando as áreas, para corresponder aos dados de precipitação
total_area_by_year_df = df.groupby('year')['area'].sum().reset_index()

# Unir os conjuntos de dados com base em 'year'
merged_df = pd.merge(total_area_by_year_df, precipitation_df[['year', 'precipitation']], on='year', how='inner')

# Selecionar as colunas de interesse: 'year', 'precipitation', e 'area'
final_df = merged_df[['year', 'precipitation', 'area']]

# Exibir as primeiras linhas do dataframe final
final_df.head()

# Configurar o gráfico com estilos mais avançados
fig, ax1 = plt.subplots(figsize=(12, 7))

# Melhorar a aparência com seaborn
sns.set_style("whitegrid")

# Definição da fonte (você precisará definir 'font_path' caso o try acima falhe)
plt.rcParams['font.family'] = 'Times New Roman'  

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

# Eixo para 'area'
color = 'tab:red'
ax1.set_xlabel('Ano', fontsize=12)  
ax1.set_ylabel('Área Queimada(km²)', color=color, fontsize=12) 
lns1 = ax1.plot(final_df['year'], final_df['area'], color=color, label='Área (km²)', marker='o', linestyle='-')
ax1.tick_params(axis='y', labelcolor=color, labelsize=12)
ax1.tick_params(axis='x', labelsize=12)

# Eixo para 'precipitation'
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Precipitação (mm)', color=color, fontsize=12)  
lns2 = ax2.plot(final_df['year'], final_df['precipitation'], color=color, label='Precipitação (mm)', linestyle='--')
ax2.tick_params(axis='y', labelcolor=color, labelsize=12)

# Combinar legendas
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
plt.legend(lns, labs, loc='upper center',bbox_to_anchor=(0.5, -0.1), fontsize=12, frameon=False)

# Formatando o eixo y para usar ponto como separador de milhar
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))


# Mostrar o gráfico
plt.show()

#%% Extensão

acumulado = pd.read_csv(r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\freq_rix_1985_2022_v2.csv")

acumulado['freq'] = acumulado['class'].divide(100).astype(int)

acumulado['territory'] = acumulado['territory'].astype(int)

acumulado['class_id'] = acumulado['class'].mod(100)

acumulado = acumulado.drop(columns=['system:index', '.geo', 'class'])

fire_extension_by_year = acumulado.groupby(['year'])['area'].sum().reset_index()

print(fire_extension_by_year.head())

# Configurando as fontes para Times New Roman, tamanho 12
matplotlib.rcParams['font.family'] = 'Times New Roman'
matplotlib.rcParams['font.size'] = 12

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

# Usando Python e Pandas para gerar um gráfico de área acumulada
ax = fire_extension_by_year.plot(kind='area', x='year', y='area', figsize=(12, 6), alpha=0.4, color='red', label='Extensão Área Queimada')

plt.xlabel('Ano')

plt.ylabel('Área Queimada (km²)')
plt.grid(False)
plt.xticks(rotation=45, fontname='Times New Roman', fontsize=12)

plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)

# Formatando o eixo y para usar ponto como separador de milhar
ax.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))

plt.show()

#%% Uso do Solo
use_land_file = pd.read_csv(r'C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\areas_lulc_rix_1985_2022.csv')

use_land = use_land_file.drop(columns=['system:index', '.geo'])

use_land = use_land.groupby(['year', 'class'])['area'].sum().reset_index()

use_land['class_name'] = use_land['class'].map(id_to_class)

print(use_land.head())

# Definindo uma função para formatar o eixo y
def formatador(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

formatter = FuncFormatter(formatador)

# Agrupando as categorias especificadas em 'Agricultura'
categorias_agricultura = ['Outras Lavouras Temporárias', 'Outras Lavouras Perenes', 'Soja', 'Silvicultura']
dados_agrupados = use_land.copy()
dados_agrupados['class_name'] = dados_agrupados['class_name'].apply(lambda x: 'Agricultura' if x in categorias_agricultura else x)

# Pivotando os dados novamente com o agrupamento atualizado
dados_pivot_agrupados = dados_agrupados.pivot_table(values='area', index='year', columns='class_name', aggfunc='sum')

# Criando o gráfico de linha com ajustes de legenda e cor
plt.figure(figsize=(12, 8))
for coluna in dados_pivot_agrupados.columns:
    plt.plot(dados_pivot_agrupados.index, dados_pivot_agrupados[coluna], label=coluna, color=cores_classes.get(coluna, 'gray'))

plt.xlabel('Ano', fontdict={'fontname': 'Times New Roman', 'fontsize': 12})
plt.ylabel('Área (km²)', fontdict={'fontname': 'Times New Roman', 'fontsize': 12})
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5, fontsize=12, title_fontsize=12, frameon=False)
plt.grid(False)
plt.gca().yaxis.set_major_formatter(formatter)
plt.xticks(rotation=45, fontname='Times New Roman', fontsize=12)
plt.yticks(fontname='Times New Roman', fontsize=12)
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajustando para a legenda não sobrepor o gráfico

# Formatando o eixo y para usar ponto como separador de milhar
ax.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))

plt.show()

#%% Recorrencia de Queimada
rec_fire = pd.read_csv(r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\freq_rix_1985_2022_v2.csv")

rec_fire['freq'] = rec_fire['class'].divide(100).astype(int)

rec_fire['territory'] = rec_fire['territory'].astype(int)

rec_fire['class_id'] = rec_fire['class'].mod(100)

rec_fire = rec_fire.drop(columns=['system:index', '.geo', 'class'])

rec_fire_2022 = rec_fire.query('year == 2022')

rec_fire_2022 = rec_fire_2022.groupby(['freq', 'class_id'])['area'].sum().reset_index()

rec_fire_2022['class_name'] = rec_fire_2022['class_id'].map(id_to_class)

total_area_km2 = rec_fire_2022['area'].sum()

print(total_area_km2)

# Definir a fonte para Times New Roman, tamanho 12
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Times New Roman',
    'font.size': 12
})

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

formatter = FuncFormatter(formatador)

# Categorizar frequências acima de 10 como "Acima de 10"
rec_fire_2022['freq_category'] = rec_fire_2022['freq'].apply(lambda x: 'Acima de 10' if x > 10 else str(x))

# Agrupar os dados pela nova categoria 'freq_category'
grouped_data_new = rec_fire_2022.groupby('freq_category').agg({'area':'sum'}).reset_index()
grouped_data_new['percent_of_total_area'] = (grouped_data_new['area'] / grouped_data_new['area'].sum()) * 100

# Ordenar os dados para a plotagem
grouped_data_new['freq_category'] = pd.Categorical(grouped_data_new['freq_category'], categories=list(map(str, range(1, 11))) + ['Acima de 10'], ordered=True)
grouped_data_new = grouped_data_new.sort_values('freq_category')

# Configurar cores usando o mapa de cores YlOrBr
colors = cm.YlOrBr(np.linspace(0.3, 0.9, len(grouped_data_new)))

# Criar figura e eixo para o gráfico de barras
fig, ax1 = plt.subplots(figsize=(10, 5))

# Plotar as barras para a área
bars = ax1.bar(grouped_data_new['freq_category'], grouped_data_new['area'], color=colors, label='Área (km²)')
ax1.set_xlabel('Recorrência')
ax1.set_ylabel('Área Queimada (km²)')
ax1.tick_params(axis='y')

# Criar eixo secundário para as porcentagens
ax2 = ax1.twinx()
ax2.plot(grouped_data_new['freq_category'], grouped_data_new['percent_of_total_area'], color='red', marker='o', linestyle='-', label='Porcentagem do total')
ax2.set_ylabel('Porcentagem (%)')
ax2.tick_params(axis='y')

# Ajustar o posicionamento dos rótulos de porcentagem
for i, txt in enumerate(grouped_data_new['percent_of_total_area']):
    ax2.annotate(f'{txt:.2f}%', 
                 (grouped_data_new['freq_category'][i], grouped_data_new['percent_of_total_area'][i]),
                 textcoords="offset points", 
                 xytext=(0,5), 
                 ha='center')
    
plt.tight_layout()

# Formatando o eixo y para usar ponto como separador de milhar
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))

plt.show()

#%% Recorrencia por Uso

# Substituir os nomes das classes específicas por 'Agricultura'
rec_fire_2022['class_name_aggregated'] = rec_fire_2022['class_name'].replace({
    'Outras Lavouras Temporárias': 'Agricultura',
    'Outras Lavouras Perenes': 'Agricultura',
    'Soja': 'Agricultura',
    'Silvicultura': 'Agricultura'
})

# Agrupar freq maiores que 10 em 'maior que 10'
rec_fire_2022['freq_aggregated'] = rec_fire_2022['freq'].apply(lambda x: 'Acima de 10' if x > 10 else str(x))

# Assegurar que os valores de 'freq_aggregated' estejam ordenados corretamente
rec_fire_2022['freq_aggregated'] = pd.Categorical(rec_fire_2022['freq_aggregated'], categories=[str(x) for x in range(1, 11)] + ['Acima de 10'], ordered=True)

# Agrupar os dados por 'class_name_aggregated' e 'freq_aggregated', somando a área
grouped_data = rec_fire_2022.groupby(['class_name_aggregated', 'freq_aggregated']).agg({'area': 'sum'}).reset_index()

# Configurar a fonte para Times New Roman, tamanho 12
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': 'Times New Roman',
    'font.size': 12
})

# Função para formatar os valores do eixo Y com separador de milhar como ponto
def custom_formatter(x, pos):
    return f'{x:,.0f}'.replace(',', '.')

formatter = FuncFormatter(formatador)

# Definir cores específicas para cada classe
color_map = {
    'Formação Florestal': '#1f8d49',
    'Formação Campestre': '#d6bc74',
    'Campo Alagado e Área Pantanosa': '#519799',
    'Formação Savânica': '#7dc975',
    'Agricultura': '#E974ED',
    'Área Urbanizada': '#d4271e',
    'Corpo Dágua': '#0000FF',
    'Afloramento Rochoso': '#ffaa5f',
    'Mineração': '#9c0027',
    'Pastagem': '#edde8e'
}

# Criar a figura e o eixo para o gráfico
fig, ax = plt.subplots(figsize=(10, 6))

# Plotar um gráfico de linha para cada classe agregada
for class_name, group in grouped_data.groupby('class_name_aggregated'):
    if class_name in color_map:  # Verificar se a classe tem cor definida
        ax.plot(group['freq_aggregated'], group['area'], label=class_name, color=color_map[class_name])

# Configurar os rótulos, título do gráfico e ajustar a legenda
ax.set_xlabel('Recorrência de Fogo')
ax.set_ylabel('Área Queimada(km²)')

# Ajustar a legenda para baixo e distribuí-la horizontalmente
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)

# Formatando o eixo y para usar ponto como separador de milhar
ax.yaxis.set_major_formatter(mticker.FuncFormatter(custom_formatter))

plt.grid(False)
plt.tight_layout()
plt.show()

#%% Polulação RI Xingu
df_populacao = pd.read_csv(r'C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\populacao_urbana_rural_v4.csv')

print(df_populacao.head())

plt.figure(figsize=(10, 6))
plt.plot(df_plot.index, df_plot["Urbana"] * 1000, label="População Urbana", marker='o')  # Multiplicando por 1000
plt.plot(df_plot.index, df_plot["Rural"] * 1000, label="População Rural", marker='x')  # Multiplicando por 1000

plt.xlabel("Ano", fontsize=12, fontname="Times New Roman")
plt.ylabel("Quantidade de Habitantes", fontsize=12, fontname="Times New Roman")

# Ajustando o tamanho da fonte dos ticks (valores dos eixos)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.legend(fontsize=12)
plt.grid(False)

# Ajustando o formato do eixo Y para mostrar números inteiros completos com ponto como separador de milhares
plt.gca().get_yaxis().set_major_formatter(plt.matplotlib.ticker.FuncFormatter(lambda x, _: format(int(x), ',').replace(',', '.')))

plt.show()


#%% Export
acumulado['city_name'] = acumulado['territory'].map(municipality_code_to_name)

acumulado['class_name'] = acumulado['class_id'].map(id_to_class)

print(acumulado)

output_file_path = r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\areas_rix_fire_level1_v1.csv"

df.to_csv(output_file_path, index=True)

# %%
