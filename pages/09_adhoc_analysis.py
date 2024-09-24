import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from streamlit_extras.chart_container import chart_container

import duckdb


# including the parent folder on the path
import sys
sys.path.append('..')

import constants
import pandas_utils
from data_model import categoricals_demographics, load_survey_core, load_know_bank, load_nps_questions, load_ranking_questions


################## Page config ########################################################################
st.set_page_config(layout="wide")


core = load_survey_core()
nps = load_nps_questions()
rankings = load_ranking_questions()

st.title("Ad-hoc Analysis - Using SQL")

with st.expander("Exemplos das tableas"):
    st.write("Exemplos de tabelas disponíveis para consulta")
    st.write("utilize a columna id para unir as tabelas")
    tabs = st.tabs(["Core", "NPS", "Ranking"])

    for cont, table, title in zip(tabs, [core, nps, rankings], ['Core', 'Dados do tipo NPS', 'Dados do tipo Ranking']):
        with cont:
            st.write("# "+title)
            st.write(table.dtypes.to_frame('tipo de dados'))

            st.write("Sample")
            st.dataframe(table.sample(10))


if 'consultaSQL'  in st.session_state:
    consultaSQL= st.session_state['consultaSQL']
else:
    consultaSQL = "select * from core limit 10"
consulta = st.text_area("SQL Query", consultaSQL)
st.session_state['consultaSQL'] = consulta
st.download_button(label="Download query", data=consulta, file_name="my_query.sql", mime="text/sql")

st.write("### Resultado da consulta")
df_resultado = duckdb.sql(consulta).df()

st.dataframe(df_resultado)

