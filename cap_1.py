#%%
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

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


#%%Export

output_file_path = r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_1\data\df_fire_month_v1.csv"

df_fire_month.to_csv(output_file_path, index=True)