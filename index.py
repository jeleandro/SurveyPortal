import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Pesquisa de Crédito PF 2024",
    page_icon="",
)

st.write("# Pesquisa de crédito PF 2024")

st.markdown("""
## Contexto

Essa pesquisa tem como objetivo entender comportamento bancário dos clientes, jornada de contratação de produtos,
causas da inadimplência e tendências do mundo de crédito.
            

## Extratificação
            
Os clientes foram extratificados em bancarizado versus não bancarizado e Inadimplente vs não inadimplentes,
fornecendo uma visão balanceada nas duas dimensões.
            

|                   |Inadimplente|Não Inadimplente|Total|
|-------------------|------------|----------------|-----|
|**Bancarizado**    |500         |500             |1000 |
|**Não Bancarizado**|300         |300             |600  |
|**Total**          |800         |800             |1600 |
""")

st.markdown("## Módulos da pesquisa:")
st.html("""

<style>.table td, .table th {border:1px solid #ccc; padding:5px}</style>

<table class='table'>
<thead>
<tr><th>Módulo</th><th>Público</th><th>Questões</th><th>Respondentes</th></tr>
</thead>
<tbody>
<tr><td>Screener</td><td>Todos</td><td>9</td><td>1600</td></tr>
<tr><td>Comportamento</td><td>Todos</td><td>8</td><td>1600</td></tr>
<tr><td>Crédito e linhas de financiamento</td><td>Bancarizados</td><td>17</td><td>1000</td></tr>
<tr><td>Inadimplência</td><td>Inadimplentes</td><td>12</td><td>800</td></tr>
<tr><td>Novas tendências</td><td>Todos</td><td>12</td><td>1600</td></tr>
</tbody>
</table>
""")


