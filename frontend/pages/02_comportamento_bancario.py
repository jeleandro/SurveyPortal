import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from streamlit_extras.chart_container import chart_container

# including the parent folder on the path
import sys
sys.path.append('..')

import constants
import pandas_utils
from data_model import categoricals_demographics, load_survey_core, load_know_bank, load_nps_questions


#### Page config
st.set_page_config(layout="wide")

df = load_survey_core()


# conhece_banco

if st.sidebar.button("Clear All"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()

############################################################################################################## 
# Visao questões do tipo NPS
st.title("Comportamento bancário")

with st.sidebar:
    st.write('## Opções dos gráficos')
    sortingChoice = st.selectbox("Ordenação",("Mesma dos dados", "Quantidade"),)
    acumChoice = st.toggle("Percentual acumulado")
    if acumChoice:
        cutoff = st.slider('Top%', 0.0, 1.0, 1.0,0.05)
    row_len = st.slider('Quantidade de colunas por linha', 1, 4, 2)




with st.expander("Filtre"):
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

    if len(filtroNPSGenero) < 2:
        df_filter = df_filter.query(f"genero in {filtroNPSGenero}")

    if len(filtroNPSEducation) != len(constants.CATEG_EDUCATION.categories):
        df_filter = df_filter.query(f"escolaridade in {filtroNPSEducation}")

    if len(filtroNPSIncome) != len(constants.CATEG_INCOME_RANGE.categories):
        df_filter = df_filter.query(f"faixa_renda in {filtroNPSIncome}")

    if len(filtroNPSRegiao) != len(constants.CATEG_REGIAO.categories):
        df_filter = df_filter.query(f"regiao in {filtroNPSRegiao}")


    if len(filtroNPSAge) != len(constants.CATEG_AGE.categories):
        df_filter = df_filter.query(f"faixa_idade in {filtroNPSAge}")

    st.write(f"{len(df_filter)/len(df):0.1%} respondentes selecionados")

df_nps = load_nps_questions()

df_nps = df_nps.merge(df_filter[['id']],on='id', how='inner')

def nps_chart(cel_container, categ, df):
    with cel_container:
        with chart_container(df):
            fig = px.bar(
                df,
                y="pergunta",
                x=constants.CATEG_NPS.categories, title=f"{categ.replace('_', ' ').title()}",
                # color= ['DarkRed','red','lightred', 'lightblue','blue','darkbl']
                color_discrete_map={
                    'Discordo totalmente':'#bb0a0a',
                    'Discordo':'#c2204b',
                    'Discordo em partes':'#b54579',
                    'Concordo em partes':'#3549b5',
                    'Concordo':'#1d30b9',
                    'Concordo totalmente':'#0f00b9',
                }
            )
            fig.update_layout(legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-1.02,
                # xanchor="center",
                x=-1
            ))
            st.plotly_chart(fig, use_container_width=True)

def nps_filter(df, categ):
    return (
            df
            .query(f'categoria == "{categ}"')
            .drop(columns='categoria')
            .set_index('pergunta')
            [constants.CATEG_NPS.categories]
            .apply(lambda x:x/x.sum(),axis=1)
            .reset_index()
            .assign(pergunta=lambda x: x['pergunta'].str.replace('_',' ').str.capitalize())
        )

def displayNPS(df_nps, categorias):
    df_nps_agrupado = (
        df_nps
        .astype({'nps':str})
        .pivot_table(
            index=['categoria', 'pergunta'],
            columns='nps',
            values='id',
            aggfunc='nunique',
        )
        .reset_index()
    )


    row = st.columns(row_len);
    col_count = 0
    for categ in categorias:
        if col_count == row_len:
            row = st.columns(row_len)
            col_count = 0
        cel_container = row[col_count]
        col_count += 1
        temp = nps_filter(df_nps_agrupado, categ)
        nps_chart(cel_container, categ,temp)

if len(df_nps):
    st.write('## Jornada de contratação de crédito')
    displayNPS(df_nps, [ 'atendimento_robo','jornada_contratacao_credito_principal','planejamento_credito', 'capacidade_financeira'])

    st.write('## Contratação de produtos')
    displayNPS(df_nps, [ 'cartao_credito', 'cheque_especial',   'crediario_digital', 'credito_parcelado'])

    st.write('## Inadimplência')
    displayNPS(df_nps, [ 'credito_negado', 'situacao_credito',   'endividamento', 'personalizacao_cobranca'])
else:
    st.write("Nenhum dado encontrado para a seleção. Considere mudar o filtro.")