import pandas as pd
import numpy as np

SURVEY_FILE = 'Pesquisa Credito PF - compacta.xlsx'

CATEG_REGIAO =  pd.CategoricalDtype(categories=['Norte','Nordeste','Centro Oeste',  'Sudeste', 'Sul'], ordered=True)

CATEG_MARITAL =  pd.CategoricalDtype(categories=['Solteiro','Casado','Separado',  'Viuvo','Prefiro nao responder'], ordered=True)
CATEG_NPS =  pd.CategoricalDtype(categories=[
    'Discordo totalmente','Discordo','Discordo em partes',  'Concordo em partes', 'Concordo','Concordo totalmente'
], ordered=True)


CATEG_EDUCATION=  pd.CategoricalDtype(
    categories=[
    'fundamental incompleto',
    'fundamental completo',
    'médio incompleto',
    'médio completo', 
    'graduação incompleta',
    'graduação completa',
    'pos-graduação'], ordered=True)

CATEG_INCOME_RANGE=  pd.CategoricalDtype(
    categories=[
    'Até 1412',
    '1.413 a 2.824',
    '2.825 a 3.135', 
    '3.136 a 4.236', 
    '4.237 a 5.648',
    '5.649 a 7.060',
    '7.060 a 8.472',
    '8.473 a 9.884',
    '9.885 a 11.296',
    '11.297 a 12.708', 
    '12.708 a 14.120',
    '14.120 a 15.532',
    'Mais 15.532',
    ], ordered=True
)

FAIXA_IDADE = {18:'18-24', 25:'25-34', 35:'35-44', 45:'45-54', 55:'55-64', 65:'65-74', 75:'75->'}
CATEG_AGE =  pd.CategoricalDtype(categories=list(FAIXA_IDADE.values()), ordered=True)



CATEG_JOB_TYPE=  pd.CategoricalDtype(
    categories=[
        'Autonomo',
        'Empregado tempo integral', 'Empregado tempo parcial',
        'Aposentado',  'Cuido da casa', 'Desempregado',
       'Estudante', 'Outros'
    ], ordered=True
)



agrupamento_bancos_geral = {
    'Nubank': 'Digitais',
    'CEF': 'BancoPublico',
    'BB': 'BancoPublico',
    'Itau': 'BancoTradicional',
    'Iti': 'BancoTradicional',
    'Bradesco': 'BancoTradicional',
    'Next': 'BancoTradicional',
    'PicPay': 'Digitais',
    'Original': 'Digitais',
    'MercadoPago': 'Digitais',
    'Santander': 'BancoTradicional',
    'PagBank': 'Digitais',
    'Inter': 'Digitais',
    'C6': 'Digitais',

    'XP': 'Investimentos',
    'BTG': 'Investimentos',
    'Safra': 'Investimentos',
    'AgZero': 'Investimentos',

    'Pan': 'Financeiras',
    'BV': 'Financeiras',
    'Crefisa': 'Financeiras',

    'Agibank': 'Digitais',
    'Daycoval': 'Digitais',
    'Sicredi': 'Cooperativa',
    'Sicoob': 'Cooperativa',
    'Unicred': 'Cooperativa',
    'Digio': 'Digitais',
    'Neon': 'Digitais',
    'Help': 'Digitais',
    'BS2': 'Digitais',
    'Outros': 'Outros'
 }

BANKS_JOB_TYPE=  pd.CategoricalDtype(
    categories=[
        'Nubank',
        'Itau',
        'CEF',
        'BB',
        'Bradesco',
        'Santander',
        'Original',
        'Pan',
        'BS2',
        'BTG',
        'BV',
        'C6',
        'Crefisa',
        'Daycoval',
        'Digio',
        'Help',
        'Inter',
        'Iti',
        'MercadoPago',
        'Neon',
        'Next',
        'PagBank',
        'PicPay',
        'Safra',
        'Sicoob',
        'Sicredi',
        'Unicred',
        'XP',
        'Agibank',
        'AgZero',
        'Outros'
       
    ], ordered=True
)


PRODUCTS = {
    1: 'conta poupanca',
    2: 'cheque especial',
    3: 'cartao de credito',
    4: 'credito pessoal',
    5: 'consig publico',
    6: 'consig privado',
    7: 'credito imobiliario',
    8: 'credito veiculo',
    9: 'cdc credito varejo',
    10: 'emprestimo com garantia de investimento fgts',
    11: 'emprestimo com garantia de auto ou imob',
    12: 'emprestimo com garantia de penhor',
    13: 'consorcio',
    14: 'investimentos',
    15: 'crypto',
    16: 'seguros',
    97: 'outros'
}

CATEG_PRODUCTS=  pd.CategoricalDtype(
    categories=list(PRODUCTS.values()), ordered=True
)




