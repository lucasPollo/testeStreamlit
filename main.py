import streamlit as st
import pandas as pd
import yfinance as yf





#funcoes de carregamento de dados
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas)
    dados_acao = yf.Tickers(texto_tickers)
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-08-01")
    print(cotacoes_acao)
    cotacoes_acao = cotacoes_acao["Close"]
    return cotacoes_acao

@st.cache_data
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";")
    tickers = list(base_tickers["Código"])
    tickers = [item + ".SA" for item in tickers]
    return tickers

acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)

#criar a interface streamlit
st.write("""
### PREÇO DE AÇOES
         """)


    
#prepara a visualizaçao = filtros

st.sidebar.header("Filtros")

#filtro de açoes
lista_acoes = st.sidebar.multiselect("Escolha a ação para visualizar",dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
print(dados)


#filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()
intervalo_datas = st.sidebar.slider("Selecione o período", min_value=data_inicial, max_value=data_final, value=(data_inicial, data_final))
print(intervalo_datas[1])
dados = dados.loc[intervalo_datas[0]:intervalo_datas[1]]





#sempre depois dos codigos
#criar o grafico
st.line_chart(dados)


texto_performance_ativos = ""

if len(lista_acoes) == 0:
    lista_acoes = list(dados.columns)
    
elif len(lista_acoes):
    dados = dados.rename(columns={"Close": acao_unica})

for acao in lista_acoes:
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)
    print(performance_ativo)
    
    if performance_ativo > 0:
        #:cor[texto]
       texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :green[{performance_ativo:.1%}]"
        
    elif performance_ativo  < 0:
         texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{performance_ativo:.1%}]"
    else:
         texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"
   
    
st.write(f"""
### PERFORMANCE DE ATIVOS
Essa foi a perfomance de cada ativo no período selecionado:

{texto_performance_ativos}
         """)


