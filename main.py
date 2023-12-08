import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import locale


# Função para carregar dados da planilha "BASE"
@st.cache_data
def load_data_analise():
    plan2 = "HABI"
    base = pd.read_excel("PAINEL DE CONTROLE - BBT V3.xlsx", sheet_name=plan2)
    return base

# Função para carregar dados da planilha "COMP"
@st.cache_data
def load_data():
    plan = "COMP"
    df = pd.read_excel("PAINEL DE CONTROLE - BBT V3.xlsx", sheet_name=plan)
    return df


# Função para filtrar dados com base na seleção do usuário
def filter_data(base):
    st.sidebar.header('Filtro por cidades: ')
    category = st.sidebar.multiselect(
        "Filtro por cidade:",
        options=base["Cidades"].unique(),
        default=base["Cidades"].unique()
    )
    return base.query("Cidades == @category")

# Função para exibir totais e gráfico de barras
def display_totals_and_graph(selection_query):
    #Define modelo brasileiro
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # Calcular totais
    total_litros = round(selection_query["Pesos"].sum(), 2)
    #total_notas = pd.to_numeric(selection_query['Notas'], errors='coerce')
    total_notas = (selection_query['Notas'])
   
    total_lp_habitante = (selection_query['LPHabitante'].sum())
    #litros_por_reg = total_litros/float(total_lp_habitante)
   
   
    # Configurar layout em duas colunas
    first_col, second_col, third_col = st.columns(3)

    with first_col:
        st.markdown("### Total Litros")
        st.subheader(f'{locale.format_string('%.2f', total_litros, grouping=True)}')

    with second_col:
        st.markdown("### Total Notas")
        st.subheader(f'{locale.format_string('%.0f',total_notas.sum(), grouping=True)}')

    with third_col:
        st.markdown("### Total Litros por Região")
        st.subheader(f'{locale.format_string('%.4f', total_lp_habitante, grouping=True)}')
    

    st.markdown("---")

    # Agrupar por cidade e criar gráfico de barras
    total_cidades = selection_query.groupby(by=["Cidades"]).agg({'Pesos':'sum', 'Notas':'sum'}).reset_index() 
    

    grafico = px.bar(
        total_cidades,
        x="Cidades",
        y=["Pesos", 'Notas'],
        title="Cidades - Peso Vs Notas",
        color_discrete_sequence=["green", "#f51717"],
        labels={'value': 'Peso-Nota', 'variable': 'Categoria'}
    )

    grafico.update_layout(plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), barmode='stack')
    
    st.plotly_chart(grafico)

    
# Função para exibir gráfico de linha mensal
def display_monthly_chart(df):
    # Definir a ordem desejada dos meses (do menor para o maior)
    ordem_dos_meses = [
        'set-22', 'out-22', 'nov-22', 'dez-22', 'jan-23', 'fev-23', 'mar-23',
        'abr-23', 'mai-23', 'jun-23', 'jul-23', 'ago-23', 'set-23', 'out-23', 'nov-23', 'dez-23'
    ]

    # Categorizar a coluna 'DATA' e criar gráfico de linha
    df['DATA'] = pd.Categorical(df['DATA'], categories=ordem_dos_meses, ordered=True)
    df = df.sort_values('DATA')
    fig = px.line(df, x="DATA", y="VOLUME_PESO", text='VOLUME_PESO', color_discrete_sequence=['green'], title='Volume Mensal - Peso')

    # Atualizar configurações do gráfico
    fig.update_yaxes(range=[0, 220000])
    fig.update_traces(texttemplate='%{text:.2s}', textposition='top center')

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)
    

# Função principal
def main():
    # Configurar a página do Streamlit
    st.set_page_config(layout="wide")
    st.header("INDICADORES - BBT", divider='green')

    # Carregar dados da planilha "BASE" e "COMP"
    base = load_data_analise()
    df = load_data()

    # Carregar imagem
    img = Image.open("BBT.png")
    st.image(img, caption='Big Boss Transportes')

    # Filtrar dados, exibir totais e gráficos
    selection_query = filter_data(base)
    display_totals_and_graph(selection_query)
    display_monthly_chart(df)

# Executar a função principal se o script for executado diretamente
if __name__ == "__main__":
    main()