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




################## Page config ########################################################################
st.set_page_config(layout="wide")


################## Data loading ########################################################################
df_core_full = load_survey_core()
df_nps_full = load_nps_questions()
df_rankings_full = load_ranking_questions()


categoria_bancos = ['Todos']+constants.CATEG_BANK_CATEG.categories.tolist()



################## side bar ########################################################################

with st.sidebar:
    st.write("## Escolha uma categoria");
    selected_banco_categ = st.selectbox("Categoria", categoria_bancos, 0)

    df_core_categ = df_core_full;
    if selected_banco_categ != 'Todos':
        df_core_categ = df_core_full.query('agrupamento_bancos in (@selected_banco_categ)')


    st.write('## Escolha um banco')
    bancos_principais = ['Todos']+df_core_categ['banco_principal'].value_counts().to_frame().query('count >0').index.tolist()
    selected_banco = st.selectbox("Banco", bancos_principais, 0)

    if selected_banco != 'Todos':
        df_core = df_core_categ.query('banco_principal == @selected_banco')
    else:
        df_core = df_core_categ

    if len(df_core) < 10:
        st.write("Nenhum dado encontrado para a seleção. Considere mudar o filtro.")
        st.stop()


    st.write('## Opções dos gráficos')
    sortingChoice = st.selectbox("Ordenação",("Mesma dos dados", "Quantidade"),)
    acumChoice = st.toggle("Percentual acumulado")
    if acumChoice:
        cutoff = st.slider('Top%', 0.0, 1.0, 1.0,0.05)
    row_len = st.slider('Quantidade de colunas por linha', 1, 4, 2)

#st.write(len(df_core_full), len(df_core_categ), len(df_core))

df_nps_full = df_nps_full.merge(df_core_full[['id','agrupamento_bancos','banco_principal']], on='id', how='inner')
nps_categ = df_nps_full.merge(df_core_categ[['id']], on='id', how='inner')
nps_core = df_nps_full.merge(df_core[['id']], on='id', how='inner')


df_rankings_full = df_rankings_full.merge(df_core_full[['id','agrupamento_bancos','banco_principal']], on='id', how='inner')
df_rankings_categ = df_rankings_full.merge(df_core_categ[['id']], on='id', how='inner')
df_rankings_core = df_rankings_full.merge(df_core[['id']], on='id', how='inner')

############ Main Page  ########################################################################

############################################################################################################## 
# Visao questões do tipo NPS
st.title(f"Comportamento bancário {' - '+selected_banco if selected_banco != 'Todos' else ''}")


if len(df_core) == 0:
    st.write("Nenhum dado encontrado para a seleção. Considere mudar o filtro.")
    st.stop()

st.write(f" Os resultados abaixo foram preenchidos com  {len(df_core)} - {len(df_core)/len(df_core_full):0.1%} respondentes selecionados")


bank_categ_selected = st.multiselect("Escolha os agrupamentos de bancos",categoria_bancos,)


############ Charts functions  ########################################################################
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
        

def nps_chart(cel_container, df, x, y, title):
    if type(y) == str:
        y = [y]

    with cel_container:
        with chart_container(df):
            st.write(f"### {title.replace('_',' ').title()}")
            fig = make_subplots() 
            for c in y:
                fig.add_trace(go.Scatter(
                    y=df[x],
                    x=df[c], 
                    name=c.replace("_"," ").title(),
                    # text=[f"{v:.1%}" for v in df[c]],
                    textposition="top center",
                    # line_color="blue",
                    mode="text+lines"))
            
            fig.update_layout(
                legend=dict(orientation="h",yanchor="bottom",y=-1.02,x=-1),
                xaxis_range=[0,1],
                # title_text=f"{title.title().replace('_', ' ')}"
            )
            st.plotly_chart(fig, use_container_width=True)

def ranking_chart(cel_container, categ, df, x, y):
    with cel_container:
        with chart_container(df):
            fig = px.line(df,y=y,x=x,title=f"{categ.replace('_', ' ').title()}",)
            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=-1.02,x=-1))
            fig.update_layout(xaxis_range=[0,1])
            st.plotly_chart(fig, use_container_width=True)


############ data summarization  ########################################################################


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
    
    totals = df.groupby(['categoria']).agg(N=('id', 'nunique')).reset_index()
    df = (
        df
        .query(f'categoria == "{categ}"')
        .assign(rank=lambda x:x['rank'].apply(lambda x:f'R{x:02d}')) # colunando pelo rank
        .pivot_table(
            index=['categoria', 'prioridade'],
            columns='rank',
            values='id',
            aggfunc='nunique',
        )
        .reset_index()
        .merge(totals,on=['categoria'])
    )
    df = (
        df.assign(pct_prioridade_1_e_2=df[['R01','R02']].sum(axis=1)/df['N'])
        [['prioridade','pct_prioridade_1_e_2']]
    )

    return df


###########################################################################################################################
st.write('## Crédito e canais de contratação')

