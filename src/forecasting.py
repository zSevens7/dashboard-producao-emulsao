import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

def executar_previsao(df, coluna_alvo='Diário (Ton)', dias_futuros=15):
    # Preparar dados para o Prophet
    df_p = df[['Data', coluna_alvo]].rename(columns={'Data': 'ds', coluna_alvo: 'y'})
    
    # Treinar modelo
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df_p)
    
    # Prever futuro
    future = model.make_future_dataframe(periods=dias_futuros)
    forecast = model.predict(future)
    
    # --- MÉTRICAS DE ERRO ---
    # Comparamos o que o modelo previu para o passado com o que aconteceu de verdade
    df_merged = df_p.merge(forecast[['ds', 'yhat']], on='ds')
    mae = mean_absolute_error(df_merged['y'], df_merged['yhat'])
    rmse = np.sqrt(mean_squared_error(df_merged['y'], df_merged['yhat']))
    
    return forecast, mae, rmse, model