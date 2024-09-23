import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from streamlit_extras.chart_container import chart_container

from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, RobustScaler
from sklearn.metrics import silhouette_score


# including the parent folder on the path
import sys
sys.path.append('..')

import constants
import pandas_utils
from data_model import categoricals_demographics, load_survey_core, load_product_bank


################## Page config
st.set_page_config(layout="wide")


############## Data loading
df = load_survey_core()

df_products = load_product_bank()

############## Side Bar

with st.sidebar:
    st.title("Clustering");

    n_clusters = st.number_input("Escolha o número de clusteres", min_value=2, max_value=20)



###### Main page
st.title('Análise do Consumo de produtos')

with st.expander("Filtros"):
    filtroNPSIncome  = st.multiselect(
        "Selecione a faixa de renda",
        constants.CATEG_INCOME_RANGE.categories,
        constants.CATEG_INCOME_RANGE.categories.tolist(),
        )
    
    filtroNPSEducation  = st.multiselect(
        "Selecione o nível educacional",
        constants.CATEG_EDUCATION.categories,
        constants.CATEG_EDUCATION.categories.tolist(),
        )
    
    cols = st.columns(3)

    filtroBancarizado = cols[0].multiselect(
        'Bancarizado',
        ['Bancarizado','Não bancarizado'],
        ['Bancarizado','Não bancarizado']
    )

    filtroNPSGenero  = cols[0].multiselect(
        "Selecione genero",
        ['Feminino','Masculino'],
        ['Feminino','Masculino'],
        )
    
    filtroNPSRegiao  = cols[1].multiselect(
        "Selecione regiao",
        constants.CATEG_REGIAO.categories,
        constants.CATEG_REGIAO.categories.tolist(),
        )
    filtroNPSAge  = cols[2].multiselect(
        "Selecione as faixa de idade",
        constants.CATEG_AGE.categories,
        constants.CATEG_AGE.categories.tolist(),
        )

    df_filter = df.copy()

    df_waterfall = [['total',len(df_filter)]]


    if len(filtroBancarizado) < 2:
        df_filter = df_filter.query(f"ind_bancarizado in {filtroBancarizado}")
        df_waterfall.append(['Filtro bancarizado',len(df_filter)])

    if len(filtroNPSGenero) < 2:
        df_filter = df_filter.query(f"genero in {filtroNPSGenero}")
        df_waterfall.append(['Filtro genero',len(df_filter)])

    if len(filtroNPSEducation) != len(constants.CATEG_EDUCATION.categories):
        df_filter = df_filter.query(f"escolaridade in {filtroNPSEducation}")
        df_waterfall.append(['Filtro escolaridade',len(df_filter)])

    if len(filtroNPSIncome) != len(constants.CATEG_INCOME_RANGE.categories):
        df_filter = df_filter.query(f"faixa_renda in {filtroNPSIncome}")
        df_waterfall.append(['Filtro faixa de renda',len(df_filter)])

    if len(filtroNPSRegiao) != len(constants.CATEG_REGIAO.categories):
        df_filter = df_filter.query(f"regiao in {filtroNPSRegiao}")
        df_waterfall.append(['Filtro regiao',len(df_filter)])


    if len(filtroNPSAge) != len(constants.CATEG_AGE.categories):
        df_filter = df_filter.query(f"faixa_idade in {filtroNPSAge}")
        df_waterfall.append(['Filtro idade',len(df_filter)])

    st.write(f"{len(df_filter)/len(df):0.1%} respondentes selecionados")
    st.dataframe(pd.DataFrame(df_waterfall,columns=['base','quantidade']).sort_values('quantidade', ascending=False))

if len(df_filter)>0:
    df_products = df_products.merge(df_filter, on='id', how='inner')
else:
    st.write("Nenhum registro foi selecionado. O filtro será ignorado")



##################################################################################################################
st.write('## Análise de cesta - via cluster de banco por produto')

produtosDisponiveis  = df_products['produto'].value_counts().index.tolist()
filtroProdutos = st.multiselect(
        'Produtos',
        produtosDisponiveis,
        produtosDisponiveis
    )

