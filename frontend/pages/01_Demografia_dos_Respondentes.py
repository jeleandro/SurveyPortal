import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.chart_container import chart_container

# including the parent folder on the path
import sys
sys.path.append('..')

import constants
import pandas_utils
from data_model import categoricals_demographics, load_survey_core, load_know_bank, load_nps_questions


##############################################################################################################
#### Page config
st.set_page_config(layout="wide")
df_core = load_survey_core()


##############################################################################################################
#### Side bar config

with st.sidebar:
    bancos_principais = ['']+df_core['banco_principal'].value_counts().index.values.tolist()
    chosenBank = ''
    st.write('## Escolha um banco')
    chosenBank = st.selectbox("Banco", bancos_principais, 0)

    if chosenBank != '':
        df_core = df_core.query('banco_principal == @chosenBank')


with st.sidebar:
    st.write('## Opções dos gráficos')
    sortingChoice = st.selectbox("Ordenação",("Mesma dos dados", "Quantidade"),)
    acumChoice = st.toggle("Percentual acumulado")
    if acumChoice:
        cutoff = st.slider('Top%', 0.0, 1.0, 1.0,0.05)

if st.sidebar.button("Limpar cache de dados"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()



##############################################################################################################
#### Page CSS
st.write(""" 
<style>
.insight_box {
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
}
         
.insight_box h1 {
    color: #333;
    font-size: 0.9em;
    margin: 0;
}

.staticTable th{background-color:#efefef; color:#777; border-radius:7px}
.staticTable td,th{padding:5px; border:1px solid #a0a0a0}
.staticTable tr:hover, td:hover{background-color:#aaFFaa !important;}       
</style>
""", unsafe_allow_html=True)

##############################################################################################################
st.title("Visão Demográfica")
st.html("""
<p>Abaixo segue uma visão interativa dos respondentes da pesquisa</p>
""")
st.write("<br/><br/>", unsafe_allow_html=True)



################################### CORE UTIL FUNCTIONS
def basicStats(df, column, precision=2):
    """
    Parameters:
        precision: number of decimal places
    """
    aggr = (
        df
        .groupby(column, dropna=False)
        .agg(
            n_default=('default', lambda x: (x=='Sim').sum()),
            n_bancarizado=('ind_bancarizado', lambda x: (x=='Bancarizado').sum()),
            n=('id', 'nunique'),
            default=('default', lambda x: (x=='Sim').mean()),
            bancarizacao=('ind_bancarizado', lambda x: (x=='Bancarizado').mean()),
        )
        .assign(pct_n=lambda x: x['n'] / x['n'].sum())
        .assign(pct_bancarizado=lambda x: x['n_bancarizado'] / x['n_bancarizado'].sum())
        .assign(pct_default=lambda x: x['n_default'] / x['n_default'].sum())
        [['n','pct_n', 'n_default','pct_default','default','n_bancarizado','pct_bancarizado', 'bancarizacao']]
        .assign(quadrante=lambda x:
                (x['bancarizacao'] > x['bancarizacao'].mean()).astype(int) +\
                (x['default'] > x['default'].mean()).astype(int)*10)
        .assign(quadrante=lambda x: x['quadrante'].apply(lambda x: f"{x:02d}"))
        .query('n > 10')
        .round(precision)
        .reset_index()
    )

    return aggr;


with st.expander("Filtre as informações demográficas:"):
    chart_cols = st.multiselect(
        "",
        categoricals_demographics,
        categoricals_demographics,
    )

for column in chart_cols + ['agrupamento_bancos']:
    if chosenBank != '' and column in ('banco_principal','agrupamento_bancos'):
        continue;
    
    column_view = column.title().replace('_', ' ')
    st.markdown(f"## {column_view}")
    df_stats = basicStats(df_core,column);

    if len(df_stats) == 0:
        st.write(f"Não há dados suficientes para esse banco")
        continue;


    if sortingChoice == "Quantidade":
        df_stats = df_stats.sort_values(by='n', ascending=False)


    pct_col = 'pct_n';
    if acumChoice:
        pct_col = 'pct_n_acc'
        df_stats = (
            df_stats
            .assign(pct_n_acc=lambda x:x['pct_n'].cumsum())
            .query(f'pct_n_acc <= {cutoff}')
        )

    with chart_container(df_stats):
        row = st.columns(3);

        # Population
        with row[0]:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(
                x=df_stats[column],
                y=df_stats['n'],
                name='Quantidade',
                textposition='auto',
                marker_color="darkgray",
                )
            )
            fig.add_trace(go.Scatter(
                x=df_stats[column],
                y=df_stats[pct_col],
                name='Percentual',
                text=[f"{v:.1%}" for v in df_stats[pct_col]],
                textposition="top center",
                line_color="blue",
                mode="text+lines"), secondary_y=True)
            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=-0.4,x=-0))
            st.plotly_chart(fig, use_container_width=True)

        # Population
        with row[1]:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Bar(
                x=df_stats[column],
                y=df_stats['pct_n'],
                name='Percentual população',
                textposition='auto',
                marker_color="darkgray",))
            
            fig.add_trace(go.Scatter(
                x=df_stats[column],
                y=df_stats['bancarizacao'],
                name='Bancarização',
                text=[f"{v:.1%}" for v in df_stats['bancarizacao']],
                textposition="top center",
                line_color="blue",
                mode="text+lines"), secondary_y=True)
                        
            fig.add_trace(go.Scatter(
                x=df_stats[column],
                y=df_stats['default'],
                name='Inadimplência',
                text=[f"{v:.1%}" for v in df_stats['default']],
                textposition="top center",
                line_color="red",
                mode="text+lines"), secondary_y=True)
            # fig.update_layout(
            #     title_text=f"{column.title().replace('_', ' ')}"
            # )
            fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=-0.42,x=0))
            st.plotly_chart(fig, use_container_width=True)

        #### ---- Buble chart
        with row[2]:
            df_stats = df_stats.query('n > 5')
            fig = px.scatter(df_stats,
                x="bancarizacao",
                y="default",
	            size="pct_n",
                color="quadrante",
                color_discrete_map={'00':'gray', '01':'blue', '10':'orange', '11':'red'},
                hover_name=column, 
                size_max=40
            )
            fig.add_hline(y=df_stats['default'].mean(), line_dash="dot", line_color="gray")
            fig.add_vline(x=df_stats['bancarizacao'].mean(),  line_dash="dot", line_color="gray")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


        metrics = []
        # Maior grupo
        df = df_stats.sort_values(by='n', ascending=False).dropna().head(1)
        metrics.append({
            'title':f'Mais representativo:',
            'group':df[column].values[0],
            'metric':df['pct_n'].values[0],
        })

        # Maior inadimplencia
        df = df_stats.sort_values(by='default', ascending=False).dropna().head(1)
        metrics.append({
            'title':f'Maior inadimplencia:',
            'group':df[column].values[0],
            'metric':df['default'].values[0],
        })

        # Menor inadimplencia
        df = df_stats.sort_values(by='default', ascending=False).dropna().tail(1)
        metrics.append({
            'title':f'Menor inadimplencia:',
            'group':df[column].values[0],
            'metric':df['default'].values[0],
        })
           

        # Maior bancarizacao
        df = df_stats.sort_values(by='bancarizacao', ascending=False).dropna().head(1)
        metrics.append({
            'title':f'Maior bancarizacao:',
            'group':df[column].values[0],
            'metric':df['bancarizacao'].values[0],
        })

        st.markdown(f"### Insights da {column_view}")
        cols = st.columns(len(metrics))

        for m, col in zip(metrics, cols):
            col.html(f"""<div class='insight_box'>
            <h1>{m['title']} {m['metric']:.1%}</h1>
            {m['group']} 
            </div>""")

