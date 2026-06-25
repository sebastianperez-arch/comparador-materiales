import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Control Materiales",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Control y Comparación de Materiales")
st.caption("Compara registros de entrada y evidencia automáticamente")

def limpiar(x):
    return (
        str(x)
        .strip()
        .upper()
    )

entrada = st.file_uploader(
    "📥 Subir Excel Entrada",
    type="xlsx"
)

evidencia = st.file_uploader(
    "📸 Subir Excel Evidencia",
    type="xlsx"
)

if entrada and evidencia:

    try:

        df1 = pd.read_excel(entrada)
        df2 = pd.read_excel(evidencia)

        st.success("Archivos cargados correctamente")

        col1, col2 = st.columns(2)

        with col1:

            placa1 = st.selectbox(
                "Placa Entrada",
                df1.columns
            )

            fecha1 = st.selectbox(
                "Fecha Entrada",
                df1.columns
            )

            material1 = st.selectbox(
                "Material Entrada",
                df1.columns
            )

        with col2:

            placa2 = st.selectbox(
                "Placa Evidencia",
                df2.columns
            )

            fecha2 = st.selectbox(
                "Fecha Evidencia",
                df2.columns
            )

            material2 = st.selectbox(
                "Material Evidencia",
                df2.columns
            )

        if st.button(
            "🔍 Comparar"
        ):

            base1 = df1.copy()
            base2 = df2.copy()

            base1["KEY"] = (
                base1[placa1].apply(limpiar)
                + "_"
                + base1[fecha1].apply(limpiar)
                + "_"
                + base1[material1].apply(limpiar)
            )

            base2["KEY"] = (
                base2[placa2].apply(limpiar)
                + "_"
                + base2[fecha2].apply(limpiar)
                + "_"
                + base2[material2].apply(limpiar)
            )

            resultado = []

            k1 = set(base1["KEY"])
            k2 = set(base2["KEY"])

            for x in sorted(k1 & k2):

                resultado.append([
                    x,
                    "Coincide"
                ])

            for x in sorted(k1 - k2):

                resultado.append([
                    x,
                    "Sin evidencia"
                ])

            for x in sorted(k2 - k1):

                resultado.append([
                    x,
                    "Sin ingreso"
                ])

            final = pd.DataFrame(
                resultado,
                columns=[
                    "Registro",
                    "Resultado"
                ]
            )

            st.divider()

            a,b,c = st.columns(3)

            a.metric(
                "Coincidencias",
                (final["Resultado"]=="Coincide").sum()
            )

            b.metric(
                "Sin evidencia",
                (final["Resultado"]=="Sin evidencia").sum()
            )

            c.metric(
                "Sin ingreso",
                (final["Resultado"]=="Sin ingreso").sum()
            )

            filtro = st.text_input(
                "Buscar"
            )

            if filtro:

                final = final[
                    final["Registro"]
                    .str.contains(
                        filtro,
                        case=False
                    )
                ]

            st.dataframe(
                final,
                use_container_width=True,
                height=600
            )

            excel = "Reporte_Control_Materiales.xlsx"

            with pd.ExcelWriter(
                excel,
                engine="openpyxl"
            ) as writer:

                final.to_excel(
                    writer,
                    index=False
                )

            with open(
                excel,
                "rb"
            ) as f:

                st.download_button(
                    "⬇ Descargar Reporte",
                    f,
                    excel
                )

    except Exception as e:

        st.error(
            f"Error: {e}"
        )

else:

    st.info(
        "Sube ambos archivos para iniciar"
    )