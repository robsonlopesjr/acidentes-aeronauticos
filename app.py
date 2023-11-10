import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    """
    Carrega os dados de ocorrências aeronáuticas do CENIPA

    :return: DataFrame com colunas selecionadas.
    """
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    data = pd.read_csv('./dataset/ocorrencias_aviacao.csv', index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)
    data.data = data.data + " " + data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    return data


# carregar os dados
df = load_data()
labels = df.classificacao.unique().tolist()

# SIDEBAR
# Parâmetros e números de ocorrências
st.sidebar.header("Parâmetros")
info_sidebar = st.sidebar.empty()  # placeholder, para irformações filtradas que só serão carregadas depois

# Slider de seleção do ano
st.sidebar.subheader("Ano")
year_to_filter = st.sidebar.slider(label='Escolha o ano desejado', min_value=2008, max_value=2018, value=2017)

# Checkbox da Tabela
st.sidebar.subheader('Tabela')
tabela = st.sidebar.empty()  # placeholder que só vai ser carregado com o df_filtered

# Multiselect com os labels únicos dos tipos de classificação
label_to_filter = st.sidebar.multiselect(
    label='Escolha a classificação da ocorrência',
    options=labels,
    default=['INCIDENTE', 'ACIDENTE']
)

# Informações no rodapé da Slider
st.sidebar.markdown("""
A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes Aeronáuticos (CENIPA)***.
""")

# Somente aqui os dados filtrados por ano são atualizados em novo dataframe
condicao = (df.data.dt.year == year_to_filter) & (df.classificacao.isin(label_to_filter))
filtered_df = df[condicao]

# Aqui o placeholder vazio finalmente é atualizado com os dados do filtered_df
info_sidebar.info("{} ocorrências selecionadas.".format(filtered_df.shape[0]))


# MAIN
st.title("CENIPA - Acidentes Aeronáuticos")
st.markdown(f"""
Estão sendo exibidas as ocorrências classificadas como **{", ".join(label_to_filter)}**
para o ano de **{year_to_filter}**.
""")

# raw data (tabela) dependete do checkbox
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_df)

# mapa
st.subheader("Mapa de ocorrências")
st.map(filtered_df)
