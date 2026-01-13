import shutil
import os

import time

import streamlit as st
import sqlalchemy

from models.models import Base
from models import produto, cliente, transacao
from models.models import Cliente, Produto

from utils import show as utils_show
from utils import collects as utils_collects


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

    cpf = st.text_input("CPF do Cliente:")
    cliente_instance = utils_collects.collect_cliente_data(cpf)

    if st.button("Cadastrar Cliente"):
        if cliente_instance.nome_completo == "":
            st.error("Por favor, preencha o nome completo.")

        else:
            cliente.insert_cliente(ENGINE_SESSION, cliente_instance)
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
        cliente_instance = st.selectbox("Procure ou cadastre um cliente pelo CPF:", [novo_cadastro]+clientes_list, format_func=lambda c: f"{c.nome_completo} - {c.cpf}")
        
        if cliente_instance.nome_completo != "Novo Cadastro":
            utils_show.show_cliente(cliente_instance)

            col1, _, col2 = st.columns(3)
            with col1:
                add_pontos = st.toggle("Adicionar Pontos")
            
            if add_pontos:
                adicao_pontos(cliente_instance)
            
            with col2:
                if st.button("Excluir Cliente"):
                    if cliente.delete_cliente_by_cpf(ENGINE_SESSION, cliente_instance.cpf):
                        st.success("Cliente excluído com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Erro ao excluir o cliente.")

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


def adicao_pontos(c):

    col1, *_ = st.columns([1,3])
    with col1:
        add_buttom = st.number_input("Adicionar Produtos", min_value=1, value=1)
        
    produtos = []
    for i in range(add_buttom):
        produtos.append(utils_collects.collect_product_i(ENGINE_SESSION,i=i))


    _, col2 = st.columns([2,1])
    with col2:
        with st.container(border=True):
            total = sum([i[0].pontos_compra * i[1] for i in produtos])
            st.markdown(f"**Total**: {total}")

    confirma_add = st.button("Confirmar Adição de Pontos")
    if confirma_add:

        try:
            c = cliente.get_cliente_by_cpf(ENGINE_SESSION, c.cpf)
            valor_pontos = transacao.create_trasacao(ENGINE_SESSION, c.id, produtos)
            c.pontos += valor_pontos
            cliente.update_cliente(ENGINE_SESSION, c)
            st.success("Pontos adicionados com sucesso!")
            c = cliente.get_cliente_by_cpf(ENGINE_SESSION, c.cpf)
            time.sleep(1)
            st.rerun()
            adicao_pontos(c)

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

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

if not st.session_state.get("logged_in", False):
    st.session_state['logged_in'] = login()
    if st.session_state['logged_in']:
        st.rerun()

else:
    expander_cliente()
    expander_produto()
