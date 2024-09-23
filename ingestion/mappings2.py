mapSimNao = {
    0:'Não',
    1:'Sim',
    2:'Erro',
    3:'Erro',
    4:'Erro',
    5:'Erro',
}

map_genero = {
    1: 'Masculino',
    2: 'Feminino',
    #3: 'Other',
    #4: 'Prefer not to answer',
    3:'Masculino',
    4:'Feminino',
}

map_faixa_idade = {
    1: "18-24",
    2: "25-34",
    3: "35-44",
    4: "45-54",
    5: "55-64",
    6: " 65-74",
    7: "75+",
}

tipo_trabalho_map = {
    1: 'Empregado tempo integral',
    2: 'Empregado tempo parcial',
    3: 'Autonomo',
    4: 'Estudante',
    5: 'Cuido da casa',
    6: 'Aposentado',
    7: 'Desempregado',
    97: 'Outros',
    99: 'Outros'	
}

map_estado = {
    1: 'Acre',
    2: 'Alagoas',
    3: 'Amapá',
    4: 'Amazonas',
    5: 'Bahia',
    6: 'Brasília - Distrito Federal',
    7: 'Ceará',
    8: 'Espírito Santo',
    9: 'Goiás',
    10: 'Maranhão',
    11: 'Mato Grosso',
    12: 'Mato Grosso do Sul',
    13: 'Minas Gerais',
    14: 'Pará',
    15: 'Paraíba',
    16: 'Paraná',
    17: 'Pernambuco',
    18: 'Piauí',
    19: 'Rio de Janeiro',
    20: 'Rio Grande do Norte',
    21: 'Rio Grande do Sul',
    22: 'Rondônia',
    23: 'Roraima',
    24: 'Santa Catarina',
    25: 'São Paulo',
    26: 'Sergipe',
    27: 'Tocantins',
}

map_regiao = {
    1: 'Norte',
    2: 'Centro Oeste',
    3: 'Nordeste',
    4: 'Sul',
    5: 'Sudeste',
}

map_capital = {
    1: 'Capital',
    2: 'Região Metropolitana',
    3: 'Interior',
}

map_faixa_renda = {
    201: 'Até 1412',
    202: '1.413 a 2.824',
    203: '2.825 a 3.135',
    204: '3.136 a 4.236',
    205: '4.237 a 5.648',
    206: '5.649 a 7.060',
    207: '7.060 a 8.472',
    208: '8.473 a 9.884',
    209: '9.885 a 11.296',
    210: '11.297 a 12.708',
    211: '12.708 a 14.120',
    212: '14.120 a 15.532',
    213: 'Mais 15.532',
    299: 'Prefiro não responder',
}

map_bancarizado = {
    1: 'Não possuo conta',
    2: 'Possuo conta mas não uso',
    3: 'Possuo conta'
}

depara_bancos = {
    1:'Agibank',
    2:'AgZero',
    3:'BB',
    4:'Original',
    5:'Pan',
    6:'Bradesco',
    7:'BS2',
    8:'BTG',
    9:'BV',
    10:'C6',
    11:'CEF',
    12:'Crefisa',
    13:'Daycoval',
    14:'Digio',
    15:'Help',
    16:'Inter',
    17:'Itau',
    18:'Iti',
    19:'MercadoPago',
    20:'Neon',
    21:'Next',
    22:'Nubank',
    23:'PagBank',
    24:'PicPay',
    25:'Safra',
    26:'Santander',
    27:'Sicoob',
    28:'Sicredi',
    29:'Unicred',
    30:'XP',
    88:'Outros'
}


map_considera_contratacao = {
    # 1:'Nunca considerei ter qualquer produto',
    # 2:'Considerei, mas nunca tive algum produto contratado',
    # 3:'Já tive algum produto contratado, mas não atualmente',
    # 4:'Tenho um produto contratado atualmente',
    1: 'Não',
    2: 'Considerei',
    3: 'Já tive',
    4: 'Tenho atualmente'
}

