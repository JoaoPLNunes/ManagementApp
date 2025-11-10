import json
import streamlit as st

FICHEIRO = "/Users/tiagonunes/Documents/tarefas.json"

def carregar_tarefas():
    try:
        with open(FICHEIRO, "r") as f:
            return json.load(f)
    except:
        return {"tarefas": []}

def guardar_tarefas(tarefas):
    with open(FICHEIRO, "w") as f:
        json.dump(tarefas, f, indent=2)

st.title("Gerenciador de Tarefas")

tarefas = carregar_tarefas()

nova = st.text_input("Nova tarefa")
if st.button("Adicionar"):
    if nova.strip():
        tarefas["tarefas"].append({"tarefa": nova, "completa": False})
        guardar_tarefas(tarefas)
        st.rerun()

st.subheader("Tarefas")
for i, t in enumerate(tarefas["tarefas"]):
    col1, col2, col3 = st.columns([5,2,2])
    with col1:
        st.write(f"{t['tarefa']}")
    with col2:
        if not t["completa"]:
            if st.button("Completar", key=f"c{i}"):
                tarefas["tarefas"][i]["completa"] = True
                guardar_tarefas(tarefas)
                st.rerun()
        if t["completa"]:
            label = ("Completado: ✅")
            with col1:
                st.markdown(label)
    with col3:
        if st.button("Remover", key=f"r{i}"):
            tarefas["tarefas"].pop(i)
            guardar_tarefas(tarefas)
            st.rerun()