import streamlit as st

import time

from utils import collects as utils_collects
from models import cliente, transacao
from models.models import Cliente
from sqlalchemy.orm import Session



def adicao_pontos(db: Session, c:Cliente):

    col1, *_ = st.columns([1,3])
    with col1:
        add_buttom = st.number_input("Adicionar Produtos", min_value=1, value=1)
        
    produtos = []
    for i in range(add_buttom):
        produtos.append(utils_collects.collect_product_i(db,i=i))


    _, col2 = st.columns([2,1])
    with col2:
        with st.container(border=True):
            total = sum([i[0].pontos_compra * i[1] for i in produtos])
            st.markdown(f"**Total**: {total}")

    if st.button("Confirmar Adição de Pontos"):

        try:
            c = cliente.get_cliente_by_cpf(db, c.cpf)
            valor_pontos = transacao.create_transacao_compra(db, c.id, produtos)
            c.pontos += valor_pontos
            cliente.update_cliente(db, c)
            st.success("Pontos adicionados com sucesso!")
            c = cliente.get_cliente_by_cpf(db, c.cpf)
            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")


def resgate_pontos(db: Session, c:Cliente):

    col1, *_ = st.columns([1,3])
    with col1:
        add_buttom = st.number_input("Adicionar Produtos", min_value=1, value=1)
        
    produtos = []
    for i in range(add_buttom):
        produtos.append(utils_collects.collect_product_i(db=db, product=None, i=i, tipo_transacao="resgate"))


    _, col2 = st.columns([2,1])
    with col2:
        with st.container(border=True):
            total = sum([i[0].pontos_resgate * i[1] for i in produtos])
            st.markdown(f"**Total**: {total}")

    if c.pontos < total:
        st.error("Pontos insuficientes para esse resgate.")

    if st.button("Confirmar Resgate de Pontos", disabled=(c.pontos < total)):

        try:
            c = cliente.get_cliente_by_cpf(db, c.cpf)
            valor_pontos = transacao.create_transacao_resgate(db, c.id, produtos)
            c.pontos += valor_pontos
            cliente.update_cliente(db, c)
            st.success("Pontos resgatados com sucesso!")
            c = cliente.get_cliente_by_cpf(db, c.cpf)
            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