depara_produtos = {
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

nps_map = {
    1:'Discordo totalmente',
    2:'Discordo',
    3:'Discordo em partes',
    4:'Concordo em partes',
    5:'Concordo',
    6:'Concordo totalmente',
    7:'Não se aplica',
}

defaulter_map = {
    1:'Não',
    23:'Sim',
}

default_detalhe_map = {
    1:'Não',
    2:'Não, mas já tive atraso >30 em 12 meses',
    3:'Sim, estou com contas em atraso'
}

prioridade_pgto_map = {
    1: 'Compra de alimentos e produtos de higiene e limpeza',
    2: 'Pagar no prazo as contas mensais',
    3: 'Compra de vestuário e calçados',
    4: 'Compras com lazer',
    5: 'Gastos recorrentes',
    6: 'Pagamento de empréstimos/financiamentos que ainda estão em dia',
    7: 'Pagar as contas que estão em atraso para limpar o nome',
}

futuro_map = {
    1: 'Muito pior',
    2: 'Pior',
    3: 'Igual',
    4: 'Melhor',
    5: 'Muito melhor'
}

suporte_contratacao_map = {
    # 1: 'Prefiro contratar de forma totalmente independente, sem apoio de gerente',
    # 2: 'Gosto de avaliar opções, mas ter suporte do gerente na formalização da contratação',
    # 3: 'Gosto de 100% de suporte do gerente'
    1: 'Sem suporte',
    2: 'Com suporte para formalizacao',
    3: 'Com suporte do gerente',
}

prioridade_canal_contratacao = {
    1:'Celular',
    2:'Website',
    3:'Telefone',
    4:'Whatsapp',
    5:'Pessoalmente'
}

fatores_escolha_banco_credito = {
    1: 'Simple and easy to understand credit information ',
    2: 'Relationship time with financial institution',
    3: 'Simplified process for applying for credit',
    4: 'Quick response on credit approval',
    5: 'Quick to have access to the desired credit/value in the current account',
    6: 'Attractive interest rates',
    7: 'Monthly installments that fit the budget',
    8: 'Other',
}

uso_limite_conta_map = {
    1: 'Uso todos os meses por mais de 10 dias',
    2: 'Uso todos os meses por menos e 10 dias',
    3: 'Uso esporadicamente (ex: 1 vez a cada 3 meses)',
    4: 'Uso muito raramente (ex: Não mais que uma vez a cada 6 meses)',
    5: 'Não uso limite do cheque especial em hipótese nenhuma',
}

ncartoes_map = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
}

escolaridade_map = {
    1: 'fundamental incompleto',
    2: 'fundamental completo',
    3: 'médio incompleto',
    4: 'médio completo',
    5: 'graduação incompleta',
    6: 'graduação completa',
    7: 'pos-graduação',
    # outros
    8: 'fundamental incompleto',
    9: 'fundamental incompleto',
    97:'fundamental incompleto',
    99:'fundamental incompleto'
}

consistencia_pagamento_cartao_map = {
    1: 'eu pago em dia o valor integral da fatura',
    2: 'eu pago em dia o valor entre o mínimo e o total da fatura',
    3: 'eu pago em atraso o valor integral da fatura',
    4: 'eu pago em atraso o valor entre o mínimo e o total da fatura',
    5: 'unca pago em dia nem o valor integral e nem o valor mínimo da fatura',
}


comprometimento_renda_com_parcelas_map = {
    1: '<= 5%',
    2: '6% - 30%',
    3: '31% - 50%',
    4: '>50%',
}

estado_civil_map = {
    1: 'Solteiro',
    2: 'Casado',
    3: 'Separado',
    4: 'Viuvo',
    99: 'Prefiro nao responder'
}

transparencia_comunicacao_map = {
    1:'Sim',
    2:'Não',
    3:'Não sei',
}

importancia_cartao_novo_map = {
    1:'Aumentar meu limite',
    2: 'Pagar menos anuidade',
    3: 'Taxa de juros baixa',
    4: 'Cashback',
    5: 'Progama de fidelidade',
    6: 'Outros'
}

importancia_em_emprestimo_map = {
    1:	'Valor emprestado',
    2:	'Taxa de juros',
    3:	'Prazo de pagamento',
    4:	'Rapidez para aprovação/recursos na conta',
    5:	'Valor da parcela',
    6:	'Outro (especifique)',
}




melhor_forma_saber_sobre_inadimplencia_map = {
    1: 'Ligação de um consultor',
    2: 'Ligação do gerente da conta',
    3: 'WhatsApp',
    4: 'SMS',
    5: 'Aplicativo/Site da instituição financeira/loja',
    6: 'Outras plataformas de negociação (Serasa Limpa Nome, etc.)',
    7: 'Recebimento de email',
    8: 'Receber carta',
    9: 'Presença na agência/loja',
    10: 'Outro',
}


