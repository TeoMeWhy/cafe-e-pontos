import datetime
import streamlit as st

from sqlalchemy.orm import Session

from models import models, produto, cliente


def collect_cliente_data(c: models.Cliente = models.Cliente()) -> models.Cliente:
    
    cpf = st.text_input("CPF do Cliente:", value=c.cpf, disabled=c.cpf != "")
    min_date = datetime.datetime.now() - datetime.timedelta(days=365*100)
    max_date = datetime.datetime.now() - datetime.timedelta(days=365*18) + datetime.timedelta(days=1)

    nome_completo = st.text_input("Nome Completo", value=c.nome_completo)
    email = st.text_input("Email", value=c.email)
    aniversario = st.date_input("Aniversário",
                                value=c.aniversario,
                                format="DD/MM/YYYY",
                                min_value=min_date,
                                max_value=max_date,
                                help="Data de nascimento do cliente")
    telefone = st.text_input("Telefone", value=c.telefone)
    instagram = st.text_input("Instagram", value=c.instagram)

    cliente = models.Cliente(
        cpf=cpf,
        nome_completo=nome_completo,
        email=email,
        aniversario=aniversario,
        telefone=telefone,
        instagram=instagram
    )

    return cliente


def collect_produto_data(db:Session):

    nome = st.text_input("Nome do Produto")
    
    exists_prods = [i.lower() for i in produto.get_produtos(db)]
    if nome.lower() in exists_prods:
        st.warning("Já existe um produto com esse nome. Por favor, escolha outro nome.")

    
    descricao = st.text_input("Descrição", help="Descrição do produto")
    preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, format="%.2f", help="Preço pelo qual o produto será vendido")
    preco_custo = st.number_input("Preço do Custo (R$)", min_value=0.0, format="%.2f", help="Preço que o produto custou para ser adquirido/produzido")
    pontos_compra = st.number_input("Pontos de Compra", min_value=0, help="Quantidade de pontos que o cliente ganha ao comprar esse produto")
    pontos_resgate = st.number_input("Pontos de Resgate", min_value=0, help="Quantidade de pontos necessários para resgatar esse produto")

    new_produto = models.Produto(
        nome=nome,
        descricao=descricao,
        preco_venda=int(100*preco_venda) if preco_venda else None,
        preco_custo=int(100*preco_custo) if preco_custo else None,
        pontos_compra=int(pontos_compra) if pontos_compra else None,
        pontos_resgate=int(pontos_resgate) if pontos_resgate else None
    )

    return new_produto


def collect_produto_input(db:Session, key=None):
    all_products = produto.get_produtos(db)
            
    if len(all_products) == 0:
        st.warning("Nenhum produto cadastrado. Por favor, cadastre um produto.")
    
    else:
        produto_selecionado = st.selectbox(label="Busque pelo produto",
                                            options=all_products,
                                            help="Selecione um produto para visualizar ou editar",
                                            key=key)
        
        return produto.get_produto_by_name(db, produto_selecionado)


def collect_product_i(db:Session, product=None, i=0, tipo_transacao="compra"):

    with st.container(border=True):

        col1, col2, col3 = st.columns(3)
        with col1:
            if not product:
                produto = collect_produto_input(db, key=f"Adicao_produto_{i}_{tipo_transacao}")

        with col2:
            qtde = st.number_input("Quantidade", min_value=1, value=1, key=f"qtde_produto_{i}_{tipo_transacao}")

        with col3:
            st.markdown(f"######")
            st.markdown(f"   **Pontos**: {qtde*produto.pontos_compra if tipo_transacao == 'compra' else qtde*produto.pontos_resgate}")

        return produto, qtde
