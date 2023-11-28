import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import locale


# Função para carregar dados da planilha "BASE"
@st.cache_data
def load_data_analise():
    plan2 = "BASE"
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
        options=base["Cidade"].unique(),
        default=base["Cidade"].unique()
    )
    return base.query("Cidade == @category")

# Função para exibir totais e gráfico de barras
def display_totals_and_graph(selection_query):
    #Define modelo brasileiro
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    # Calcular totais
    total_litros = locale.format_string('%.2f', round(selection_query["Peso"].sum(), 2), grouping=True)
    total_notas = locale.format_string('%.2f', pd.to_numeric(selection_query['Nota'], errors='coerce').count(), grouping=True)

    # Configurar layout em duas colunas
    first_col, second_col = st.columns(2)

    with first_col:
        st.markdown("### Total Litros")
        st.subheader(f'{total_litros}')

    with second_col:
        st.markdown("### Total Notas")
        st.subheader(f'{total_notas}')

    st.markdown("---")

    # Agrupar por cidade e criar gráfico de barras
    total_cidades = selection_query.groupby(by=["Cidade"]).agg({'Peso':'sum', 'Nota':'count'}).reset_index()

    grafico = px.bar(
        total_cidades,
        x="Cidade",
        y=["Peso", "Nota"],
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
    fig.update_yaxes(range=[90000, 220000])
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