melhorias_processo_cobranca_map = {
    1: 'Reduzir o numero de ligacoes',
    2: 'Ligar quando estou disponível',
    3: 'Entrar em contato por outros canais',
    4: 'Ser mais cordial',
    5: 'Ter uma plataforma ou app melhor para negociar as dividas',
    6: 'Outros',
}

faixa_divida_map = {
    1: '<500',
    2: '500 - 1,000',
    3: '1000 - 3000',
    4: '3000 - 5000',
    5: '>5000',
    6: 'Não sei ou perdi o controle do quanto devo',
}


faixa_meses_inadimplente_map = {
    1: '<1',
    2: '01 a 02',
    3: '03 a 06',
    4: '06 a 11',
    5: '12>',
}

tipo_ofertas_renegociacao_map ={
    1: 'Prefiro pagamento à vista com desconto no total devido',
    2: 'Prefiro a prazo com maior número de parcelas, mas sem desconto',
    3: 'Prefiro negociar a prazo de forma que a parcela caiba em meu orçamento, sem estender por muito tempo',
    4: 'Prefiro poder realizar pagamentos mais frequentes (p.ex.: semanal)',
    5: 'Prefiro ter flexibilidade no pagamento, ou seja, poder adiantar parcelas, pagando uma quantia maior quando for favorável para mim, e/ou postergar em momentos de maior dificuldade',
    6: 'Gostaria de poder unificar minhas dívidas em uma única renegociação',
    7: 'Outro'
}

meio_pagamento_preferencial_map ={
    1: 'boleto',
    2: 'PIX',
    3: 'transferencia',
    4: 'dinheiro na loterica',
    5: 'dinheiro na agencia ou loja',
    6: 'cartao de credito',
    7: 'debito em conta',
    8: 'outros',
}

prazo_pretende_quitar_map ={
    1: '<30 dias',
    2: '31 a 90 dias',
    3: '91 a 180 dias',
    4: '>180 dias',
    5: 'Sem previsão',
}

fator_mudar_banco_map = {
    1: 'Credito aprovado com maior agilidade',
    2: 'Maior limite de credito rotativo',
    3: 'Maior limite para financiamento',
    4: 'Taxas menores para financiamento',
    5: 'Maior prazo ou parcelas mais baratas para financiamento',
    97: 'Outros',
    99: 'Nada',
}

meses_inadimplentes_map= {
    1: '<1',
    2: '01 a 02',
    3: '03 a 06',
    4: '06 a 11',
    5: '12>',
}

    

