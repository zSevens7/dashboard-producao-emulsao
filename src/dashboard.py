import streamlit as st
import pandas as pd
from datetime import datetime
# Importamos a fábrica de gráficos
from src.plots import (
    grafico_evolucao, 
    grafico_barras_mensal,
    grafico_comparativo_barras, 
    grafico_comparativo_pizza, 
    grafico_media_semanal,
    grafico_previsao_detalhado
)
# Importamos o cérebro da IA
from src.forecasting import executar_previsao

# --- FUNÇÃO NOVA: GERENCIADOR DE TEMAS (CORRIGIDO) ---
def configurar_tema_visual():
    """
    Cria o botão de troca de tema na barra lateral e aplica o CSS/Template.
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Aparência")
    
    # Botão de escolha
    if 'tema_escolhido' not in st.session_state:
        st.session_state['tema_escolhido'] = 'Azulado Noturno' # Padrão
    
    tema = st.sidebar.radio(
        "Escolha o estilo:",
        ["Azulado Noturno", "Claro (Dia)"],
        index=0 if st.session_state['tema_escolhido'] == 'Azulado Noturno' else 1
    )
    st.session_state['tema_escolhido'] = tema

    # Definição das Cores (CSS Injetado)
    if tema == "Azulado Noturno":
        template_grafico = "plotly_dark"
        css = """
        <style>
            /* Fundo Geral e Texto */
            .stApp { background-color: #0e1117; color: #fafafa; }
            [data-testid="stSidebar"] { background-color: #262730; }
            [data-testid="stHeader"] { background-color: #0e1117; }
            
            /* Cartões de KPI (Noturno) */
            div[data-testid="metric-container"] {
                background-color: #1c202a !important;
                border: 1px solid #333 !important;
            }
            /* Força o Texto dos KPIs para Branco */
            [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
                color: #ffffff !important;
            }
            
            p, h1, h2, h3, h4 { color: #fafafa !important; }
        </style>
        """
    else: # Tema Claro
        template_grafico = "plotly_white"
        css = """
        <style>
            /* Fundo Geral e Texto */
            .stApp { background-color: #ffffff; color: #31333F; }
            [data-testid="stSidebar"] { background-color: #f0f2f6; }
            [data-testid="stHeader"] { background-color: #ffffff; }
            
            /* Cartões de KPI (Claro) */
            div[data-testid="metric-container"] {
                background-color: #f9f9f9 !important;
                border: 1px solid #e0e0e0 !important;
            }
            /* AQUI ESTÁ A CORREÇÃO: Força o número para PRETO */
            [data-testid="stMetricValue"] {
                color: #000000 !important;
            }
            [data-testid="stMetricLabel"] {
                color: #555555 !important;
            }
            
            p, h1, h2, h3, h4 { color: #31333F !important; }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)
    return template_grafico

# ----------------------------------------

def render_kpis(df):
    if df.empty:
        st.warning("Sem dados para calcular indicadores.")
        return

    total = df['Diário (Ton)'].sum()
    media = df['Diário (Ton)'].mean()
    idx_max = df['Diário (Ton)'].idxmax()
    recorde_val = df.loc[idx_max, 'Diário (Ton)']
    recorde_data = df.loc[idx_max, 'Data'].strftime('%d/%b') 
    ultimo_val = df['Diário (Ton)'].iloc[-1]
    ultimo_data = df['Data'].iloc[-1].strftime('%d/%m')

    # O CSS dos cartões agora é controlado pela função configurar_tema_visual
    col1, col2, col3, col4 = st.columns(4)

    with col1: st.metric(label="📦 Produção Total", value=f"{total:,.0f} T")
    with col2: st.metric(label="📊 Média Diária", value=f"{media:,.1f} T")
    with col3: st.metric(label="🏆 Recorde", value=f"{recorde_val:,.1f} T", delta=f"Em {recorde_data}", delta_color="normal")
    with col4:
        diff_media = ultimo_val - media
        st.metric(label=f"📅 Último Dia ({ultimo_data})", value=f"{ultimo_val:,.1f} T", delta=f"{diff_media:,.1f} T vs Média")

def render_charts(df):
    # 1. Configura o Tema e pega o template correto
    template_grafico = configurar_tema_visual()
    
    st.markdown("### 📊 Centro de Análise e Inteligência")
    
    tabs = st.tabs([
        "🏭 Geral", "📅 Mensal", "☀️ Dia", "🌙 Noite", "⚖️ Comparativo", "📅 Sazonalidade", "🔮 Previsão IA"
    ])
    
    # Função auxiliar para aplicar o template
    def plotar(fig):
        fig.update_layout(template=template_grafico)
        st.plotly_chart(fig, use_container_width=True)

    # --- Aba 1: Geral ---
    with tabs[0]:
        st.markdown("#### Evolução Diária Detalhada")
        fig = grafico_evolucao(df, 'Diário (Ton)', '#0068c9', 'Média Geral')
        plotar(fig)

    # --- Aba 2: MENSAL ---
    with tabs[1]:
        st.markdown("#### Visão Gerencial (Acumulado)")
        
        # Correção para garantir que o gráfico mensal apareça
        from src.plots import grafico_barras_mensal
        fig_mes = grafico_barras_mensal(df)
        plotar(fig_mes)
        
        st.markdown("---")
        col_a, col_b = st.columns(2)
        total_periodo = df['Diário (Ton)'].sum()
        qtd_meses = df['Data'].dt.to_period('M').nunique()
        media_mensal = total_periodo / qtd_meses if qtd_meses > 0 else 0
        
        with col_a: st.metric("📅 Meses Analisados", f"{qtd_meses} meses")
        with col_b: st.metric("📈 Média de Produção Mensal", f"{media_mensal:,.1f} Ton/mês")

    # --- Aba 3: Dia ---
    with tabs[2]:
        st.markdown("#### Performance: Turno do Dia")
        fig = grafico_evolucao(df, 'Turno Dia (Ton)', '#ff9f1c', 'Média Dia')
        plotar(fig)

    # --- Aba 4: Noite ---
    with tabs[3]:
        st.markdown("#### Performance: Turno da Noite")
        fig = grafico_evolucao(df, 'Turno Noite (Ton)', '#2ec4b6', 'Média Noite')
        plotar(fig)

    # --- Aba 5: Comparativo ---
    with tabs[4]:
        st.markdown("#### Eficiência entre Turnos")
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = grafico_comparativo_barras(df)
            plotar(fig_bar)
        with col2:
            fig_pie = grafico_comparativo_pizza(df)
            plotar(fig_pie)

    # --- Aba 6: Sazonalidade ---
    with tabs[5]:
        st.markdown("#### Padrões de Dia da Semana")
        fig_semana = grafico_media_semanal(df)
        plotar(fig_semana)
        
        df_temp = df.copy()
        df_temp['Dia_Num'] = df_temp['Data'].dt.dayofweek
        medias = df_temp.groupby('Dia_Num')['Diário (Ton)'].mean()
        dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        if not medias.empty:
            st.info(f"💡 **Insight:** O dia de maior produtividade média é **{dias[medias.idxmax()]}**.")

    # --- Aba 7: Previsão IA ---
    with tabs[6]:
        st.markdown("#### 🔮 Inteligência Preditiva (Prophet)")
        st.write("Análise de tendência para os próximos 15 dias.")
        
        if st.button("🚀 Gerar Nova Previsão"):
            with st.spinner("A IA está calculando os padrões históricos..."):
                forecast, mae, rmse, model = executar_previsao(df)
                
                m1, m2 = st.columns(2)
                m1.metric("📉 Margem de Erro (MAE)", f"{mae:.2f} T")
                m2.metric("🎯 Precisão do Modelo (RMSE)", f"{rmse:.2f} T")
                
                fig_prev = grafico_previsao_detalhado(df, forecast, 'Diário (Ton)', "Projeção Detalhada")
                plotar(fig_prev)
                
                st.markdown("---")
                with st.expander("❓ Entenda o que a IA está dizendo"):
                    st.write(f"O **MAE** de {mae:.1f}T indica o erro médio diário.")
                
                ult_prev = forecast['yhat'].iloc[-1]
                base_prev = forecast['yhat'].iloc[-15]
                tendencia = ((ult_prev / base_prev) - 1) * 100
                
                c_a, c_b = st.columns([1, 2])
                with c_a:
                    if tendencia > 0: st.success(f"📈 Tendência: ALTA de {tendencia:.1f}%")
                    else: st.error(f"📉 Tendência: QUEDA de {tendencia:.1f}%")
                with c_b:
                    st.info(f"🤖 **Analista IA:** Projeção de {ult_prev:.1f} T.")