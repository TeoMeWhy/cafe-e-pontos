from nicegui import APIRouter, ui

from sqlalchemy import select

from models.product import Product

from utils import db

session = db.new_session()
cadastro = APIRouter()

@cadastro.page("/cadastro_transacao")
def create_transaction(document_value=''):
    ui.markdown("# Crie uma compra")

    products = session.execute(select(Product.id, Product.name)).all()
    descriptions = [f'{i[0]:02} - {i[-1]}' for i in products]

    document_id = (ui.input(label="CPF",
                            placeholder="entre com o cpf",
                            validation={'Entre com 11 valores para cpf': lambda value: len(value) == 14},
                            value=document_value)
                        .props('mask="###.###.###-##"'))
    
    with ui.row():
        description = ui.select(label="Produto", options=descriptions, with_input=True)
        quantity = ui.number(label="Quantidade", min=1, max=20, value=1)

    def create_transaction():
        produto_id = (description.value.split(" - ")[0]
                                       .lstrip("0")
                                       .rstrip(" "))
        print(produto_id)
        ui.notification("Sucesso!", color='green')

    with ui.row():
        ui.button("Confirmar", on_click=create_transaction, color='green')
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))