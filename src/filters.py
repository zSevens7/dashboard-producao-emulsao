import streamlit as st
import pandas as pd

def render_filters(df):
    st.sidebar.header("🔍 Filtros Avançados")
    
    # Dicionário para traduzir meses (Fica muito mais profissional)
    mapa_meses = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    
    # 1. Menu de Seleção (Colocamos "Todo o Histórico" PRIMEIRO para ser o padrão)
    opcoes_filtro = [
        "Todo o Histórico",
        "Ano Específico", 
        "Por Trimestre",
        "Mês Específico", 
        "Personalizado"
    ]
    
    tipo_filtro = st.sidebar.radio("Modo de Seleção:", opcoes_filtro)
    
    # Inicializa variáveis
    df_filtrado = df.copy()
    titulo_periodo = "Todo o Histórico"
    
    # --- LÓGICA DOS FILTROS ---
    
    if tipo_filtro == "Todo o Histórico":
        df_filtrado = df.copy()
        titulo_periodo = "Histórico Completo"

    elif tipo_filtro == "Ano Específico":
        anos_disponiveis = sorted(df['Data'].dt.year.unique(), reverse=True)
        ano_sel = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis)
        
        df_filtrado = df[df['Data'].dt.year == ano_sel]
        titulo_periodo = f"Ano de {ano_sel}"

    elif tipo_filtro == "Por Trimestre":
        anos_disponiveis = sorted(df['Data'].dt.year.unique(), reverse=True)
        ano_sel = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis)
        
        trimestre_sel = st.sidebar.selectbox(
            "Selecione o Trimestre", 
            ["1º Trimestre (Jan-Mar)", "2º Trimestre (Abr-Jun)", "3º Trimestre (Jul-Set)", "4º Trimestre (Out-Dez)"]
        )
        
        # Pega o primeiro número da string (1, 2, 3 ou 4)
        num_trimestre = int(trimestre_sel[0])
        
        df_filtrado = df[
            (df['Data'].dt.year == ano_sel) & 
            (df['Data'].dt.quarter == num_trimestre)
        ]
        titulo_periodo = f"{trimestre_sel} de {ano_sel}"

    elif tipo_filtro == "Mês Específico":
        anos_disponiveis = sorted(df['Data'].dt.year.unique(), reverse=True)
        ano_sel = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis)
        
        # Pega meses apenas daquele ano
        df_ano = df[df['Data'].dt.year == ano_sel]
        meses_ingles = df_ano['Data'].dt.month_name().unique()
        
        # Traduz para o usuário ver em Português
        meses_pt = [mapa_meses.get(m, m) for m in meses_ingles]
        mes_sel_pt = st.sidebar.selectbox("Selecione o Mês", meses_pt)
        
        # Destraduz para filtrar no Pandas (que usa inglês internamente)
        mes_sel_en = [k for k, v in mapa_meses.items() if v == mes_sel_pt][0]
        
        df_filtrado = df[
            (df['Data'].dt.year == ano_sel) & 
            (df['Data'].dt.month_name() == mes_sel_en)
        ]
        titulo_periodo = f"{mes_sel_pt} de {ano_sel}"

    elif tipo_filtro == "Personalizado":
        min_date = df['Data'].min().date()
        max_date = df['Data'].max().date()
        
        col1, col2 = st.sidebar.columns(2)
        d1 = col1.date_input("Início", min_date)
        d2 = col2.date_input("Fim", max_date)
        
        if d1 and d2:
            df_filtrado = df[
                (df['Data'].dt.date >= d1) & 
                (df['Data'].dt.date <= d2)
            ]
            titulo_periodo = f"De {d1.strftime('%d/%m')} a {d2.strftime('%d/%m')}"
            
    return df_filtrado, titulo_periodo