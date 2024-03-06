#%%
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import seaborn as sns
import matplotlib.ticker as mticker
#%%Preparo dos dados
df = pd.read_csv(r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\areas_rix_fire_lulc_year_v2.csv")

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

print(df.head())

#%% Distribuição Anual

df_fire_year = df.groupby('year')['area'].sum().reset_index()

# Cálculo da tendência linear
slope, intercept, r_value, p_value, std_err = stats.linregress(df_fire_year.index, df_fire_year["area"])

# Adicionando a tendência linear ao DataFrame
df_fire_year['trend'] = intercept + slope * df_fire_year.index

# Plotando os dados e a tendência
plt.figure(figsize=(10, 6))
plt.plot(df_fire_year["year"], df_fire_year["area"], label='Área Queimada (km²)', marker='o', color='red')
plt.plot(df_fire_year["year"], df_fire_year["trend"], label='Tendência Linear', linestyle='--', color='black')
plt.title('Análise Temporal das Áreas Queimadas (1985-2022)')
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

df_fire_month_grouped['month_id'] = df_fire_month_grouped['month'].map(month_id)

# Ordenando os dados pelo mês numericamente para garantir a sequência de Janeiro a Dezembro
df_fire_month_grouped.sort_values('month_id', inplace=True)
# Criando o gráfico de barras com porcentagem
# Recriando o gráfico com a correção para garantir que os rótulos estejam na ordem correta
fig, ax1 = plt.subplots(figsize=(14, 8))
sns.barplot(x='month', y='area', data=df_fire_month_grouped, color='red', ax=ax1)
ax1.set_title('Área Queimada Mensal')
ax1.set_xlabel('Mês')
ax1.set_ylabel('Área Queimada (km²)')

# Corrigindo a posição dos rótulos
for i, (index, row) in enumerate(df_fire_month_grouped.iterrows()):
    ax1.text(i, row['area'], f"{row['area']/1000:.2f}k\n({row['percentage']:.2f}%)", color='black', ha="center", va='bottom')

# Ajustando o eixo Y à esquerda para mostrar os valores em 'k' (milhares)
ticks_loc = ax1.get_yticks().tolist()
ax1.yaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax1.set_yticklabels(['{:.0f}k'.format(x/1000) for x in ticks_loc])

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
    'Soja': '#f5b3c8'
}

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

plt.title('Área Queimada por Classe de Uso e Cobertura do Solo por Ano (km²)', fontweight='bold')
plt.xlabel('Ano', fontweight='bold')
plt.ylabel('Área Queimada (km²)', fontweight='bold')
plt.legend(loc='upper left', ncol=1, fontsize='10')
plt.tight_layout()

plt.show()

#%% Uso do Solo Normalizado
# Normalizando os dados para que cada coluna empilhada some 100%
area_normalizada = area_por_classe_ano_ordenado.div(area_por_classe_ano_ordenado.sum(axis=1), axis=0) * 100

# Gerando o gráfico de barras empilhadas normalizado com a legenda ajustada para 2 linhas centralizadas abaixo do gráfico
fig, ax = plt.subplots(figsize=(18, 10))
area_normalizada.plot(kind='bar', stacked=True, color=[cores_classes[col] for col in ordem_classes], ax=ax, fontsize='12')

plt.title('Distribuição Percentual da Área Queimada por Classe de Uso e Cobertura do Solo por Ano', fontweight='bold', fontsize='12', fontname='Times New Roman')
plt.xlabel('Ano', fontweight='bold', fontsize='12', fontname='Times New Roman')
plt.ylabel('Percentual da Área Queimada (%)', fontweight='bold', fontsize='12', fontname='Times New Roman')
# Ajustando a legenda para 2 linhas centralizadas
leg = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=int(len(ordem_classes)/2 + 0.5), fontsize='12', frameon=False)
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
#%%Export

output_file_path = r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\df_normalized_by_class.csv"

area_normalizada.to_csv(output_file_path, index=True)
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
