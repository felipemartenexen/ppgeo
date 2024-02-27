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





#%% Gráfico Box Plot por Categoria Fundiária
# Passo 1: Converter df_grouped de volta para o formato longo
df_long = df_grouped.stack().reset_index(name='area_fire_ha')
df_long.rename(columns={'level_0': 'year', 'territory': 'category'}, inplace=True)

# Passo 2: Criar uma nova coluna para agrupar os anos nos intervalos especificados
def year_group(year):
    if 1985 <= year <= 1994:
        return '1985-1994'
    elif 1995 <= year <= 2004:
        return '1995-2004'
    elif 2005 <= year <= 2014:
        return '2005-2014'
    elif 2015 <= year <= 2022:
        return '2015-2022'
    else:
        return 'Outro'

df_long['year_group'] = df_long['year'].apply(year_group)

# Encontrar territórios únicos
unique_territories = df_long['category'].unique()

# Criar um gráfico de box plot para cada território
for territory in unique_territories:
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='year_group', y='area_fire_ha', data=df_long[df_long['category'] == territory])
    plt.title(f'Distribuição da Área Afetada por Incêndios para {territory}')
    plt.xlabel('Período')
    plt.ylabel('Área Afetada por Incêndios (ha)')
    plt.xticks(rotation=45)
    plt.show()

# %% Tabela com os Dados Agrupados por Período e Categoria Fundiária
# Definindo a função para agrupar os anos
def year_group(year):
    if 1985 <= year <= 1994:
        return '1985-1994'
    elif 1995 <= year <= 2004:
        return '1995-2004'
    elif 2005 <= year <= 2014:
        return '2005-2014'
    elif 2015 <= year <= 2022:
        return '2015-2022'
    else:
        return 'Outro'

# Aplicando a função ao DataFrame
df['year_group'] = df['year'].apply(year_group)

# Criando o DataFrame desejado
df_long = df.groupby(['year_group', 'territory'])['area_fire_ha'].sum()

print(df_long)
#%%Exportar para .csv
# Definir o caminho do arquivo de destino
output_file_path = r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_2\data\join_geo\area_group_by_year_territory.csv"

# Exportar o DataFrame para um arquivo CSV
df_long.to_csv(output_file_path, index=True)

# Imprimir o caminho do arquivo para referência
print(f'O DataFrame foi exportado para: {output_file_path}')

# %%
# Carregar o DataFrame
df_class = pd.read_csv(r"C:\Users\luiz.felipe\Desktop\FLP\Mestrado\etapa_2\data\join_geo\area_group_by_year_territory_class.csv")

# Definir a função class_group
def class_group(class_id):
    if class_id == 3:
        return 'Formação Florestal'
    elif class_id == 4:
        return 'Formação Savânica'
    elif class_id == 9:
        return 'Silvicultura'
    elif class_id == 11:
        return 'Campo Alagado e Área Pantanosa'
    elif class_id == 12:
        return 'Formação Campestre'
    elif class_id == 15:
        return 'Pastagem'
    elif class_id == 39:
        return 'Soja'
    elif class_id == 41:
        return 'Outras Lavouras Temporárias'
    elif class_id == 48:
        return 'Outras Lavouras Perenes'
    else:
        return 'Outro'

# Aplicar a função para criar a nova coluna 'desc_class'
df_class['desc_class'] = df_class['class'].apply(class_group)

# Aplicar a função para criar a nova coluna 'period'
df_class['period'] = df_class['year'].apply(year_group)

df_class_group = df_class.groupby(['territory', 'period', 'desc_class'])['area_fire_ha'].sum().reset_index()

# Exibir as primeiras linhas do DataFrame modificado para verificar a nova coluna
df_class_group
# %%
