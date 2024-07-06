import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Grupo 6", page_icon=":bar_chart:")

st.sidebar.image("upch-logo.png", use_column_width=True)
st.sidebar.markdown("# Menu Principal")

menu = st.sidebar.radio(
    "_",
    ["Inicio", "Datos", "Comparacion"]
)
st.sidebar.image("medio.png", use_column_width=True)

elegidas = [
    "N_SEC", "REG_NAT", "DEPARTAMENTO", "QRESIDUOS_ALIMENTOS", "QRESIDUOS_PAPEL_MIXTO",
    "QRESIDUOS_VIDRIOS_OTROS", "QRESIDUOS_LATA", "QRESIDUOS_BOLSAS_PLASTICAS",
    "QRESIDUOS_PILAS", "QRESIDUOS_TECNOPOR", "QRESIDUOS_MEDICAMENTOS", "QRESIDUOS_ENVOLTURAS_SNAKCS_OTROS"
]
elegi=["QRESIDUOS_ALIMENTOS", "QRESIDUOS_PAPEL_MIXTO",
    "QRESIDUOS_VIDRIOS_OTROS", "QRESIDUOS_LATA", "QRESIDUOS_BOLSAS_PLASTICAS",
    "QRESIDUOS_PILAS", "QRESIDUOS_TECNOPOR", "QRESIDUOS_MEDICAMENTOS", "QRESIDUOS_ENVOLTURAS_SNAKCS_OTROS"
]

columnas_validas=[]
st.title("Composición de Residuos Sólidos Domiciliarios")
st.write("---")

data = pd.read_csv("Dcompos.csv", sep=";", encoding="latin1")
data = data.set_index("N_SEC")
dfrepe = data.dropna(how='all')

