# pylint: disable=E1101,E1136
# type: ignore
import json
import streamlit as st
from jsonfiles import salvar_json, carregar_json


def tarefas_tab():
    tarefas_file = "tarefas.json"
    # Carregar ficheiros
    tarefas = carregar_json(tarefas_file, {"tarefas": []})
    lista_prio = ["Baixa", "Média", "Alta"]
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
