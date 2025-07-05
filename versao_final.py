import streamlit as st
import math

# --- CONFIGURACAO DA PAGINA ---
st.set_page_config(
    page_title="Simulador de Sonhos",
    page_icon="💰"
)

# --- TITULO E TEXTOS INICIAIS ---
st.title("💰 Simulador de Sonhos")
st.subheader("Compare e veja a diferença no seu futuro financeiro")
st.markdown("---")
st.markdown("##### 📊 Simulação – Preencha 2 dos 3 campos")
st.write("Nossa carteira tem um rendimento estimado de **1% ao mês**. Compare o resultado com a **poupança (0.5% a.m.)**.")
st.markdown("---")

# --- VARIAVEIS GLOBAIS ---
# Pra guardar o que o usuario digita
if 'aporte' not in st.session_state:
    st.session_state.aporte = ""
if 'tempo' not in st.session_state:
    st.session_state.tempo = ""
if 'vf' not in st.session_state:
    st.session_state.vf = ""
if 'unidade' not in st.session_state:
    st.session_state.unidade = "meses"

# --- FUNSÕES DE CALCULO E FORMATACAO ---
# [CORREÇÃO] Funções reintroduzidas para organizar a lógica
def calc_vf(aporte, meses, taxa):
    if meses <= 0: return aporte
    return aporte * (((1 + taxa)**meses - 1) / taxa)

def calc_aporte(vf, meses, taxa):
    if meses <= 0: return float('inf')
    return vf / (((1 + taxa)**meses - 1) / taxa)

def calc_tempo(aporte, vf, taxa):
    if vf <= aporte: return 1
    numerador = math.log((vf * taxa / aporte) + 1)
    denominador = math.log(1 + taxa)
    return math.ceil(numerador / denominador)