mapeamento = [
    {'col':'QSGEND', 'rename':'genero', 'map':map_genero},
    {'col':'QSSTATE', 'rename':'estado', 'map':map_estado},
    {'col':'QREGION', 'rename':'regiao', 'map':map_regiao},
    {'col':'QSCAPITAL', 'rename':'capital', 'map':map_capital},
    {'col':'QDMARITAL', 'rename':'estado_civil', 'map':estado_civil_map},
    {'col':'QSINC', 'rename':'faixa_renda', 'map':map_faixa_renda},
    {'col':'QSESCOL', 'rename':'escolaridade', 'map':escolaridade_map},
    {'col':'QDWORK', 'rename':'tipo_emprego','map':tipo_trabalho_map},

    {'col':'QNB0', 'rename':'bancarizado_uso_conta', 'map':map_bancarizado},
    {'col':'QBANKED', 'rename':'ind_bancarizado', 'map':{3:'Bancarizado', 12:'Não bancarizado'}},
    {'col':'QNB1', 'rename':'cartao_loja', 'map':{1:'Possuo', 2:'Não possuo'}},
    {'col':'QSPRINCIPAL', 'rename':'banco_principal', 'map':{200+k:v for k,v in depara_bancos.items()}},
    {'col':'QDEFAULTER', 'rename':'default', 'map':defaulter_map},
    {'col':'QINA', 'rename':'default_detalhe', 'map':default_detalhe_map},
    {'col':'QFUT', 'rename':'perspectiva_futuro', 'map':futuro_map},
    {'col':'Q19', 'rename':'nivel_suporte_contratacao', 'map':suporte_contratacao_map},
    {'col':'Q48', 'rename':'transparencia_comunicacao', 'map':transparencia_comunicacao_map},
    {'col':'Q27', 'rename':'uso_limite_conta_corr_12_meses', 'map':uso_limite_conta_map},
    {'col':'Q29', 'rename':'consistencia_pagamento_cartao', 'map':consistencia_pagamento_cartao_map},
    {'col':'Q35', 'rename':'comprometimento_renda_com_parcelas', 'map':comprometimento_renda_com_parcelas_map},
    {'col':'Q50', 'rename':'credito_parcelado__aceito_outros_parcelamentos_alem_do_cartao', 'map':nps_map},
    {'col':'Q36', 'rename':'valor_em_atraso', 'map':faixa_divida_map},
    {'col':'Q37', 'rename':'meses_inadimplentes', 'map':meses_inadimplentes_map},
    {'col':'Q47', 'rename':'prazo_pretende_quitar', 'map':prazo_pretende_quitar_map},
    
]

    

    
mapeamento += [{'col':f'Q18RANK{i}',   'rename':f'canal_contratacao_prioridade__{i}', 'map':prioridade_canal_contratacao} for i in  [1,2,3,4,5]]
mapeamento += [{'col':f'Q30RANK{i}',   'rename':f'cartao_credito_novo__importancia__{i}', 'map':importancia_cartao_novo_map} for i in  [1,2,3,4,5]]
mapeamento += [{'col':f'Q34RANK{i}',   'rename':f'credito_parcelado_novo__importancia__{i}', 'map':importancia_em_emprestimo_map} for i in  [1,2,3,4,5]]
mapeamento += [{'col':f'Q41RANK{i}',   'rename':f'inadimplencia__melhor_forma_de_saber__{i}', 'map':melhor_forma_saber_sobre_inadimplencia_map} for i in  [1,2,3,4,5]]
mapeamento += [{'col':f'Q44RANK{i}',   'rename':f'melhorias_processo_cobranca__{i}', 'map':melhorias_processo_cobranca_map} for i in  [1,2,3,4,5]]
mapeamento += [{'col':f'Q45RANK{i}',   'rename':f'tipo_ofertas_renegociacao__{i}', 'map':tipo_ofertas_renegociacao_map} for i in  [1,2,3,4,5]]
mapeamento += [{'col':f'Q46RANK{i}',   'rename':f'meio_pagamento_preferencial__{i}', 'map':meio_pagamento_preferencial_map} for i in  [1,2,3,4,5]]



mapeamento += [{'col':f'QPGTORANK{i}', 'rename':f'prioridadePagamentoRank__{i}', 'map':prioridade_pgto_map} for i in [1,2,3,4,5,6,7]]




mapeamento += [{'col':f'QSFUNN1.2{i:02d}', 'rename':f'Conhece_Banco__{banco}', 'map':mapSimNao} for i,banco in depara_bancos.items()]
mapeamento += [{'col':f'QSFUNN2R{200+i}',  'rename':f'Considera_Contracao__{banco}', 'map':map_considera_contratacao} for i,banco in depara_bancos.items()]
mapeamento += [{'col':f'Q28R{200+i}',      'rename':f'n_cartoes_banco__{banco}', 'map':ncartoes_map} for i,banco in depara_bancos.items()]
mapeamento += [{'col':f'QCURRENT.{200+i}', 'rename':f'PossuiConta__{banco}', 'map':mapSimNao} for i,banco in depara_bancos.items()]

mapeamento += [{'col':f'QPRODUCT_{200+i}.{j}', 'rename':f'ProdutoBanco__{banco}__{produto}', 'map':mapSimNao}
               for i,banco in depara_bancos.items()
                for j,produto in depara_produtos.items()]

mapeamento += [{'col':f'Q23.{k}',  'rename':f'fator_mudar_banco__{v.replace(' ','_')}', 'map':mapSimNao} for k,v in fator_mudar_banco_map.items()]

mapeamento +=[{ 'col':f'QATT1R{i+101}', 'rename':rename, 'map':nps_map,}
                for i, rename in enumerate([
                    'capacidade_financeira__invisto_5pct_renda' ,
                    'capacidade_financeira__possuo_reserva_emergencia' ,
                    'capacidade_financeira__recorro_credito' ,
                    'capacidade_financeira__uso_cheque_especial' ,
                    'capacidade_financeira__recorro_credito_para_compromissos',
                    'capacidade_financeira__recorro_familiares',
                ])]

