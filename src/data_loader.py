import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
from datetime import datetime

# Configuração de Cache para não ficar lendo a planilha a cada clique (Performance)
@st.cache_data(ttl=60)  # Atualiza os dados a cada 60 segundos
def carregar_dados():
    # --- CONEXÃO ---
    SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]
    
    # IMPORTANTE: O arquivo credentials.json deve estar na pasta principal do projeto
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
    client = gspread.authorize(creds)
    
    # Abrir planilha pelo link
    sheet = client.open_by_url("PLANILHA DO CLIENTE AQUI").sheet1
    data = sheet.get_all_values()
    
    # Criar DataFrame (Tabela do Python)
    df = pd.DataFrame(data[1:], columns=data[0])
    
    # --- TRATAMENTO ROBUSTO DE DADOS ---
    
    # 1. Converter Datas (DD/MM/YYYY)
    df['Data'] = pd.to_datetime(df['Data'], dayfirst=True, errors='coerce')
    
    # 2. Converter Números (Tratando o formato brasileiro: 1.000,00 -> 1000.00)
    cols_numericas = ['Diário (Ton)', 'Turno Dia (Ton)', 'Turno Noite (Ton)']
    for col in cols_numericas:
        if col in df.columns:
            # Remove pontos de milhar, troca vírgula decimal por ponto
            df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # 3. Tratamento dinâmico de Observações
    cols_padrao = ['Data', 'Diário (Ton)', 'Turno Dia (Ton)', 'Turno Noite (Ton)', 'Ano', 'Mês']
    col_obs = None
    for col in df.columns:
        if col not in cols_padrao and "Col" not in col and col != "":
             col_obs = col
    
    if col_obs:
        df['Observações'] = df[col_obs]
    else:
        df['Observações'] = ""

    # --- REGRAS DE NEGÓCIO (LIMPEZA DE ZEROS FALSOS) ---
    
    # A. Remove linhas onde a data é inválida (NaT)
    df = df.dropna(subset=['Data'])
    
    # B. Filtra até o dia de HOJE (ignora lançamentos acidentais no futuro)
    hoje = pd.Timestamp(datetime.now().date())
    df = df[df['Data'] <= hoje]
    
    # C. REGRA DE OURO: Corta a tabela no último dia que teve produção real (> 0)
    # Isso evita que dias que o Enoque ainda não preencheu apareçam como 0.0 T
    if not df.empty:
        # Acha a maior data onde a produção diária foi maior que zero
        ultima_data_com_producao = df[df['Diário (Ton)'] > 0]['Data'].max()
        
        # Se encontrou uma data válida, filtra para mostrar apenas até ela
        if pd.notnull(ultima_data_com_producao):
            df = df[df['Data'] <= ultima_data_com_producao]

    # Ordenar por data para garantir que os gráficos fiquem na sequência correta
    df = df.sort_values('Data')
    
    return df