st.write("Cada cluster diz, em média, em quantos bancos o cliente tem o produto x.")

def trainCluster(df_produtos_basket, k):
    model = Pipeline([
        # ('pca', PCA(n_components=2, random_state=42)),
        ('outlier', RobustScaler(quantile_range=(0.1,0.9))),
        ('norm', PowerTransformer()),
        ('kmeans', KMeans(n_clusters=k, random_state=42)),
    ])
    
    
    # Fit the model to the data
    model.fit(df_produtos_basket)
    
    # Calculate the silhouette score
    score = silhouette_score(df_produtos_basket, model['kmeans'].labels_, sample_size=600, random_state=42)

    return model['kmeans'].labels_


df_consolidado_por_id = (
    df_products
    .query(f'produto in {filtroProdutos}')
    .pivot_table(
        index='id',
        columns='produto',
        values='banco',
        aggfunc='nunique',
        fill_value=0,
    )
)


labels = trainCluster(
    df_consolidado_por_id.apply(lambda x:x/x.sum(), axis=1),
    n_clusters
)

df_consolidado_por_id['cluster'] = labels

def sortCols(df):
    return df.sort_values(df.columns.values.tolist(), ascending=False);

cols = st.columns([2,1])

cols[0].dataframe(
    df_consolidado_por_id.groupby('cluster').median()
    [filtroProdutos]
    .T
    # .pipe(sortCols)
    .round(2)
    .style
    .format('{:.2}')
    .background_gradient(cmap='Blues', axis=0)
)

with cols[1]:
    st.bar_chart(
        df_consolidado_por_id
        .reset_index()
        .groupby('cluster')
        .agg(pct_respondentes=('id','nunique'))
        .assign(pct_respondentes=lambda x:x['pct_respondentes']/x['pct_respondentes'].sum())
        .style
        .format('{:.1%}')
        .background_gradient(cmap='Blues', axis=0)
    )

    df_indicadores = (
        df_products
        .merge(df_consolidado_por_id.reset_index()[['id','cluster']], on='id')
        .assign(default=lambda x:x['default']=='Sim')
        .assign(bancarizado=lambda x:x['ind_bancarizado']=='Bancarizado')
        .groupby('cluster')
        .agg(
            inadimplencia=('default','mean'),
            #bancarizado=('bancarizado','mean'),
        )
    )
    st.line_chart(df_indicadores)
    
df_cesta_banco = (
    df_products
    .merge(df_consolidado_por_id.reset_index()[['id','cluster']], on='id')
    .pivot_table(
        index='banco_principal',
        columns='cluster',
        values='id',
        aggfunc='nunique',
        fill_value=0,
    )
    .pipe(sortCols)
)

with chart_container(df_cesta_banco):
    fig = px.bar(
        df_cesta_banco.apply(lambda x:x/x.sum(),axis=1).reset_index(),
        x="banco_principal",
        y=df_cesta_banco.columns,
        # barmode='group',
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.5,
        x=-0
    ))
    st.plotly_chart(fig, use_container_width=True)


###########################################################
st.write("## Comparativo entre bancos")

bancosPorPrincipalidade = df['banco_principal'].value_counts().index.tolist()

listaBancos  = st.multiselect(
        "Filtre os bancos para o estudo",
        bancosPorPrincipalidade,
        bancosPorPrincipalidade[0],
        )

df_consolidado = (
    df_products
    .pivot_table(
        index='banco',
        columns='produto',
        values='id',
        aggfunc='nunique',
        fill_value=0,
    )
    .apply(lambda x:x/x.sum(), axis=1)
    .T
)

# st.dataframe(df_consolidado[listaBancos])

with chart_container(df_consolidado[listaBancos]):
    fig = px.bar(
        df_consolidado[listaBancos].reset_index(),
        x="produto",
        y=listaBancos,
        barmode='group',
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-1,
        x=-0
    ))
    st.plotly_chart(fig, use_container_width=True)