layout = RowProducer(row_len=row_len)
for categ in ['jornada_contratacao_credito_principal', 'atendimento_robo','planejamento_credito',  'capacidade_financeira']:
    # Banco atual
    temp = nps_filter(nps_core, categ).rename(columns={'pct_concordancia':'pct_concordancia_'+selected_banco.lower()})

    # adding categories
    selected_columns = ['pct_concordancia_'+selected_banco.lower()];
    for c in set(bank_categ_selected) - set([selected_banco]):
        if c == 'Todos':
            temp1 = nps_filter(df_nps_full, categ)
        else:
            temp1 = nps_filter(df_nps_full.query('agrupamento_bancos == @c'), categ)

    
        temp1 = temp1.rename(columns={'pct_concordancia':'pct_concordancia_'+c.lower()})
        temp = temp.merge(temp1, on='pergunta', how='left')
        selected_columns.append('pct_concordancia_'+c.lower())

    nps_chart(layout.getNext(), temp, x='pergunta', y=selected_columns, title=categ)


###########################################################################################################################
st.write('## Contratação de produtos')
layout = RowProducer(row_len=row_len)
for categ in ['cheque_especial','cartao_credito',    'crediario_digital', 'credito_parcelado']:
    # Banco atual
    temp = nps_filter(nps_core, categ).rename(columns={'pct_concordancia':'pct_concordancia_'+selected_banco.lower()})

    # adding categories
    selected_columns = ['pct_concordancia_'+selected_banco.lower()];
    for c in set(bank_categ_selected) - set([selected_banco]):
        if c == 'Todos':
            temp1 = nps_filter(df_nps_full, categ)
        else:
            temp1 = nps_filter(df_nps_full.query('agrupamento_bancos == @c'), categ)

    
        temp1 = temp1.rename(columns={'pct_concordancia':'pct_concordancia_'+c.lower()})
        temp = temp.merge(temp1, on='pergunta', how='left')
        selected_columns.append('pct_concordancia_'+c.lower())

    nps_chart(layout.getNext(), temp, x='pergunta', y=selected_columns, title=categ)


# ###########################################################################################################################
for categ in [ "fator_escolher_banco_emprestimo",'credito_parcelado_novo__importancia', "cartao_credito_novo__importancia", "credito_parcelado_novo__importancia"]:
    temp = ranking_filter(df_rankings_core, categ)
    selected_columns = ['pct_prioridade_1_e_2'];
    for c in bank_categ_selected:
        if c == 'Todos':
            temp1 = ranking_filter(df_rankings_full, categ)
        else:
            temp1 = ranking_filter(df_rankings_full.query('agrupamento_bancos == @c'), categ)

        temp1 = temp1.rename(columns={'pct_prioridade_1_e_2':'pct_prioridade_1_e_2_'+c.lower()})
        temp = temp.merge(temp1, on='prioridade', how='left')
        selected_columns.append('pct_prioridade_1_e_2_'+c.lower())


    # st.write(temp)

    nps_chart(layout.getNext(), temp, x='prioridade', y=selected_columns, title=categ)

###########################################################################################################################
st.write('## Inadimplência')
layout = RowProducer(row_len=row_len)
for categ in ['credito_negado', 'situacao_credito',   'endividamento', 'personalizacao_cobranca']:
    # Banco atual
    temp = nps_filter(nps_core, categ).rename(columns={'pct_concordancia':'pct_concordancia_'+selected_banco.lower()})

    # adding categories
    selected_columns = ['pct_concordancia_'+selected_banco.lower()];
    for c in set(bank_categ_selected) - set([selected_banco]):
        if c == 'Todos':
            temp1 = nps_filter(df_nps_full, categ)
        else:
            temp1 = nps_filter(df_nps_full.query('agrupamento_bancos == @c'), categ)

    
        temp1 = temp1.rename(columns={'pct_concordancia':'pct_concordancia_'+c.lower()})
        temp = temp.merge(temp1, on='pergunta', how='left')
        selected_columns.append('pct_concordancia_'+c.lower())

    nps_chart(layout.getNext(), temp, x='pergunta', y=selected_columns, title=categ)

for categ in ['meio_pagamento_preferencial', 'prioridadePagamentoRank','melhorias_processo_cobranca'
              ,'tipo_ofertas_renegociacao','inadimplencia__melhor_forma_de_saber']:

    temp = ranking_filter(df_rankings_core, categ).rename(columns={'pct_prioridade_1_e_2':'pct_prioridade_1_e_2_'+selected_banco.lower()})
    selected_columns = ['pct_prioridade_1_e_2_'+selected_banco.lower()];
    for c in bank_categ_selected:
        if c == 'Todos':
            temp1 = ranking_filter(df_rankings_full, categ)
        else:
            temp1 = ranking_filter(df_rankings_full.query('agrupamento_bancos == @c'), categ)

        temp1 = temp1.rename(columns={'pct_prioridade_1_e_2':'pct_prioridade_1_e_2_'+c.lower()})
        temp = temp.merge(temp1, on='prioridade', how='left')
        selected_columns.append('pct_prioridade_1_e_2_'+c.lower())


    # st.write(temp)

    nps_chart(layout.getNext(), temp, x='prioridade', y=selected_columns, title=categ)