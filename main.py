# pylint: disable=E1101,E1136
# type: ignore
import json
import streamlit as st
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from streamlit_calendar import calendar

custom_css = """
.fc-event-past { opacity: 0.8; }
.fc-event-time { font-style: italic; }
.fc-event-title { font-weight: 700; }
.fc-toolbar-title { font-size: 2rem; }
"""

load_dotenv()
tarefas_file = "tarefas.json"
meetings_file = "meetings.json"

def carregar_json(file_path, default):
    try:
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    except FileNotFoundError:
        return default

def salvar_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# Carregar ficheiros
tarefas = carregar_json(tarefas_file, {"tarefas": []})
meetings = carregar_json(meetings_file, {"Reunioes": []})
lista_prio = ["Baixa", "Média", "Alta"]

tab1, tab2 = st.tabs(["Tarefas", "Reunioes"])

with tab1:
    st.header("Tarefas")

    # Input de nova tarefa
    nova_tarefa = st.text_input("Nova tarefa")
    prio_tarefa = st.selectbox("Prioridade: ", lista_prio)
    if st.button("Adicionar", key="add_tarefa") and nova_tarefa.strip():
        tarefas["tarefas"].append({"tarefa": nova_tarefa, "completa": False, "Prioridade": prio_tarefa})
        salvar_json(tarefas_file, tarefas)
        st.rerun()

    # Preparar contagens
    contagens = {p: {"total": 0, "completas": 0} for p in lista_prio}
    for t in tarefas["tarefas"]:
        p = t["Prioridade"]
        contagens[p]["total"] += 1
        if t["completa"]:
            contagens[p]["completas"] += 1
    num_tarefas = sum(c["total"] for c in contagens.values())
    num_tarefas_completas = sum(c["completas"] for c in contagens.values())

    # Exibir tarefas
    for i, t in enumerate(tarefas["tarefas"]):
        cor = {"Alta": "#C41E3A", "Média": "#FF5533", "Baixa": "#008000"}.get(t["Prioridade"], "#808080")
        col1, col2, col3 = st.columns([5, 2, 2])
        with col1:
            st.markdown(f"""<div style="background-color: {cor}; padding: 8px; border-radius: 6px; color: white;">
                {t['tarefa']}
                </div>""", unsafe_allow_html=True)
        with col2:
            if not t["completa"]:
                if st.button("Completar", key=f"c{i}"):
                    t["completa"] = True
                    salvar_json(tarefas_file, tarefas)
                    st.rerun()
            else:
                st.markdown("Completado: ✅")
        with col3:
            if st.button("Remover", key=f"r{i}"):
                tarefas["tarefas"].pop(i)
                salvar_json(tarefas_file, tarefas)
                st.rerun()

    # Sidebar com resumo
    with st.sidebar:
        st.write(f"Tarefas completadas: {num_tarefas_completas} em {num_tarefas}")
        for p in lista_prio:
            st.write(f"Tarefas {p} completadas: {contagens[p]['completas']} em {contagens[p]['total']}")

with tab2:
    st.header("Reuniões")
    meeting_info = st.text_input("Descrição da reunião")
    data_meeting = st.date_input("Data da reunião")
    data_atual = datetime.today().date()

    if data_atual > data_meeting:
        st.error('Data da reunião tem de ser superior à data de hoje.')

    if st.button("Adicionar", key="add_meeting") and meeting_info.strip() and data_meeting >= data_atual:
        meetings["Reunioes"].append({"reuniao": meeting_info, "completa": False, "data": data_meeting.isoformat()})

    # Filtra reuniões antigas antes de salvar
    meetings["Reunioes"] = [m for m in meetings["Reunioes"] if datetime.fromisoformat(m['data']).date() >= data_atual]
    salvar_json(meetings_file, meetings)

    # Gerar calendário
    calendar_events = [{"title": m["reuniao"], "date": m["data"]} for m in meetings["Reunioes"]]
    calendar(events=calendar_events, custom_css=custom_css)

    # Mostrar lista e remover
    for i, m in enumerate(meetings["Reunioes"]):
        st.markdown(f"{m['data']} - {m['reuniao']}")
        if st.button(f"Remover {m['reuniao']}", key=f"meeting_remove_{i}"):
            meetings['Reunioes'].pop(i)
            salvar_json(meetings_file, meetings)
            st.rerun()

