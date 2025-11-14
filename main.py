#type ignore
import json
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
FICHEIRO = os.getenv("FICHEIRO")
if not FICHEIRO:
    raise FileNotFoundError("Não foi encontrado ficheiro json")
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
lista_prio =["Baixa","Média","Alta"] 
nova = st.text_input("Nova tarefa")
prio = st.selectbox(label="Prioridade: ",options=lista_prio)
if st.button("Adicionar"):
    if nova.strip():
        tarefas["tarefas"].append({"tarefa": nova, "completa": False,"Prioridade": prio})  # pyright: ignore[reportUnknownMemberType]
        guardar_tarefas(tarefas)
        st.rerun()
num_tarefas = len(tarefas["tarefas"])
num_tarefas_completas = sum(1 for t in tarefas["tarefas"] if t["completa"])
for prioridade in lista_prio:
    num_tarefa_baixa = sum(1 for pt in tarefas["tarefas"] if pt["Prioridade"]=="Baixa")
    num_tarefa_media = sum(1 for pt in tarefas["tarefas"] if pt["Prioridade"]=="Média")
    num_tarefa_alta = sum(1 for pt in tarefas["tarefas"] if pt["Prioridade"]=="Alta")
    num_tarefa_alta_completa = sum(1 for pt in tarefas["tarefas"] if pt["Prioridade"]=="Alta" and pt["completa"] )
    num_tarefa_media_completa = sum(1 for pt in tarefas["tarefas"] if pt["Prioridade"]=="Média" and pt["completa"] )
    num_tarefa_baixa_completa = sum(1 for pt in tarefas["tarefas"] if pt["Prioridade"]=="Baixa" and pt["completa"] )
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
    with st.sidebar:
        st.write(f"Tarefas completadas: {num_tarefas_completas} em {num_tarefas}")
        st.write(f"Tarefas urgentes completadas: {num_tarefa_alta_completa} em {num_tarefa_alta}")
        st.write(f"Tarefas meio urgentes completadas: {num_tarefa_media_completa} em {num_tarefa_media}")
        st.write(f"Tarefas não urgentes completadas: {num_tarefa_baixa_completa} em {num_tarefa_baixa}")
