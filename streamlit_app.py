import streamlit as st

st.set_page_config(page_title="Assistente de Nódulos Pulmonares", layout="centered")

st.title("🫁 Assistente de Nódulos Pulmonares")

# Escolha do contexto
context = st.selectbox("Contexto do nódulo", ["Fleischner (Incidental)", "Lung-RADS (Triagem)"])

# Tipo de nódulo
nodule_type = st.selectbox("Tipo de nódulo", ["Sólido", "Sub-sólido (ground-glass/part-solid)"])

# Tamanho inicial
size_initial = st.number_input("Tamanho inicial (mm)", min_value=0.0, step=0.1)

# Tamanho no exame subsequente (opcional)
size_followup = st.number_input("Tamanho no exame subsequente (mm, opcional)", min_value=0.0, step=0.1)

# Risco do paciente (apenas Fleischner)
risk = "Baixo risco"
if context == "Fleischner (Incidental)":
    risk = st.selectbox("Risco do paciente", ["Baixo risco", "Alto risco"])

# Função de cálculo
def calcular_recomendacao():
    growth = size_followup - size_initial
    rec = ""

    if context.startswith("Fleischner"):
        if nodule_type == "Sólido":
            if size_initial < 6:
                rec = "Sem seguimento necessário." if risk=="Baixo risco" else "TC em 12 meses (opcional)."
            elif size_initial <= 8:
                rec = "TC em 6–12 meses; considerar outro em 18–24 meses."
            else:
                rec = "TC em 3 meses, PET-CT ou biópsia."
        else:
            if size_initial < 6:
                rec = "TC em 12 meses; se estável, seguir por 5 anos."
            else:
                rec = "TC em 3–6 meses; se persistir, seguir por 5 anos."
    else:  # Lung-RADS
        if nodule_type == "Sólido":
            if size_initial < 6:
                rec = "Categoria 2 – TC anual."
            elif size_initial < 8:
                rec = "Categoria 3 – TC em 6 meses."
            else:
                rec = "Categoria 4A – TC em 3 meses ou PET-CT."
        else:
            if size_initial < 6:
                rec = "Categoria 2 – TC anual."
            elif size_initial < 20:
                rec = "Categoria 3 – TC em 6 meses."
            else:
                rec = "Categoria 4B – PET-CT ou biópsia."

    if size_followup > 0:
        if growth >= 2:
            rec += " ⚠️ Crescimento detectado (≥ 2 mm). Manejo mais agressivo sugerido."
        elif growth <= -2:
            rec += " ✅ Redução significativa detectada."
        else:
            rec += " ➖ Nódulo estável em exames subsequentes."

    return rec

# Botão para calcular
if st.button("Calcular recomendação"):
    recommendation = calcular_recomendacao()
    st.success(recommendation)
