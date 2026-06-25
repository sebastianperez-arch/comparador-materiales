import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Control Materiales",
    page_icon="🚛",
    layout="wide"
)

st.markdown("""
<style>

.main{
background:
linear-gradient(
135deg,
#071426,
#112244,
#1d4f91
);
}

.block-container{
padding-top:2rem;
}

div[data-testid="stMetric"]{
background:white;
padding:20px;
border-radius:20px;
box-shadow:0 10px 30px rgba(0,0,0,.15);
}

[data-testid="stDataFrame"]{
background:white;
border-radius:20px;
padding:10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🚛 Control Inteligente de Materiales")
st.caption(
"Compara registros de entrada y evidencia automáticamente"
)

def limpiar(x):
    return str(x).strip().upper()

col1,col2=st.columns(2)

with col1:

    entrada=st.file_uploader(
        "📥 Excel Entrada",
        type=["xlsx"]
    )

with col2:

    evidencia=st.file_uploader(
        "📸 Excel Evidencia",
        type=["xlsx"]
    )

if entrada and evidencia:

    df1=pd.read_excel(entrada)
    df2=pd.read_excel(evidencia)

    st.success(
        "Archivos cargados correctamente"
    )

    st.subheader(
        "Vista previa"
    )

    a,b=st.columns(2)

    with a:
        st.dataframe(
            df1.head()
        )

    with b:
        st.dataframe(
            df2.head()
        )

    st.subheader(
        "Selecciona columnas"
    )

    c1,c2,c3=st.columns(3)

    placa1=c1.selectbox(
        "Placa Entrada",
        df1.columns
    )

    material1=c2.selectbox(
        "Material Entrada",
        df1.columns
    )

    fecha1=c3.selectbox(
        "Fecha Entrada",
        df1.columns
    )

    d1,d2,d3=st.columns(3)

    placa2=d1.selectbox(
        "Placa Evidencia",
        df2.columns
    )

    material2=d2.selectbox(
        "Material Evidencia",
        df2.columns
    )

    fecha2=d3.selectbox(
        "Fecha Evidencia",
        df2.columns
    )

    if st.button(
        "🚀 Ejecutar Comparación"
    ):

        r=[]

        base2=[]

        for _,x in df2.iterrows():

            base2.append(

                (
                    limpiar(
                        x[placa2]
                    ),

                    limpiar(
                        x[material2]
                    ),

                    limpiar(
                        x[fecha2]
                    )

                )

            )

        for _,x in df1.iterrows():

            placa=limpiar(
                x[placa1]
            )

            material=limpiar(
                x[material1]
            )

            fecha=limpiar(
                x[fecha1]
            )

            key=(
                placa,
                material,
                fecha
            )

            if key in base2:

                estado="✅ Coincide"

            else:

                estado="❌ Revisar"

            r.append([

                placa,
                material,
                fecha,
                estado

            ])

        final=pd.DataFrame(

            r,

            columns=[

                "Placa",
                "Material",
                "Fecha",
                "Resultado"

            ]

        )

        st.divider()

        x,y=st.columns(2)

        x.metric(
            "Coincidencias",
            (
                final["Resultado"]
                ==
                "✅ Coincide"
            ).sum()
        )

        y.metric(
            "Revisar",
            (
                final["Resultado"]
                ==
                "❌ Revisar"
            ).sum()
        )

        st.dataframe(
            final,
            use_container_width=True
        )

        archivo="Reporte_Control.xlsx"

        final.to_excel(
            archivo,
            index=False
        )

        with open(
            archivo,
            "rb"
        ) as f:

            st.download_button(

                "⬇ Descargar Reporte",

                f,

                archivo

            )

else:

    st.info(
        "Sube ambos archivos para comenzar"
    )