def formata_dinheiro(valor):
    if valor is None or math.isinf(valor): return ""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formata_tempo(total_meses):
    if total_meses is None or total_meses <= 0 or math.isinf(total_meses):
        return "um tempo indefinido"
    anos = int(total_meses // 12)
    meses = int(total_meses % 12)
    if anos > 0 and meses > 0: return f"{anos} {'ano' if anos == 1 else 'anos'} e {meses} {'mês' if meses == 1 else 'meses'}"
    if anos > 0: return f"{anos} {'ano' if anos == 1 else 'anos'}"
    return f"{meses} {'mês' if meses == 1 else 'meses'}"


# --- LOGICA PRINCIPAL DO PROGRAMA ---

# 1. Pega os valores q o usuario digitou
aporte_str = st.session_state.aporte
tempo_str = st.session_state.tempo
vf_str = st.session_state.vf
unidade = st.session_state.unidade

# 2. Tenta converter pra numero
try:
    aporte_num = float(aporte_str.replace('.', '').replace(',', '.'))
except:
    aporte_num = None

try:
    tempo_num = float(tempo_str.replace('.', '').replace(',', '.'))
except:
    tempo_num = None

try:
    vf_num = float(vf_str.replace('.', '').replace(',', '.'))
except:
    vf_num = None

# 3. ve quantos campos tao preenchidos
preenchidos = 0
if aporte_num is not None and aporte_num > 0:
    preenchidos += 1
if tempo_num is not None and tempo_num > 0:
    preenchidos += 1
if vf_num is not None and vf_num > 0:
    preenchidos += 1

# 4. arruma as variaveis pra mostrar na tela
# [CORREÇÃO] Usa a função de formatar para reexibir o que o usuário digitou
aporte_display = formata_dinheiro(aporte_num) if aporte_num else ""
tempo_display = tempo_str
vf_display = formata_dinheiro(vf_num) if vf_num else ""
unidade_display = unidade
msg = None
tipo_msg = "info"

# 5. Se tiver 2 campos preenchidos, calcula o terceiro
if preenchidos == 2:
    if unidade == "anos" and tempo_num is not None:
        meses_total = tempo_num * 12
    else:
        meses_total = tempo_num

    # se for pra calcular o valor final
    if vf_num is None:
        carteira_res = calc_vf(aporte_num, meses_total, 0.01)
        poupanca_res = calc_vf(aporte_num, meses_total, 0.005)
        diff = carteira_res - poupanca_res
        vf_display = formata_dinheiro(carteira_res)
        msg = (
            f"Para um aporte de **R\\$ {formata_dinheiro(aporte_num)}** por **{formata_tempo(meses_total)}**:\n\n"
            f"**Nossa Carteira (1%):** Você terá **R\\$ {formata_dinheiro(carteira_res)}**\n\n"
            f"**Poupança (0.5%):** Você teria **R\\$ {formata_dinheiro(poupanca_res)}**\n\n"
            f"**Diferença:** Você ganha **R\\$ {formata_dinheiro(diff)} a mais!**"
        )
        tipo_msg = "success"

    # se for pra calcular o aporte
    elif aporte_num is None:
        carteira_res = calc_aporte(vf_num, meses_total, 0.01)
        poupanca_res = calc_aporte(vf_num, meses_total, 0.005)
        diff = poupanca_res - carteira_res
        aporte_display = formata_dinheiro(carteira_res)
        msg = (
            f"Para alcançar **R\\$ {formata_dinheiro(vf_num)}** em **{formata_tempo(meses_total)}**:\n\n"
            f"**Nossa Carteira (1%):** Você precisa investir **R\\$ {formata_dinheiro(carteira_res)}** por mês.\n\n"
            f"**Poupança (0.5%):** Seria necessário investir **R\\$ {formata_dinheiro(poupanca_res)}** por mês.\n\n"
            f"**Diferença:** Você economiza **R\\$ {formata_dinheiro(diff)}** todo mês!"
        )
        tipo_msg = "success"

    # se for pra calcular o tempo
    elif tempo_num is None:
        meses_carteira = calc_tempo(aporte_num, vf_num, 0.01)
        meses_poupanca = calc_tempo(aporte_num, vf_num, 0.005)
        diferenca = meses_poupanca - meses_carteira

        if meses_carteira >= 12:
            tempo_display = f"{(meses_carteira / 12):.1f}".replace('.', ',')
            unidade_display = "anos"
        else:
            tempo_display = str(int(meses_carteira))
            unidade_display = "meses"

        msg = (
            f"Para alcançar **R\\$ {formata_dinheiro(vf_num)}** com aportes de **R\\$ {formata_dinheiro(aporte_num)}**:\n\n"
            f"**Nossa Carteira (1%):** Leva **{formata_tempo(meses_carteira)}**.\n\n"
            f"**Poupança (0.5%):** Levaria **{formata_tempo(meses_poupanca)}**.\n\n"
            f"**Diferença:** Você atinge seu objetivo **{formata_tempo(diferenca)} mais rápido!**"
        )
        tipo_msg = "success"
        
elif preenchidos < 2:
    msg = "Preencha 2 campos pra calcular o terceiro."
    tipo_msg = "info"
else: # se preencheu 3
    msg = "Opa, vc preencheu os 3 campos. Tem q apagar um pra funcionar."
    tipo_msg = "warning"


# --- PARTE Q DESENHA OS CAMPOS ---
st.text_input(
    "Quanto você pretende investir por mês? (R$)",
    value=aporte_display,
    key="aporte"
)

col1, col2 = st.columns([3, 1])
with col1:
    st.text_input(
        "Por quanto tempo?",
        value=tempo_display,
        key="tempo"
    )
with col2:
    st.radio(
        "Unidade de tempo",
        options=["meses", "anos"],
        index=0 if unidade_display == "meses" else 1,
        horizontal=True,
        label_visibility="collapsed",
        key="unidade"
    )

st.text_input(
    "Qual valor final você gostaria de alcançar? (R$)",
    value=vf_display,
    key="vf"
)


# --- MOSTRA AS MENSAGENS NO FIM ---
st.markdown("---")

if msg:
    if tipo_msg == "success":
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDB2d2NtbjJ0eXJzNnN0cW96cDV2eDBpY2VqZ250aWJmYjZzeG1qZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/LdOyjZ7io5Msw/giphy.gif", width=150)
        st.success(msg)
    elif tipo_msg == "info":
        st.info(msg)
    elif tipo_msg == "warning":
        st.warning(f"⚠️ {msg}")

st.markdown("---")
st.caption("Aviso Importante: Os valores aqui são só ilustrativos pra ajudar a entender e não são garantia de ganho. Pra achar o melhor investimento pra vc, fale com nossos consultores.")
