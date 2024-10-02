import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
import plotly.express as px
import altair as alt

st.set_page_config(layout="wide")

st.title('Aluguel de casas no Brasil')

@st.cache_data
def carregar_dados():
    tabela = pd.read_csv("houses_to_rent_v2.csv", decimal =",")
    return tabela 

with st.sidebar:
    st.title("Selecione as opções")
    dados = carregar_dados()
    cidadeimov = st.sidebar.selectbox("cidade", dados["city"].unique().tolist(), index=None)
    if cidadeimov:
        dados = dados[dados["city"] == cidadeimov]        
    areaimov = st.sidebar.selectbox("área do imóvel", dados["area"].unique().tolist(), index=None)
    if areaimov:
        dados = dados[dados["area"] == areaimov]
    quartosimov = st.sidebar.selectbox("quartos", dados["rooms"].unique(), index=None)
    if quartosimov:
        dados = dados[dados["rooms"] == quartosimov]
    banheirosimov = st.sidebar.selectbox("banheiros", dados["bathroom"].unique(), index=None)
    if banheirosimov:
        dados = dados[dados["bathroom"] == banheirosimov]
    vagasimov = st.sidebar.selectbox("vagas de garagem", dados["parking spaces"].unique(), index=None)
    if vagasimov:
        dados = dados[dados["parking spaces"] == vagasimov]
    andarimov = st.sidebar.selectbox("andar", dados["floor"].unique(), index=None)
    if andarimov:
        dados = dados[dados["floor"] == andarimov]
    animalimov = st.sidebar.selectbox("aceita animal?", dados["animal"].unique(), index=None)
    if animalimov:
        dados = dados[dados["animal"] == animalimov]
    moveisimov = st.sidebar.selectbox("mobiliado?", dados["furniture"].unique(), index=None)
    if moveisimov:
        dados = dados[dados["furniture"] == moveisimov]
    
col1, col2 = st.columns(2, vertical_alignment="bottom")
col3, col4, col5 = st.columns(3)

with col1:
    st.header("Quantidade de imóveis por cidade")
    qt_cidade = dados["city"].value_counts()
    st.bar_chart(qt_cidade)

with col2:     
    cidade_med = dados.groupby("city")[["total (R$)"]].mean().reset_index()
    valorcid = px.bar(cidade_med, x ="total (R$)", y ="city", title="Valor médio por cidade", orientation ="h")
    st.plotly_chart(valorcid)

scatter = alt.Chart(dados).mark_circle().encode(
    alt.X("area"),
    alt.Y("total (R$)"),
    alt.Color("city"), tooltip = ["city", "area", "total (R$)"]
    ).interactive()
st.altair_chart(scatter, theme="streamlit", use_container_width=True)

st.dataframe(dados, use_container_width=True)