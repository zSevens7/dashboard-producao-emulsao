import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta

def grafico_evolucao(df, coluna_y, cor_linha, titulo_media):
    """
    Gera um gráfico de linha temporal com linha de média.
    """
    fig = px.line(df, x='Data', y=coluna_y, markers=True)
    fig.update_traces(line_color=cor_linha, line_width=3)
    
    # Adiciona linha de média
    media = df[coluna_y].mean()
    fig.add_hline(y=media, line_dash="dot", line_color="gray", 
                  annotation_text=f"{titulo_media}: {media:.1f}", 
                  annotation_position="bottom right")
    
    fig.update_layout(height=400, hovermode="x unified", margin=dict(l=20, r=20, t=40, b=20))
    return fig

# --- NOVA FUNÇÃO (PEDIDO DO CLIENTE) ---
def grafico_barras_mensal(df):
    """
    Gera gráfico de barras com o TOTAL ACUMULADO por mês.
    Ordena cronologicamente (Jan/25 -> Fev/25...).
    """
    df_temp = df.copy()
    
    # Cria coluna de ordenação (Periodo) e visual (Texto)
    df_temp['Periodo'] = df_temp['Data'].dt.to_period('M')
    
    # Agrupa somando a produção
    df_agrupado = df_temp.groupby('Periodo')['Diário (Ton)'].sum().reset_index()
    
    # Cria a coluna visual bonita (Ex: 01/2025)
    df_agrupado['Mes_Visual'] = df_agrupado['Periodo'].dt.strftime('%m/%Y')
    
    # Ordena pelo Periodo (tempo real) e não pelo texto
    df_agrupado = df_agrupado.sort_values('Periodo')

    fig = px.bar(
        df_agrupado, 
        x='Mes_Visual', 
        y='Diário (Ton)',
        title="Produção Total Acumulada (Mês a Mês)",
        text_auto='.0f' # Mostra o valor arredondado em cima da barra
    )
    
    # Estilização
    fig.update_traces(marker_color='#00d4ff') # Azul Neon
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Total (Ton)",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig
# ---------------------------------------

def grafico_comparativo_barras(df):
    """
    Gera barras agrupadas (Dia vs Noite) lado a lado.
    """
    df_melt = df.melt(id_vars=['Data'], value_vars=['Turno Dia (Ton)', 'Turno Noite (Ton)'], 
                      var_name='Turno', value_name='Ton')
    
    fig = px.bar(df_melt, x='Data', y='Ton', color='Turno', barmode='group',
                 color_discrete_map={'Turno Dia (Ton)': '#ff9f1c', 'Turno Noite (Ton)': '#2ec4b6'})
    
    fig.update_layout(height=400, xaxis_title=None, legend_title=None, margin=dict(l=20, r=20, t=20, b=20))
    return fig

def grafico_comparativo_pizza(df):
    """
    Gera gráfico de pizza mostrando a fatias da produção total.
    """
    total_dia = df['Turno Dia (Ton)'].sum()
    total_noite = df['Turno Noite (Ton)'].sum()
    
    dados_pizza = pd.DataFrame({
        'Turno': ['Turno Dia', 'Turno Noite'],
        'Total': [total_dia, total_noite]
    })
    
    fig = px.pie(dados_pizza, values='Total', names='Turno', hole=0.4,
                 color='Turno',
                 color_discrete_map={'Turno Dia': '#ff9f1c', 'Turno Noite': '#2ec4b6'})
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
    return fig

def grafico_media_semanal(df):
    """
    Gera barras com a MÉDIA por dia da semana.
    """
    df_temp = df.copy()
    df_temp['Dia_Num'] = df_temp['Data'].dt.dayofweek 
    df_agrupado = df_temp.groupby('Dia_Num')['Diário (Ton)'].mean().reset_index()
    
    mapa = {
        0: 'Segunda', 1: 'Terça', 2: 'Quarta', 3: 'Quinta', 
        4: 'Sexta', 5: 'Sábado', 6: 'Domingo'
    }
    df_agrupado['Dia_Nome'] = df_agrupado['Dia_Num'].map(mapa)
    df_agrupado = df_agrupado.sort_values('Dia_Num')
    
    fig = px.bar(
        df_agrupado, x='Dia_Nome', y='Diário (Ton)',
        title="Média de Produtividade Típica (Por Dia da Semana)",
        text_auto='.1f',
        color='Diário (Ton)', color_continuous_scale='Blues'
    )
    
    fig.update_layout(xaxis_title=None, yaxis_title="Média (Ton)", height=400, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def grafico_previsao_prophet(df, forecast, titulo):
    """
    (Legado) Gera um gráfico comparando o real com a previsão do Prophet.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Data'], y=df['Diário (Ton)'], name='Histórico Real',
        line=dict(color='#0068c9', width=2)
    ))

    df_futuro = forecast[forecast['ds'] > df['Data'].max()]
    
    fig.add_trace(go.Scatter(
        x=df_futuro['ds'], y=df_futuro['yhat'], name='Previsão (IA)',
        line=dict(color='orange', width=3, dash='dot')
    ))

    fig.add_trace(go.Scatter(
        x=df_futuro['ds'].tolist() + df_futuro['ds'].tolist()[::-1],
        y=df_futuro['yhat_upper'].tolist() + df_futuro['yhat_lower'].tolist()[::-1],
        fill='toself', fillcolor='rgba(255,165,0,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip", showlegend=False, name='Margem de Erro'
    ))

    fig.update_layout(title=titulo, xaxis_title="Tempo", yaxis_title="Toneladas", height=450, hovermode="x unified")
    return fig

def grafico_previsao_detalhado(df, forecast, coluna_y, titulo):
    """
    Gera gráfico com Zoom de 3 meses + Previsão
    """
    fig = go.Figure()

    # --- Filtro de Zoom (Últimos 90 dias) ---
    data_corte = df['Data'].max() - timedelta(days=90)
    df_recente = df[df['Data'] >= data_corte]

    # 1. Dados Reais (Apenas os últimos 90 dias)
    fig.add_trace(go.Scatter(
        x=df_recente['Data'], y=df_recente[coluna_y],
        name='Realidade (Últimos 3 meses)', mode='lines+markers',
        line=dict(color='#0068c9', width=3),
        marker=dict(size=6)
    ))

    # 2. Previsão (Laranja Pontilhado)
    df_futuro = forecast[forecast['ds'] > df['Data'].max()]
    
    fig.add_trace(go.Scatter(
        x=df_futuro['ds'], y=df_futuro['yhat'],
        name='Previsão IA',
        line=dict(color='#ff9f1c', width=4, dash='dot')
    ))

    # 3. Margem de Incerteza (Sombra)
    fig.add_trace(go.Scatter(
        x=df_futuro['ds'].tolist() + df_futuro['ds'].tolist()[::-1],
        y=df_futuro['yhat_upper'].tolist() + df_futuro['yhat_lower'].tolist()[::-1],
        fill='toself', fillcolor='rgba(255, 159, 28, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Margem de Incerteza'
    ))

    fig.update_layout(
        height=500, hovermode="x unified", title=titulo,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig