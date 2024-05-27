from nicegui import APIRouter, ui

from models.product import Product
from utils import db

from sqlalchemy import select

busca = APIRouter()

session = db.new_session()

@busca.page("/busca_produto")
def search_product_page(error=None):
    
    if error:
        ui.notify("Usuário não encontrado", color='red')

    ui.markdown('# Buscar Produto')

    products = session.scalars(select(Product)).all()
    descriptions = [f'{i.id:02} - {i.name}' for i in products]
    description = ui.select(descriptions, with_input=True)

    def search():

        produto_id = (description.value.split(" - ")[0]
                                       .lstrip("0")
                                       .rstrip(" "))
        
        ui.navigate.to(f"/produto/{produto_id}")

    with ui.row():
        ui.button("Buscar!", on_click=search, color='green')
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))

    columns = [
            {'name': 'id', 'label': 'Id', 'field': 'id'},
            {'name': 'name', 'label': 'Nome', 'field': 'name'},
            {'name': 'description', 'label': 'Descrição', 'field': 'description'},
            {'name': 'value', 'label': 'Valor', 'field': 'value'},
            {'name': 'points', 'label': 'Pontos', 'field': 'points'},
    ]
    rows = [
            {'id': i.id, 'name': i.name, 'description': i.description, 'value': i.value, 'points': i.points}
            for i in products[:10]
    ]
    
    table=ui.table(columns=columns, rows=rows, row_key='name')
