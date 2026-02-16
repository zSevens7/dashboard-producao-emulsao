# 🏭 Dashboard de Produção de Emulsão

> **Sistema de Business Intelligence (BI)** desenvolvido para monitoramento, análise e previsão de produção industrial.

![Status](https://img.shields.io/badge/Status-Concluído-success)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-red)
![IA](https://img.shields.io/badge/AI-Prophet-orange)

## 📄 Sobre o Projeto

Este painel foi desenvolvido sob demanda para uma planta industrial de emulsão asfáltica. O objetivo principal era substituir planilhas estáticas por uma **visualização de dados interativa, dinâmica e em tempo real**.

O sistema conecta-se diretamente à API do **Google Sheets**, processa os dados brutos com **Pandas** e gera visualizações estratégicas (KPIs, Gráficos de Evolução, Comparativos de Turno) utilizando **Plotly**. Além disso, implementa um módulo de **Inteligência Artificial (Facebook Prophet)** para prever a demanda futura baseada no histórico de produção.

---

## ✨ Funcionalidades Principais

* **📊 Monitoramento em Tempo Real:** Conexão direta com Google Sheets API com sistema de cache inteligente (atualização a cada 60s).
* **📅 Visão Mensal & Gerencial:** Gráficos acumulados por mês e cálculo automático de médias mensais.
* **🔮 Previsão com IA:** Algoritmo de *Time Series* (Prophet) que projeta a produção para os próximos 15 dias, exibindo margem de erro e tendências.
* **🌗 Multi-Tema:** Sistema de troca de temas (Claro/Escuro) com injeção de CSS personalizado para garantir acessibilidade e conforto visual.
* **🏭 Análise de Turnos:** Comparativo de eficiência entre Turno Dia vs. Turno Noite.
* **🛠️ Automação Desktop:** Scripts `.bat` personalizados para instalação de atalhos e inicialização automática do servidor local, simulando uma experiência de aplicativo nativo.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** [Python 3.13](https://www.python.org/)
* **Frontend/Framework:** [Streamlit](https://streamlit.io/)
* **Visualização de Dados:** [Plotly Express & Graph Objects](https://plotly.com/python/)
* **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
* **Machine Learning:** [Facebook Prophet](https://facebook.github.io/prophet/)
* **Conexão:** [Google Sheets API](https://developers.google.com/sheets/api) via `gspread`

---

## 🚀 Como Executar Localmente

### Pré-requisitos
* Python 3.10 ou superior.
* Arquivo `credentials.json` (Chave de Serviço do Google Cloud) na raiz do projeto.

### Instalação

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/zSevens7/dashboard-producao-emulsao.git](https://github.com/zSevens7/dashboard-producao-emulsao.git)
   cd dashboard-producao-emulsao
