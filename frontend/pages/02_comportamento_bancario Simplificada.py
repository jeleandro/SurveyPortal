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
from data_model import categoricals_demographics, load_survey_core, load_know_bank, load_nps_questions, load_ranking_questions


################## Page config
st.set_page_config(layout="wide")

df = load_survey_core()
df_rankings = load_ranking_questions()


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

def nps_chart(cel_container, categ, df, x, y):
    with cel_container:
        with chart_container(df):
            fig = px.line(df,y=y,x=x,title=f"{categ.replace('_', ' ').title()}",)
            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=-1.02,x=-1))
            fig.update_layout(xaxis_range=[0,1])
            st.plotly_chart(fig, use_container_width=True)

def nps_filter(df, categ):
    df = (
        df
        .astype({'nps':str})
        .pivot_table(
            index=['categoria', 'pergunta'],
            columns='nps',
            values='id',
            aggfunc='nunique',
        )
        .reset_index()
    )
    df=  (
        df
        .query(f'categoria == "{categ}"')
        .drop(columns='categoria')
        .set_index('pergunta')
        [constants.CATEG_NPS.categories]
        .apply(lambda x:x/x.sum(),axis=1)
        .reset_index()
        .assign(pergunta=lambda x: x['pergunta'].str.replace('_',' ').str.capitalize())
    )
    
    df = (
        df
        .assign(pct_concordancia=df[['Concordo totalmente','Concordo']].sum(axis=1))
        [['pergunta','pct_concordancia']]
    )

    return df


def ranking_filter(df, categ):
    df = (
        df
        .query(f'categoria == "{categ}"')
        .assign(rank=lambda x:x['rank'].apply(lambda x:f'R{x:02d}'))
        .pivot_table(
            index=['categoria', 'prioridade'],
            columns='rank',
            values='id',
            aggfunc='nunique',
        )
        .reset_index()
        .merge(
            df_rankings.groupby(['categoria']).agg(N=('id', 'nunique')).reset_index(),
            on=['categoria']

        )
    )
    df = (
        df
        .assign(pct_prioridade_1_e_2=df[['R01','R02']].sum(axis=1)/df['N'])
        [['prioridade','pct_prioridade_1_e_2']]
    )

    return df


class RowProducer:
    def __init__(self, row_len) -> None:
        self.row_len = row_len;
        self.row = row = st.columns(row_len);
        self.index = 0;
        pass
    def getNext(self):
        if self.index == row_len:
            row = st.columns(row_len)
            self.index=0
        
        theRow = self.row[self.index];
        self.index+=1
        return theRow
        

if len(df_nps) == 0 :
    st.write("Nenhum dado encontrado para a seleção. Considere mudar o filtro.")

st.write('## Crédito e canais de contratação')

layout = RowProducer(row_len=row_len)
for categ in ['jornada_contratacao_credito_principal','atendimento_robo','planejamento_credito',  'capacidade_financeira']:
    temp = nps_filter(df_nps, categ)
    nps_chart(layout.getNext(), categ,temp, x='pct_concordancia', y="pergunta")

for categ in [ 'canal_contratacao_prioridade','fator_escolher_banco_emprestimo']:
    temp = ranking_filter(df_rankings, categ)
    nps_chart(layout.getNext(), categ,temp, x='pct_prioridade_1_e_2', y="prioridade")


# 
# displayBlock(df_nps, )

st.write('## Contratação de produtos')
layout = RowProducer(row_len=row_len)
for categ in ['cheque_especial','cartao_credito',    'crediario_digital', 'credito_parcelado']:
    temp = nps_filter(df_nps, categ)
    nps_chart(layout.getNext(), categ,temp, x='pct_concordancia', y="pergunta")

for categ in [ "fator_escolher_banco_emprestimo",'credito_parcelado_novo__importancia', "cartao_credito_novo__importancia", "credito_parcelado_novo__importancia"]:
    temp = ranking_filter(df_rankings, categ)
    nps_chart(layout.getNext(), categ,temp, x='pct_prioridade_1_e_2', y="prioridade")


st.write('## Inadimplência')
layout = RowProducer(row_len=row_len)
for categ in ['credito_negado', 'situacao_credito',   'endividamento', 'personalizacao_cobranca']:
    temp = nps_filter(df_nps, categ)
    nps_chart(layout.getNext(), categ,temp, x='pct_concordancia', y="pergunta")

for categ in ['meio_pagamento_preferencial', 'prioridadePagamentoRank','melhorias_processo_cobranca'
              ,'tipo_ofertas_renegociacao']:
    temp = ranking_filter(df_rankings, categ)
    nps_chart(layout.getNext(), categ,temp, x='pct_prioridade_1_e_2', y="prioridade")