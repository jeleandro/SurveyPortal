import streamlit as st
import pandas as pd
import numpy as np

import constants


categoricals_demographics = ['faixa_idade', 'genero', 'estado_civil',   'capital', 'estado', 'regiao',
                              'escolaridade', 'faixa_renda', 'classe_social', 'tipo_emprego','banco_principal']
other_cols = ['ind_bancarizado','default']


@st.cache_data
def load_survey_core():
    df_pesquisa = pd.read_excel(f'../data/{constants.SURVEY_FILE}', sheet_name='pesquisa')
    
    df_pesquisa = (
        df_pesquisa
        .assign(faixa_idade=lambda x: x['faixa_idade'].map(constants.FAIXA_IDADE))
        
        .assign(classe_social=lambda x: x['faixa_renda'].map(constants.CATEG_SOCIAL_CLASS))
        [['id']+categoricals_demographics+other_cols]
        .assign(agrupamento_bancos=lambda x: x['banco_principal'].map(constants.agrupamento_bancos_geral))
        .assign(tipo_emprego=lambda x: x['tipo_emprego'].str.replace(')',''))

        # .astype({'faixa_idade':str})
        .astype({c:'category' for c in categoricals_demographics})
        .astype({'estado_civil':constants.CATEG_MARITAL})
        .astype({'escolaridade':constants.CATEG_EDUCATION})
        .astype({'faixa_renda':constants.CATEG_INCOME_RANGE})
        .astype({'tipo_emprego':constants.CATEG_JOB_TYPE})
        .astype({'regiao':constants.CATEG_REGIAO})
        .astype({'banco_principal':constants.BANKS_TYPE})
        .astype({'agrupamento_bancos':constants.CATEG_BANK_CATEG})
    
    )
    #"""
    return df_pesquisa


@st.cache_data
def load_know_bank():

    df = (
        pd.read_excel(f'../data/{constants.SURVEY_FILE}', sheet_name='conhece_banco')
        .assign(agrupamento_bancos=lambda x: x['banco'].map(constants.agrupamento_bancos_geral))
        .astype({'banco':'category'})
    )

    return df

@st.cache_data
def load_has_banck():
    df = (
        pd.read_excel(f'../data/{constants.SURVEY_FILE}', sheet_name='possui_banco')
    )

    return df

@st.cache_data
def load_nps_questions():
    df = (
        pd.read_excel(f'../data/{constants.SURVEY_FILE}', sheet_name='questoes_nps')
    )

    return df


@st.cache_data
def load_product_bank():
    df = (
        pd.read_excel(f'../data/{constants.SURVEY_FILE}', sheet_name='produto_por_banco')
    )

    return df


@st.cache_data
def load_ranking_questions():
    df = (
        pd.read_excel(f'../data/{constants.SURVEY_FILE}', sheet_name='questoes_ranking')
    )

    return df







