# pylint: disable=E1101,E1136
# type: ignore
import json
import streamlit as st
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from streamlit_calendar import calendar
from reunioes import *
from tarefas import * 

def main():
    st.title("Gestor de Tarefas")
    tab1, tab2 = st.tabs(["Tarefas", "Reunioes"])

    with tab1:
        st.header("Tarefas")
        tarefas_tab() 
    with tab2:
        st.header("Reuniões")
        reunioes_tab()



if __name__ == '__main__':
    main()
    
    