def mostrar_seccion(seccion):
    if seccion == "Inicio":
        st.subheader("Integrantes")
        integrantes = ["- Delsi Cueva Guerra", "- Harriet Mamani Mamani", "- Angelica Perez Poma", "- Francklin Dueñas Lagua"]
        col1, col2 = st.columns(2)
        col1.write(integrantes[0])
        col2.write(integrantes[1])
        col1.write(integrantes[2])
        col2.write(integrantes[3])
        st.write("---")
        with st.container():
            left_column, right_column = st.columns(2)
            with left_column:
                st.header("Objetivo")
                st.write(
                    """
                   Analizar la composición química y física de los residuos sólidos domiciliarios para 
                   identificar los principales componentes orgánicos e inorgánicos, 
                   con el fin de desarrollar estrategias efectivas de gestión y tratamiento
                    """
                )
            with right_column:
                imagen_url = 'imagen.png'  
                st.image(imagen_url, use_column_width=True)
        st.subheader("Descripcion")
        st.write("El manejo de residuos sólidos es un desafío crítico para cualquier nación en vías de desarrollo, y el Perú no es una excepción. En los últimos años, el país ha experimentado un crecimiento económico y demográfico significativo, lo cual ha llevado a un aumento proporcional en la generación de residuos sólidos. Estos residuos, que abarcan desde desechos orgánicos y plásticos hasta materiales de construcción y electrónicos, representan un problema complejo que afecta tanto a las zonas urbanas como rurales del Perú.")
        st.write("----")
        st.write("A continuación se muestra la tabla general:")
        st.subheader("Tabla General")
        st.dataframe(dfrepe)
        st.info("[Dirección de la tabla](https://www.datosabiertos.gob.pe/dataset/composici%C3%B3n-de-residuos-s%C3%B3lidos-domiciliarios/resource/22240195-3dbf-4ea1-a2ef-ff4c9ed02801)")
        st.write("---")
    elif seccion == "Datos":
        st.subheader("Datos Generales de los departamentos")
        opti = st.multiselect(
            "Seleccione un departamento", 
            options=dfrepe["DEPARTAMENTO"].unique()
        )
        nombre = dfrepe[dfrepe["DEPARTAMENTO"].isin(opti)]
        st.dataframe(nombre)

        depas = dfrepe.groupby('DEPARTAMENTO')['POB_TOTAL'].sum().reset_index()

        total_population = depas['POB_TOTAL'].sum()

        depas['porcentaje'] = (depas['POB_TOTAL'] / total_population) * 100

        fig = px.bar(depas, x='DEPARTAMENTO', y='porcentaje', title='Porcentaje de Población por Departamento',
                    labels={'DEPARTAMENTO': 'Departamento', 'porcentaje': 'Porcentaje de Población'})

        st.plotly_chart(fig)
        fig_pie = px.pie(depas, values='porcentaje', names='DEPARTAMENTO', title='Porcentaje de Población por Departamento')

        st.subheader("Datos Agrupados por Departamento")
        st.write("---")
        col1, col2 = st.columns(2)

        col1.dataframe(depas)

        col2.plotly_chart(fig_pie)

        st.write("---")

        
        for i in elegidas:
            if i in dfrepe.columns:
                columnas_validas.append(i)


        nuevodata = dfrepe[columnas_validas]

        st.dataframe(nuevodata)
        
        ims = ["img/r_alimentos.jpg", "img/r_papel.jpg", "img/r_vidrios.jpg", "img/r_lata.jpg", "img/r_bosas.jpg", "img/r_pilas.jpg",
               "img/r_tecno.jpg", "img/r_medic.jpg", "img/r_snack.jpg"]
        descripcion=[
                "Perú pierde o desperdicia 12.8 millones de toneladas de alimentos anualmente, y aunque ha avanzado en el marco legal con varias leyes desde 2016, aún carece de datos oficiales para evaluar la efectividad de estas políticas en la reducción de la inseguridad alimentaria y el desperdicio de alimentos.",
                "La industria papelera debe reducir su impacto ambiental y proteger la salud de sus trabajadores mediante el uso de materias primas recicladas, una buena gestión del agua y procesos de producción eficientes y menos contaminantes. Es esencial un correcto asesoramiento medioambiental para gestionar residuos peligrosos y no peligrosos, garantizando su separación, almacenamiento y tratamiento adecuado.",
                "En Perú, los residuos de vidrio representan una fuente significativa de contaminación debido a su lenta degradación y acumulación en vertederos y entornos naturales. Aunque el vidrio es 100% reciclable, solo una pequeña fracción se recicla adecuadamente. La falta de infraestructura y programas eficientes de recolección y reciclaje contribuye al problema, aumentando la contaminación y desperdiciando un recurso que podría reutilizarse indefinidamente. Abordar este problema requiere mejorar las políticas de reciclaje y aumentar la conciencia pública sobre la importancia del reciclaje del vidrio",
                "En Perú, los residuos de latas, principalmente de aluminio, son una fuente de contaminación significativa. Aunque el aluminio es altamente reciclable y su reciclaje ahorra energía y recursos, una gran cantidad de latas no se reciclan adecuadamente debido a la falta de infraestructura y programas de recolección efectivos. Mejorar las tasas de reciclaje de latas puede reducir la contaminación, ahorrar recursos naturales y disminuir el impacto ambiental. Es crucial implementar políticas de reciclaje más eficaces y aumentar la conciencia pública sobre la importancia del reciclaje de latas.",
                "En Perú, los residuos de bolsas plásticas representan un grave problema ambiental debido a su lenta degradación y acumulación en el medio ambiente, contaminando suelos, ríos y océanos. A pesar de los esfuerzos para reducir su uso, como la Ley del Plástico que busca limitar las bolsas plásticas de un solo uso, la implementación y cumplimiento aún son desafíos. Fomentar el uso de alternativas reutilizables y mejorar los programas de recolección y reciclaje son cruciales para reducir la contaminación por bolsas plásticas en el país.",
                "Los residuos de pilas son una fuente significativa de contaminación debido a los metales pesados y sustancias tóxicas que contienen, las cuales pueden filtrarse al suelo y al agua, afectando el medio ambiente y la salud humana. Aunque existen programas y normativas para su recolección y disposición adecuada, la infraestructura y la conciencia pública aún son insuficientes. Es fundamental mejorar la gestión de residuos de pilas mediante campañas de sensibilización, puntos de recolección accesibles y una mayor colaboración entre el gobierno, empresas y ciudadanos",
                "Los residuos de tecnopor representan un problema ambiental grave debido a su difícil degradación y su capacidad para fragmentarse en microplásticos. Estos residuos contaminan suelos, ríos y océanos, afectando la vida silvestre y los ecosistemas. Aunque hay iniciativas para reducir su uso, como la propuesta de ley para prohibir tecnopor en la distribución de alimentos, su implementación es un desafío. Es crucial promover alternativas biodegradables y mejorar las prácticas de recolección y reciclaje para mitigar el impacto del tecnopor en el medio ambiente.",
                "Los residuos de medicamentos son una preocupación ambiental y de salud pública debido a la presencia de compuestos farmacéuticos que pueden contaminar el agua y el suelo. La eliminación inadecuada de medicamentos vencidos o no utilizados, a través de la basura común o el desagüe, agrava este problema. Actualmente, la infraestructura para la recolección y disposición adecuada de estos residuos es limitada. Es crucial implementar y fortalecer programas de recolección específicos, así como campañas de concienciación para educar a la población sobre la correcta eliminación de medicamentos",
                "En Perú, los residuos de snacks y sus envolturas constituyen una fuente significativa de contaminación ambiental debido a su difícil degradación y acumulación en espacios públicos y naturales. Estos residuos, generalmente hechos de materiales plásticos y metalizados, no son fácilmente reciclables y contribuyen a la creciente crisis de residuos sólidos. La falta de infraestructura de reciclaje adecuada y la baja conciencia pública agravan el problema. Es esencial promover campañas de sensibilización, mejorar la recolección selectiva y fomentar el uso de materiales de embalaje más sostenibles para reducir el impacto ambiental de estos residuos."
            ]
        x=0
        for col in nuevodata.columns[2:]:
            st.write("---")
            st.title(col)
            with st.container():
                st.write("---")
                left_column, right_column = st.columns(2)
                with left_column:
                    fig1 = px.bar(nuevodata, x='DEPARTAMENTO', y=col, title=col)
                    st.plotly_chart(fig1)    
                with right_column:
                    df_pie = nuevodata.groupby('DEPARTAMENTO')[col].sum().reset_index()
                    fig_pie = px.pie(df_pie, names='DEPARTAMENTO', values=col, title=col)
                    st.plotly_chart(fig_pie)
            if x < len(ims):  
                with st.container():
                    left_column1, right_column1 = st.columns(2)
                    with left_column1:
                        st.image(ims[x], width=300)
                    with right_column1:
                        st.write(descripcion[x])
                x += 1
    elif seccion == "Comparacion":
        st.subheader("Comparacion entre Departamentos")
        op= st.selectbox(
            "Seleccione un departamento para comparar", 
            options=dfrepe["DEPARTAMENTO"].unique()
            )
        op1= st.selectbox(
            "Seleccione otro departamento para comparar", 
            options=dfrepe["DEPARTAMENTO"].unique()
            )
        if op == op1:
            st.warning("Seleccione dos departamentos diferentes para comparar.")

        else:
            selec=st.multiselect(
            "Seleccione las areas a comparar",
            elegi
            )
            if selec:
                for area in selec:
                    df_op = dfrepe[dfrepe["DEPARTAMENTO"] == op][area].sum()
                    df_op1 = dfrepe[dfrepe["DEPARTAMENTO"] == op1][area].sum()

                    pie_data = pd.DataFrame({
                        "Departamento": [op, op1],
                        "Valor": [df_op, df_op1]
                    })

                    fig = px.pie(pie_data, names="Departamento", values="Valor", title=f"Comparación de {area} entre {op} y {op1}")
                    st.plotly_chart(fig)
mostrar_seccion(menu)
