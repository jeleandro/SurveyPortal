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
from data_model import categoricals_demographics, load_survey_core, load_product_bank, load_nps_questions


################## Page config
st.set_page_config(layout="wide")


############## Data loading
df = load_survey_core()
df_products = load_product_bank()
df_nps = load_nps_questions()

df_indice_digital = (
    df_nps.query('pergunta == "consigo_contratar_100digital"')
    .assign(digitalizacao = lambda x:x['nps'].str.lower().isin(['concordo','concordo totalmente']).astype(int))
    [['id','digitalizacao']]
)

df = pd.merge(df, df_indice_digital, on='id', how='left').fillna({'digitalizacao':0})

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


## temp

trainingSet = (
    df_products.pivot_table(index='id', columns='produto', values='banco', aggfunc='nunique', fill_value=0)
    .merge(df[['id','default','digitalizacao']], on='id')
    .assign(default=lambda x:(x['default']=='Sim').astype(int))
    .drop('id',axis=1)
)



st.write("## Produtos com mais impacto na inadimplência e digitalização")

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV


# clf_default = RandomForestClassifier(n_estimators=100, random_state=42)
clf_default = LogisticRegressionCV(random_state=42, Cs=10)
clf_default.fit(trainingSet.drop(['default','digitalizacao'], axis=1), trainingSet['default'])

featureImportanceDefault = pd.DataFrame({
    'features':clf_default.feature_names_in_,
    # 'importance':clf.feature_importances_,
    'importance':np.round(clf_default.coef_.flatten(),4),
    'color':np.where(clf_default.coef_.flatten()>0, 'Mais inadimplente', 'Menos inadimplente')
})


clf_digitalizacao = LogisticRegressionCV(random_state=42, Cs=1)
clf_digitalizacao.fit(trainingSet.drop(['default','digitalizacao'], axis=1), trainingSet['digitalizacao'])

featureImportanceDigital = pd.DataFrame({
    'features':clf_digitalizacao.feature_names_in_,
    # 'importance':clf.feature_importances_,
    'importance':np.round(clf_digitalizacao.coef_.flatten(),4),
    'color':np.where(clf_digitalizacao.coef_.flatten()>0, 'Mais digital', 'Menos digital')
})



cols = st.columns(2)

with cols[0]:
    fig = px.bar(
        featureImportanceDefault.sort_values('importance', ascending=False),
        y='features',
        x='importance',
        title='Produtos com mais impacto na inadimplência',
        labels={'importance': 'Importance', 'features': 'Features'},
        color='color',
        color_discrete_map={'Mais inadimplente':'red','Menos inadimplente':'blue'},
        orientation='h'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    fig = px.bar(
        featureImportanceDigital.sort_values('importance', ascending=False),
        y='features',
        x='importance',
        title='Produtos com mais impacto na digitalização',
        labels={'importance': 'Importance', 'features': 'Features'},
        color='color',
        color_discrete_map={'Menos digital':'red','Mais digital':'blue'},
        orientation='h'
    )
    fig.update_layout(xaxis_tickangle=-45)
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
    cutoff = st.slider('Top%', 0.0, 1.0, 0.0,0.01)

    temp = df_consolidado[listaBancos].sort_values(listaBancos, ascending=[False]*len(listaBancos))
    temp = temp.query(" and ".join([f"{col} > {cutoff}" for col in listaBancos]))

    fig = px.bar(
        temp.reset_index(),
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



st.markdown('## quem está mais concentrado por produto versus a média')

listaProdutos  = st.selectbox(
        "Selecione o produto",
        df_consolidado.index,
        0,
        )

posicao_relativa = (df_consolidado.T/df_consolidado.T.median(axis=0)).T -1
posicao_relativa = posicao_relativa.query('produto == @listaProdutos')
posicao_relativa = posicao_relativa.T.sort_values(listaProdutos, ascending=False)

# #bar chart
# st.write(posicao_relativa.reset_index())
with chart_container(posicao_relativa):

    fig = px.bar(
        posicao_relativa.reset_index(),
        x="banco",
        y=listaProdutos,
        barmode='group',
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-1,
        x=-0
    ))
    st.plotly_chart(fig, use_container_width=True)


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