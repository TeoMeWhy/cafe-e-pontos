from nicegui import APIRouter, ui

from utils import db, models

from sqlalchemy import select

busca = APIRouter()

session = db.new_session()

@busca.page("/busca_produto")
def search_product_page(error=None):
    
    if error:
        ui.notify("Usuário não encontrado", color='red')

    ui.markdown('# Buscar Produto')

    products = session.execute(select(models.Product.id, models.Product.name)).all()
    descriptions = [f'{i[0]:02} - {i[-1]}' for i in products]
    description = ui.select(descriptions, with_input=True)

    def search():

        produto_id = (description.value.split(" - ")[0]
                                       .lstrip("0")
                                       .rstrip(" "))
        
        ui.navigate.to(f"/produto/{produto_id}")

    with ui.row():
        ui.button("Buscar!", on_click=search, color='green')
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))