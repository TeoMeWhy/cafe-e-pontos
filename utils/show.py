import streamlit as st


def show_cliente(cliente_data):
    st.success(f"Cliente encontrado!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**CPF**: {cliente_data.cpf}")
        st.markdown(f"**Aniversário**: {cliente_data.aniversario}")
        st.markdown(f"**Pontos**: {cliente_data.pontos}")
    
    with col2:
        st.markdown(f"**Nome Completo**: {cliente_data.nome_completo}")
        st.markdown(f"**Telefone**: {cliente_data.telefone}")
    
    with col3:
        st.markdown(f"**Email**: {cliente_data.email}")
        st.markdown(f"**Instagram**: {cliente_data.instagram}")


def show_produto(produto_data):
    if not produto_data:
        return

    preco_venda = produto_data.preco_venda/100 if produto_data.preco_venda is not None else 0
    preco_custo = produto_data.preco_custo/100 if produto_data.preco_custo is not None else 0


    col1, _, col3 = st.columns(3)

    with col1:
        st.markdown(f"**Nome**: {produto_data.nome}")
        st.markdown(f"**Preco Venda**: R${preco_venda:.2f}")
        st.markdown(f"**Preco Custo**: R${preco_custo:.2f}")
    
    with col3:
        st.markdown(f"**Descricao**: {produto_data.descricao}")
        st.markdown(f"**Pontos Compra**: {produto_data.pontos_compra}")
        st.markdown(f"**Pontos Resgate**: {produto_data.pontos_resgate}")