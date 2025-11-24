# pylint: disable=E1101,E1136
# type: ignore
import json
import streamlit as st
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from streamlit_calendar import calendar
from jsonfiles import salvar_json, carregar_json
def reunioes_tab():
    custom_css = """
    .fc-event-past { opacity: 0.8; }
    .fc-event-time { font-style: italic; }
    .fc-event-title { font-weight: 700; }
    .fc-toolbar-title { font-size: 2rem; }
    """
    meetings_file = "meetings.json"
    meetings = carregar_json(meetings_file, {"Reunioes": []})

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

