import streamlit as st
import pandas as pd 
import gdown
import plotly.express as px

st.set_page_config(page_title="Grupo 6 ", page_icon=":bar_chart:")

st.write("---")
st.subheader("Integrantes")
integrantes = ["Angelica Perez Poma", "Harriet Mamani Mamani", "Delsi Cueva Guerra", "Francklin Dueñas Lagua"]

col1, col2 = st.columns(2)

col1.write(integrantes[0])
col2.write(integrantes[1])
col1.write(integrantes[2])
col2.write(integrantes[3])

st.write("---")
st.title("Composicion de residuos solidos domiciliarios")
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("Objetivo")
        st.write(
            """
            Gestionar de manera integra y sostenible acerca de los residuos generados
            contribuyendo la proteccion del medio ambiente y mejora de la calidad de vida de la poblacion. 
            """
        )
    with right_column:
        imagen_url = ".\Ftreamlit\imagen.png"  
        st.image(imagen_url, use_column_width=True)

st.write("----")
st.write("*- A continuación se muestra la tabla general *")
st.subheader("Tabla General")
data = pd.read_csv(".\Ftreamlit\Dcompos.csv", sep=";", encoding="latin1")

data = data.set_index("N_SEC")
dfrepe = data.dropna(how='all')
st.dataframe(dfrepe)
st.info("[Dirreccion de la tabla](https://www.datosabiertos.gob.pe/dataset/composici%C3%B3n-de-residuos-s%C3%B3lidos-domiciliarios/resource/22240195-3dbf-4ea1-a2ef-ff4c9ed02801)")

opti= st.multiselect(
    "seleccionar", 
    options=dfrepe["DEPARTAMENTO"].unique()
)
nombre = dfrepe[dfrepe["DEPARTAMENTO"].isin(opti)]
st.dataframe(nombre)

# Agrupar por 'DEPARTAMENTO' y sumar 'POB_TOTAL'
depas = dfrepe.groupby('DEPARTAMENTO')['POB_TOTAL'].sum().reset_index()

total_population = depas['POB_TOTAL'].sum()

depas['porcentaje'] = (depas['POB_TOTAL'] / total_population) * 100

fig = px.bar(depas, x='DEPARTAMENTO', y='porcentaje', title='Porcentaje de Población por Departamento',
             labels={'DEPARTAMENTO': 'Departamento', 'porcentaje': 'Porcentaje de Población'})

# fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
# fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45)

st.plotly_chart(fig)
fig_pie = px.pie(depas, values='porcentaje', names='DEPARTAMENTO', title='Porcentaje de Población por Departamento')



# col1, col2 = st.columns(2)
# col1.plotly_chart(depas) barras y circular en uno mismo
# col2.plotly_chart(fig_pie)
st.subheader("Datos Agrupados por Departamento")
st.write("---")
col1, col2 = st.columns(2)

col1.dataframe(depas)

col2.plotly_chart(fig_pie)

st.write("---")
st.write("---")
elegidas = [
    "N_SEC", "REG_NAT", "DEPARTAMENTO", "QRESIDUOS_ALIMENTOS", "QRESIDUOS_PAPEL_MIXTO",
    "QRESIDUOS_VIDRIOS_OTROS", "QRESIDUOS_LATA", "QRESIDUOS_BOLSAS_PLASTICAS",
    "QRESIDUOS_PILAS", "QRESIDUOS_TECNOPOR", "QRESIDUOS_MEDICAMENTOS", "QRESIDUOS_ENVOLTURAS_SNAKCS_OTROS"
]

columnas_validas = []
for i in elegidas:
    if i in dfrepe.columns:
        columnas_validas.append(i)

nuevodata = dfrepe[columnas_validas]

st.dataframe(nuevodata)



for col in nuevodata.columns[2:]:
    fig1 = px.bar(nuevodata, x='DEPARTAMENTO', y=col, title=col)
    st.plotly_chart(fig1)