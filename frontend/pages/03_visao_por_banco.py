import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_container import chart_container 

# including the parent folder on the path
import sys
sys.path.append('..')

import constants
import pandas_utils
from data_model import categoricals_demographics, load_survey_core, load_know_bank

st.set_page_config(layout="wide")


other_cols = ['ind_bancarizado','default','banco_principal']


df = load_survey_core()
df_know = load_know_bank()

if st.sidebar.button("Atualizar dados"):
    st.cache_data.clear()

##############################################################################################################
bancos_principais = df['banco_principal'].value_counts().index.values
chosenBank = ''
metricChoice = ''

with st.sidebar:
    st.write('## Escolha um banco')
    chosenBank = st.selectbox("Banco", bancos_principais, np.random.randint(0,len(bancos_principais)))

    st.write('## Opções dos gráficos')
    sortingChoice = st.selectbox("Ordenação",("Mesma dos dados", "Quantidade"),)
    row = st.columns(2);
    with row[0]: metricChoice = st.selectbox("Métrica",("Percentual", "Quantidade"),)
    with row[1]: acumChoice = st.selectbox("Percentual",("Simples", "Acumulado"),)
    if acumChoice == "Acumulado":
        cutoff = st.slider('Top%', 0.0, 1.0, 1.0,0.05)
    row_len = st.slider('Quantidade de colunas por linha', 1, 4, 2)


st.title(f"Visão do {chosenBank}")
st.divider()


##############################################################################################################
st.write(f"## Métricas e insights")

def createMetrics(df, chosenBank):
    st.write("Métricas comparadas com os demais concorrentes")

    df_visibilidade = (
        df_know
        .assign(theBank=lambda x:np.where(x['banco'] == chosenBank, x['banco'], 'Demais'))
        .pivot_table(index='theBank',columns='valor', values='id', aggfunc='nunique')
        .apply(lambda x: x / x.sum(), axis=1)
        [['Sim']].rename(columns={'Sim':'visibilidade'})
        .T
        .assign(variacao=lambda x:x[chosenBank]/x['Demais'])
        .round(2)

    )
    
    principalidade = (df['banco_principal']== chosenBank).mean()
    
    
    df_metrics = (
        df
        .assign(theBank=lambda x:np.where(x['banco_principal'] == chosenBank, x['banco_principal'], 'Demais'))
        .assign(idade_menor_35=lambda x:(x['faixa_idade'].isin(['18-24','25-34'])).astype(int))
        .assign(publico_feminino=lambda x:(x['genero'].isin(['Feminino'])).astype(int))
        .assign(concentracao_sudeste=lambda x:(x['regiao'].isin(['Sudeste'])).astype(int))
        .assign(emprego_tempo_integral=lambda x:(x['tipo_emprego'].isin(['Empregado tempo integral'])).astype(int))
        .assign(aposentados=lambda x:(x['tipo_emprego'].isin(['Aposentado'])).astype(int))
        .assign(inadimplente=lambda x:(x['default'].isin(['Sim'])).astype(int))
        
        .groupby('theBank')
        .agg(
            inadimplente=('inadimplente','mean'),
            publico_jovem=('idade_menor_35','mean'),
            publico_feminino=('publico_feminino','mean'),
            concentracao_sudeste=('concentracao_sudeste','mean'),
            emprego_tempo_integral=('emprego_tempo_integral','mean'),
            aposentados=('aposentados','mean'),
        )
        .T
        .assign(variacao=lambda x:x[chosenBank]/x['Demais']-1)
        .round(2)
        .reset_index().rename(columns={'index':'metrica'})
        
    )
    # st.write(df_metrics)

    cols = st.columns(len(df_metrics)+1)
    cols[0].metric("Principalidade", f"{principalidade:0.0%}")
    
    for i, row in enumerate(df_metrics.iterrows()):
        cols[i+1].metric(
            row[1]["metrica"].replace('_',' ').title(),
            f"{row[1][chosenBank]:0.0%}",
            f"{row[1]['variacao']:0.0%}",
        )

    style_metric_cards()

    with st.expander("Detalhes das métricas"):
        st.write('''
        - **Principalidade**: Percentual de pessoas que escolheram o banco como principal
        - **Publico Jovem**: Percentual de pessoas com idade até 35 anos
        - **Publico Feminino**: Percentual de pessoas do sexo feminino
                 
        As setas indicam a razao entre o indicador do banco dividido pelo mesmo indicador dos demais bancos.
        
        ''')




createMetrics(df, chosenBank);

st.divider()

##############################################################################################################

st.write(f"## Visão demografia comparada")
chart_cols = st.multiselect(
    "Escolha as demografias",
    categoricals_demographics,
    categoricals_demographics,
)

all_bank_groups = df['agrupamento_bancos'].value_counts().index.values
bank_cate_cols = st.multiselect(
    "Escolha os agrupamentos de bancos",
    all_bank_groups,
)

def addChart(container, df,  column):
    stat = (
        pandas_utils
        .basicStats(df.query(f'banco_principal =="{chosenBank}"'), column)
        .set_index(column)
        .rename(columns=lambda x:x+'_'+chosenBank)
    )

    stat_others = (
        pandas_utils
        .basicStats(df.query(f'banco_principal !="{chosenBank}"'), column)
        .set_index(column)
        .rename(columns=lambda x:x+'_demais')
    )
    stat = stat.merge(stat_others, left_index=True, right_index=True)

    # for bank_agr in df['banco_principal_agr1'].unique():
    for bank_agr in bank_cate_cols:
        stat_others = (
            pandas_utils
            .basicStats(df
                        .query(f'banco_principal !="{chosenBank}"')
                        .query(f'agrupamento_bancos =="{bank_agr}"'), column)
            .set_index(column)
            .rename(columns=lambda x:x+'_'+bank_agr)
        )
        stat = stat.merge(stat_others, left_index=True, right_index=True)

    if sortingChoice == 'Quantidade':
        stat = stat.sort_values('n_demais', ascending=False)

    if acumChoice == 'Acumulado':
        stat = stat.cumsum();

    stat = stat.reset_index()

    metric = 'n_' if metricChoice == 'Quantidade' else 'perc_'
    fig = go.Figure()
    
    for c in stat.columns:
        if not c.startswith(metric):
            continue;
        
        
        if metricChoice == 'Quantidade':
            text = [f"{v}" for v in stat[c]]
        else:
            text = [f"{v:.1%}" for v in stat[c]]

        fig.add_trace(go.Scatter(
            x=stat[column],
            y=stat[c],
            name=c,
            text=text,
            mode="lines+markers+text",
            ))

        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

    with container:
        with chart_container(stat):
            st.write(f"### {column.replace('_',' ').title()}")
            st.plotly_chart(fig, use_container_width=True)



row_len = 2
row = st.columns(row_len);
col_count = 0
for column in chart_cols:
    if col_count == row_len:
        row = st.columns(row_len)
        col_count = 0
    col = row[col_count]
    col_count += 1

    addChart(col,df,  column)




st.divider()

##############################################################################################################

st.title("TODO: CRIAR VISAO PRODUTOS")

st.write("""
    - Quais produtos os clientes tem contratado
    - Quais produtos os respondentes considerariam contratar (clientes x não clientes)
    - Quais produtos que os clientes tem na concorrencia
    - Quais produtos que os clientes inadimplentes possuem. 
""")

