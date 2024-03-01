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

#%% Distribuição Fogo - Mês - Ano

df_fire_month['month_id'] = df_fire_month['month'].map(month_id)
df_fire_month.sort_values('month_id', inplace=True, ascending=True)

# Criando a figura
fig, ax = plt.subplots(figsize=(10, 6))

# Plotando o heatmap
sns.heatmap(data=df_fire_month.pivot_table(index="month_id", columns="year", values="area"),
            annot=False, fmt=".2f", ax=ax)

# Definindo labels
ax.set_xlabel("Ano")
ax.set_ylabel("Mês")

# Rotacionando labels do eixo x
plt.xticks(rotation=45)

# Adicionando título
plt.title("Heatmap da Área")

# Mostrando o gráfico
plt.show()
#%%Export

output_file_path = r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\df_fire_month_v1.csv"

df_fire_month.to_csv(output_file_path, index=True)
# %%
