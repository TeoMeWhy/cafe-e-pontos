import time

import streamlit as st
import sqlalchemy

import datetime

from models.models import Base
from models import produto, cliente, transacao

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




def cadastrar_cliente(cpf:str):

    cliente_instance = utils_collects.collect_cliente_data(cpf)

    if st.button("Cadastrar Cliente"):
        if cliente_instance.nome_completo == "":
            st.error("Por favor, preencha o nome completo.")

        else:
            cliente.insert_cliente(ENGINE_SESSION, cliente_instance)
            st.success("Cliente cadastrado com sucesso!")
            time.sleep(1)
            st.rerun()
     

def expander_cliente():

    with st.expander("Cliente", expanded=False):
        cpf = st.text_input("CPF do Cliente")
        if cpf:
            cliente_data = cliente.get_cliente_by_cpf(ENGINE_SESSION, cpf)
            if cliente_data:
                utils_show.show_cliente(cliente_data)

                col1, _, col2 = st.columns(3)
                with col1:
                    add_pontos = st.toggle("Adicionar Pontos")
                
                if add_pontos:
                    adicao_pontos(cpf)
                
                with col2:
                    if st.button("Excluir Cliente"):
                        if cliente.delete_cliente_by_cpf(ENGINE_SESSION, cpf):
                            st.success("Cliente excluído com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Erro ao excluir o cliente.")

            else:
                cadastrar_cliente(cpf)


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




def adicao_pontos(cpf_cliente):

    col1, *_ = st.columns(3)
    with col1:
        add_buttom = st.number_input("Adicionar Produtos", min_value=1, value=1)
        
    produtos = []
    for i in range(add_buttom):
        produtos.append(utils_collects.collect_product_i(ENGINE_SESSION,i=i))

    confirma_add = st.button("Confirmar Adição de Pontos")
    if confirma_add:

        cliente_instance = cliente.get_cliente_by_cpf(ENGINE_SESSION, cpf_cliente)

        try:
            valor_pontos = transacao.create_trasacao(ENGINE_SESSION, cliente_instance.id, produtos)

            cliente_instance.pontos += valor_pontos

            cliente.update_cliente(ENGINE_SESSION, cliente_instance)
            st.success("Pontos adicionados com sucesso!")
            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")


expander_cliente()
expander_produto()