mapeamento +=[{ 'col':f'QATT1R{i+201}', 'rename':rename, 'map':nps_map,}
                for i, rename in enumerate([
                    'endividamento__tenho_controle_despesas' ,
                    'endividamento__perdi_sono_por_causa_dividas' ,
                    'endividamento__gasto_mais_que_posso_pagar' ,
                    'endividamento__tolero_aumentar_endividamento_em_caso_de_necessidade' ,
                    'endividamento__costumo_ligar_renegociar',
                    'endividamento__me_preocupo_com_atraso_apenas_apos_contato',
                ])]


mapeamento +=[{ 'col':f'QATT2R{i+101}', 'rename':rename, 'map':nps_map,}
                for i, rename in enumerate([
                        'planejamento_credito__eu_me_planejo' ,
                        'planejamento_credito__pesquiso_opcoes' ,
                        'planejamento_credito__avalio_diferentes_instituicoes' ,
                        'planejamento_credito__preferencialmente_banco_principal' ,
                        'planejamento_credito__recorro_familia_amigos',
                        'planejamento_credito__so_recorro_familia_amigos_quando_nao_tenho_acesso_com_bancos',
                ])]

mapeamento +=[{ 'col':f'QATT2R{i+201}', 'rename':rename, 'map':nps_map,}
                for i, rename in enumerate([
                        'credito_negado__ja_tive_sem_saber_razao' ,
                        'credito_negado__recebo_justificativa' ,
                        'credito_negado__busco_outra_instituicao' ,
                        'credito_negado__ja_precisei_limpar_nome' ,
                        'credito_negado__tenho_dificuldades_mesmo_depois_de_limpar_nome',
                ])]

mapeamento +=[{ 'col':f'QATT2R{i+301}', 'rename':rename, 'map':nps_map,}
                for i, rename in enumerate([
                        'situacao_credito__ult12m_consegui_guardar_dinheiro' ,
                        'situacao_credito__ult12m_aumentei_endividamento' ,
                        'situacao_credito__ult12m_fique_inadimplente' ,
                ])]


mapeamento += [{'col':f'Q13.{i+1}', 'rename':f'origem_dinheiro_pagamento_contas__{renda}', 'map':mapSimNao}
               for i, renda in enumerate([
                   'salario',
                   'vender_bens',
                   'renda_extra',
                   'vender_ferias',
                   'reduzo_custo',
                   'cobro_divida_de_terceiros',
                   'uso_dinheiro_extra',
                   'empresto_de_parentes',
                   'outros'
               ])]

mapeamento += [{'col':f'Q49.{i+1}', 'rename':f'tendencias__{renda}', 'map':mapSimNao}
               for i, renda in enumerate([
                    'possuo_servico_streaming',
                    'uso_delivery',
                    'faco_compras_online',
                    'possuo_redes_sociais',
                    'uso_sites_apostas',
               ])]





mapeamento += [{'col':f'Q24R{i+1}',  'rename':col, 'map':nps_map} 
    for i, col in enumerate([
        'jornada_contratacao_credito_principal__consigo_contratar_100digital' ,
        'jornada_contratacao_credito_principal__processo_digital_intuitivo' ,
        'jornada_contratacao_credito_principal__informacoes_sao_claras' ,
        'jornada_contratacao_credito_principal__demandam_muitos_documentos_para_contratar_credito' ,
        'jornada_contratacao_credito_principal__aprovacao_rapida_de_credito',
        'jornada_contratacao_credito_principal__acesso_rapido_ao_dinheiro_apos_aprovacao',
        'jornada_contratacao_credito_principal__o_limite_atente'
    ])]

mapeamento += [{'col':f'Q25RANK{i}',   'rename':f'fator_escolher_banco_emprestimo__{i}', 'map':fatores_escolha_banco_credito} for i in  [1,2,3,4,5]]

mapeamento += [{'col':f'Q26R{i+1}',  'rename':col, 'map':nps_map} 
    for i, col in enumerate([
        'cheque_especial__usei_ultimos_12m' ,
        'cheque_especial__deveria_ser_maior' ,
        'cheque_especial__sei_taxa_juros' ,
        'cheque_especial__nao_uso_mesmo_tendo_limite' ,
        'cheque_especial__nao_tenho_cheque_especial' ,
    ])]

mapeamento += [{'col':f'Q31R{i+1}',  'rename':col, 'map':nps_map} 
    for i, col in enumerate([
        'cartao_credito__pretendo_obter_outro_proximos_12m' ,
        'cartao_credito__uso_cartao_quando_nao_tenho_dinheiro_em_conta' ,
        'cartao_credito__parcelei_nos_ult12m' ,
        'cartao_credito__eu_sei_taxa_juros_cobrada' ,
        'cartao_credito__eu_controlo_os_lancamentos' ,
    ])]




