import streamlit as st
from src.data_loader import carregar_dados
from src.filters import render_filters
from src.dashboard import render_kpis, render_charts

# Configuração da Página (Título e Ícone)
st.set_page_config(
    page_title="Painel de Produção - Emulsão",
    page_icon="🏭",
    layout="wide"
)

# Título Principal
st.title("🏭 Dashboard de Controle de Produção")
st.markdown("---")

# 1. Carregar Dados
try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

# 2. Sidebar e Filtros
df_filtrado, periodo_texto = render_filters(df)

# 3. Mostrar KPIs
st.subheader(f"Resumo Operacional: {periodo_texto}")
render_kpis(df_filtrado)

st.markdown("---")

# 4. Gráficos
if not df_filtrado.empty:
    render_charts(df_filtrado)
else:
    st.warning("Nenhum dado encontrado para o período selecionado.")

# Rodapé automático para atualizar via browser
st.markdown("---")
st.caption("Sistema de Monitoramento v1.0 | Conectado ao Google Sheets 🟢")