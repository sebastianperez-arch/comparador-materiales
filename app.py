import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Control Materiales",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Control de Materiales")

entrada = st.file_uploader(
    "Excel Entrada",
    type=["xlsx"]
)

evidencia = st.file_uploader(
    "Excel Evidencia",
    type=["xlsx"]
)

if entrada and evidencia:

    df1 = pd.read_excel(entrada)
    df2 = pd.read_excel(evidencia)

    placa1 = st.selectbox(
        "Placa Entrada",
        df1.columns
    )

    placa2 = st.selectbox(
        "Placa Evidencia",
        df2.columns
    )

    material1 = st.selectbox(
        "Material Entrada",
        df1.columns
    )

    material2 = st.selectbox(
        "Material Evidencia",
        df2.columns
    )

    if st.button("🔍 Comparar"):

        resultado = []

        for _, r in df1.iterrows():

            placa = str(
                r[placa1]
            ).strip().upper()

            material = str(
                r[material1]
            ).strip().upper()

            existe = (
                (
                    df2[
                        placa2
                    ]
                    .astype(str)
                    .str.upper()
                    ==
                    placa
                )
                &
                (
                    df2[
                        material2
                    ]
                    .astype(str)
                    .str.upper()
                    ==
                    material
                )
            ).any()

            estado = (
                "✅ Coincide"
                if existe
                else
                "❌ No coincide"
            )

            resultado.append([
                placa,
                material,
                estado
            ])

        final = pd.DataFrame(
            resultado,
            columns=[
                "Placa",
                "Material",
                "Resultado"
            ]
        )

        st.dataframe(
            final,
            use_container_width=True
        )

        final.to_excel(
            "resultado.xlsx",
            index=False
        )

        with open(
            "resultado.xlsx",
            "rb"
        ) as f:

            st.download_button(
                "⬇ Descargar",
                f,
                "resultado.xlsx"
            )