mapeamento += [{'col':f'Q32R{i+1}',  'rename':col, 'map':nps_map} 
    for i, col in enumerate([
        'credito_parcelado__conheco_credito_consignado',
        'credito_parcelado__conheco_emprestimo_pessoal' ,
        'credito_parcelado__conheco_parcelamento_loja_varejo_cdc' ,
        'credito_parcelado__conheco_emprestimo_com_garantia_investimentos_fgts' ,
        'credito_parcelado__conheco_emprestimo_com_garantia_imovel_automovel' ,
        'credito_parcelado__conheco_emprestimo_com_garantia_penhor' ,
    ])]

mapeamento += [{'col':f'Q38.{i+1}',  'rename':col, 'map':mapSimNao} 
    for i, col in enumerate([
        'inadimplente_no_produto__cartao_loja',
        'inadimplente_no_produto__cartao_credito',
        'inadimplente_no_produto__carne_boleto',
        'inadimplente_no_produto__cheque_devolvido',
        'inadimplente_no_produto__cheque_especial',
        'inadimplente_no_produto__emprestimo_pessoal',
        'inadimplente_no_produto__emprestimo_com_garantia',
    ])]

mapeamento += [{'col':f'Q39.{i+1}',  'rename':col, 'map':mapSimNao} 
    for i, col in enumerate([
        'gerou_inadimplencia__material_construcao',
        'gerou_inadimplencia__moveis_e_eletro',
        'gerou_inadimplencia__supermercado_alimentacao',
        'gerou_inadimplencia__vestuario_calcados',
        'gerou_inadimplencia__aluguel_condominio',
        'gerou_inadimplencia__agua_luz',
        'gerou_inadimplencia__tv_internet_telefone',
        'gerou_inadimplencia__saude',
        'gerou_inadimplencia__educacao',
        'gerou_inadimplencia__viagens',
    ])]

mapeamento += [{'col':f'Q40.{i+1}',  'rename':col, 'map':mapSimNao} 
    for i, col in enumerate([
        'impossibilitou_pagamento__salario_atrasado',
        'impossibilitou_pagamento__desemprego_familia',
        'impossibilitou_pagamento__despesa_extraordinaria',
        'impossibilitou_pagamento__despesa_saude',
        'impossibilitou_pagamento__despesa_aumentou',
        'impossibilitou_pagamento__autonomo_reducao_renda',
        'impossibilitou_pagamento__emprestei_nome_terceiros',
        'impossibilitou_pagamento__esquecimento',
    ])]

mapeamento += [{'col':f'Q42R{i+101}',  'rename':col, 'map':nps_map} 
    for i, col in enumerate([
        'atendimento_robo__costumo_desligar' ,
        'atendimento_robo__na_ligacao_solicito_redirecionamento_humano' ,
        'atendimento_robo__no_whats_solicito_redirecionamento_humano' ,
        'atendimento_robo__me_sinto_confortavel_para_renegociar_divida' ,
        'atendimento_robo__consigo_interagir_com_robo_para_renegociar' ,
        'atendimento_robo__preciso_repetir_informacoes_entre_canais'
    ])]

mapeamento += [{'col':f'Q42R{i+201}',  'rename':col, 'map':nps_map} 
    for i, col in enumerate([
        'personalizacao_cobranca__sou_contatado_pelo_canal_de_preferencia' ,
        'personalizacao_cobranca__acordo_com_o_que_posso_pagar' ,
        'personalizacao_cobranca__customizada_para_minha_situacao' ,
        'personalizacao_cobranca__atendimento_entende_razoes_da_minha_inadimplencia' ,
    ])]



mapeamento +=[{'col':f'Q51R{i+1}',  'rename':col, 'map':nps_map}
        for i, col in enumerate([
        'crediario_digital__garantia_usar_cripto',
        'crediario_digital__garantia_usar_fgts',
        'crediario_digital__garantia_ouro_joias',
        'crediario_digital__garantia_automovel',
        'crediario_digital__financiamento_auto_aceito_bloqueio_carro',
        'crediario_digital__garantia_imovel',
        'crediario_digital__financiamento_aceito_bloqueio_celular',
        ])
]


