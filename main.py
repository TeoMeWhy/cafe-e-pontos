import time

import streamlit as st
import sqlalchemy

from models.models import Base
from models import produto, cliente, transacao
from models.models import Cliente, Produto

from utils import show as utils_show
from utils import collects as utils_collects
from utils import pontos

from utils.login import login

DATABASE_URL = "sqlite:///data/database.db"
engine = sqlalchemy.create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

ENGINE_SESSION = sqlalchemy.orm.Session(engine)

st.set_page_config(
    page_title="Café Pontos",
    page_icon=":coffee:"
)

st.title("Café e Pontos")


def cadastrar_cliente():

    c = utils_collects.collect_cliente_data()
    if st.button("Cadastrar Cliente"):
        
        if c.nome_completo == "":
            st.error("Por favor, preencha o nome completo.")

        else:
            cliente.insert_cliente(ENGINE_SESSION, c)
            st.success("Cliente cadastrado com sucesso!")
            time.sleep(1)
            st.rerun()


def cadastrar_produto():
    produto_instance = utils_collects.collect_produto_data(ENGINE_SESSION)
    if st.button("Confirmar"):
        if produto_instance.nome and produto_instance.descricao and produto_instance.pontos_compra:
            produto.insert_produto(ENGINE_SESSION, produto_instance)
            st.success("Produto cadastrado com sucesso!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")


def expander_cliente():
    clientes_list = cliente.get_all_clientes(ENGINE_SESSION)
    with st.expander("Cliente", expanded=False):

        novo_cadastro = Cliente(cpf="", nome_completo="Novo Cadastro")
        c = st.selectbox("Procure ou cadastre um cliente pelo CPF:", [novo_cadastro]+clientes_list, format_func=lambda c: f"{c.nome_completo} - {c.cpf}")
        
        if c.nome_completo != "Novo Cadastro":
            
            tab_info, tab_edit = st.tabs(["Informações", "Editar"])

            with tab_info:
                utils_show.show_cliente(c)

                col1, _, col3 = st.columns(3)

                if col1.toggle("Adicionar Pontos"):
                    pontos.adicao_pontos(ENGINE_SESSION, c)

                if col1.toggle("Resgatar Pontos"):
                    pontos.resgate_pontos(ENGINE_SESSION, c)

                if col3.button("Excluir Cliente"):
                    if cliente.delete_cliente_by_cpf(ENGINE_SESSION, c.cpf):
                        st.success("Cliente excluído com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Erro ao excluir o cliente.")

            with tab_edit:
                    c_new = utils_collects.collect_cliente_data(c)
                    c_new.id = cliente.get_cliente_by_cpf(ENGINE_SESSION, c_new.cpf).id
                    if st.button("Salvar"):
                        
                        if c_new.nome_completo == "":
                            st.error("Por favor, preencha o nome completo.")

                        else:
                            cliente.update_cliente(ENGINE_SESSION, c_new)
                            st.success("Cliente atualizado com sucesso!")
                            c = cliente.get_cliente_by_cpf(ENGINE_SESSION, c_new.cpf)
                            time.sleep(3)
                            st.rerun()

        else:
            cadastrar_cliente()


def expander_produto():

    with st.expander("Produto", expanded=False):

        busca, cadastro = st.tabs(["Buscar Produto", "Cadastrar Produto"])

        with busca:
            
            produto_atual = utils_collects.collect_produto_input(ENGINE_SESSION, "expander_produto")
            utils_show.show_produto(produto_atual)

            if st.button("Excluir Produto"):
                produto.delete_produto_by_name(ENGINE_SESSION, produto_atual.nome)
                st.success("Produto excluído com sucesso!")
                time.sleep(1)
                st.rerun()
                

        with cadastro:
            cadastrar_produto()


def expander_avisos():
    with st.expander("Avisos", expanded=False):
        aniversariantes = cliente.get_aniversariantes(ENGINE_SESSION)
        utils_show.show_aniversariantes(aniversariantes)



if not st.session_state.get("logged_in", False):
    st.session_state['logged_in'] = login()
    if st.session_state['logged_in']:
        st.rerun()

else:
    expander_cliente()
    expander_produto()
    expander_avisos()
