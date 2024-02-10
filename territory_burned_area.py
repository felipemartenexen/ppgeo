#%% importar bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

#%% Preparar base de dados
df = pd.read_csv(r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_2\data\join_geo\join_areas_fundiaria_ri_xingu_fire_lulc_v2_source_v3.csv")

# Função para determinar o território com base nas condições fornecidas
def determine_territory(row):
    if row['desc_subcl'] in ["Cadastro Ambiental Rural",
                             "Terra Legal Titulado", 
                             "Propriedade Privada SIGEF/SNCI",
                             "Terra Legal Não Titulado"]:
        return 'Imóvel Privado'
    elif row['desc_subcl'] in ["Unidade de Conservação de Uso Sustentável",
                               "Unidade de Conservação de Proteção Integral"]:
        return 'Unidades de Conservação'
    elif row['desc_subcl'] in ["Território Indígena Homologado",
                               "Território Indígena Não-Homologado"]:
        return 'Território Indígena'
    
    elif row['desc_subcl'] in [#"Água",
                               #"Área Urbanizada",
                               #"Malha de Transporte"
                               "Território Quilombola"
                               "Território Quilombola",
                               "Floresta Pública não Destinada",                               
                               "Gleba Pública SIGEF/SNCI",
                               "Território Comunitário"]:
        return "Outros"
    elif row['desc_subcl'] in ["Assentamento Rural",
                               "Área Militar"]:
        return row['desc_subcl']

# Aplicar a função ao DataFrame para criar a nova coluna 'territory'
df['territory'] = df.apply(determine_territory, axis=1)

# Agregar os dados por 'territory', somando 'area_fire_ha'
territory_fire_sum = df.groupby('territory')['area_fire_ha'].sum().reset_index()

# Ordenar os valores para uma melhor visualização
territory_fire_sum = territory_fire_sum.sort_values('area_fire_ha', ascending=False)

#%% Gráfico de Barra - Acumulado por Categoria Fundiária
# Criar o gráfico de barras usando Seaborn
plt.figure(figsize=(10, 8))  # Ajustar o tamanho conforme necessário
sns.barplot(x='area_fire_ha', y='territory', data=territory_fire_sum, palette='Spectral')

# Formatar o eixo X para usar 'mil' em vez de notação científica
# Função para formatar o eixo X
def thousands(x, pos):
    """O argumento 'pos' é a posição e não é usado aqui."""
    return '{:,.0f} mil'.format(x * 1e-3).replace(',', '.')

formatter = FuncFormatter(thousands)
plt.gca().xaxis.set_major_formatter(formatter)

# Adicionar títulos e rótulos
plt.title('Área Queimada por Categoria Fundiária')
plt.xlabel('Área Queimada (ha)')
plt.ylabel('Categoria Fundiária')

# Mostrar o gráfico
plt.tight_layout()
plt.show()

#%% Gráfico Porcetagem - Área Queimada por Categoria Fundiária
# Função para formatar o eixo y
def thousands(y, pos):
    """O argumento 'pos' é a posição e não é usado aqui."""
    return '{:,.0f} mil'.format(y * 1e-3).replace(',', '.')

# Calcular a porcentagem da área total para cada território
territory_fire_sum['percentage'] = (territory_fire_sum['area_fire_ha'] / territory_fire_sum['area_fire_ha'].sum()) * 100

# Ordenar os dados pela porcentagem para um gráfico mais intuitivo
territory_fire_sum = territory_fire_sum.sort_values('percentage', ascending=False)

# Definir a paleta de cores
colors = sns.color_palette('Spectral', len(territory_fire_sum))

# Criar o gráfico de pizza com as cores definidas
plt.figure(figsize=(10, 8))
plt.pie(territory_fire_sum['percentage'], labels=territory_fire_sum['territory'], autopct='%1.1f%%', startangle=140, colors=colors)

# Título do gráfico
plt.title('Porcentagem da Área Queimada por Categoria Fundiária')

# Mostrar o gráfico
plt.show()


#%% Gráfico Barra - Anual por Categoria Fundiária
# Calculando a média anual da área total afetada por incêndios
annual_sum = df.groupby('year')['area_fire_ha'].sum()
annual_mean = annual_sum.mean()

# Ordenando as categorias pela soma total de area_fire_ha
category_order = df.groupby('territory')['area_fire_ha'].sum().sort_values(ascending=False).index

# Agrupando os dados por 'year' e 'territory' e reordenando as colunas conforme a soma total de area_fire_ha
df_grouped = df.groupby(['year', 'territory'])['area_fire_ha'].sum().unstack(fill_value=0)[category_order]

# Definindo uma função de formatação para o eixo Y
def millions_formatter(x, pos):
    return '{:,.0f} mil'.format(x * 1e-3).replace(',', '.')

# Preparando as cores
palette = sns.color_palette('Spectral', len(df_grouped.columns)).as_hex()

# Criando o gráfico de barras empilhadas
ax = df_grouped.plot(kind='bar', stacked=True, color=palette, figsize=(10, 8))

# Adicionando a linha da média anual
mean_line = ax.axhline(annual_mean, color='black', linestyle='--', linewidth=2)

# Aplicando a formatação personalizada ao eixo Y
ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

# Adicionando rótulos e título
plt.xlabel('Ano')
plt.ylabel('Área Queimada (ha)')
plt.title('Área Queimada por Categoria Fundiária')

# Ajustando a legenda e os eixos
plt.xticks(rotation=45)
plt.tight_layout()

# Adicionando a linha de média à legenda
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='black', linestyle='--', linewidth=2, label='Média Anual')] + \
                  [Line2D([0], [0], color=color, marker='s', linestyle='None', markersize=10, label=territory) for territory, color in zip(category_order, palette)]
ax.legend(handles=legend_elements, title='Legenda')

# Mostrar o gráfico
plt.show()


#%%
