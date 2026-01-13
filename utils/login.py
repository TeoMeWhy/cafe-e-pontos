import streamlit as st

import os
import time

def login():

    st.markdown("### Login")

    if os.path.exists("passwords"):

        with open("passwords", "r") as f:
            passwords = f.readlines()

        password = st.text_input("Senha", type="password")

        if len(password) == 0:
            return False

        if password in passwords:
            st.success("Login realizado com sucesso!")
            time.sleep(1)
            return True

        else:
            st.error("Senha incorreta. Tente novamente.")
            return False

    else:
        st.text("Esse é seu primeiro acesso. Por favor, crie uma senha.")
        new_password = st.text_input("Crie uma senha", type="password")

        if st.button("Criar Senha"):
            if new_password:
                with open("passwords", "w") as f:
                    f.write(new_password)
                st.success("Senha criada com sucesso!")
                time.sleep(1)
                st.rerun()
                return False
            else:
                st.error("Por favor, preencha a senha.")