##############################################################################################################
st.title("Visão combinada")

categoricals_demographics = [categoricals_demographics[-1]]+categoricals_demographics[:-1]

row = st.columns(3);
with row[0]:
    var1 = st.selectbox(
            "Eixo X",
            categoricals_demographics,
        )

with row[1]:
    var2 = st.selectbox(
            "Eixo Y",
            categoricals_demographics,
        )
    
with row[2]:
    varMetric = st.selectbox(
            "Métrica",
            ['n','pct_n', 'n_default','pct_default','default','n_bancarizado','pct_bancarizado', 'bancarizacao']
        )

if var1 != var2:
    df_cross = (
        df_core
        .groupby([var1,var2], dropna=False)
        .agg(
            n_default=('default', lambda x: (x=='Sim').sum()),
            n_bancarizado=('ind_bancarizado', lambda x: (x=='Bancarizado').sum()),
            n=('id', 'nunique'),
            default=('default', lambda x: (x=='Sim').mean()),
            bancarizacao=('ind_bancarizado', lambda x: (x=='Bancarizado').mean()),
        )
        .query('n > 0')
        .assign(pct_n=lambda x: x['n'] / x['n'].sum())
        .assign(pct_bancarizado=lambda x: x['n_bancarizado'] / x['n_bancarizado'].sum())
        .assign(pct_default=lambda x: x['n_default'] / x['n_default'].sum())
        [['n','pct_n', 'n_default','pct_default','default','n_bancarizado','pct_bancarizado', 'bancarizacao']]
        .round(2)
        .reset_index()
    )

    formatString = {
        'n':"{:d}",
        'pct_n':'{:0.1%}',
        'n_default':'{:}',
        'pct_default':'{:0.1%}',
        'default':'{:0.1%}',
        'n_bancarizado':'{:}',
        'pct_bancarizado':'{:0.1%}',
        'bancarizacao':'{:0.1%}',
    }

    def sortColumns(df):
        return df.sort_values(df.columns.values.tolist(), ascending=[False]*len(df.columns));


    with chart_container(df_cross):
        st.html(
            df_cross
            .pivot_table(index=var1, columns=var2, values=varMetric, aggfunc='sum', fill_value=0)
            .pipe(sortColumns)
            .style
            .set_table_attributes('class="staticTable"')
            .format(formatString[varMetric])
            .background_gradient(cmap='Grays')
            .to_html()
        )
    
   