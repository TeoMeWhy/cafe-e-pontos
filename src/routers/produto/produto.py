from nicegui import APIRouter, ui

from models.product import Product
from utils import validate, db

from sqlalchemy import select, exc

session = db.new_session()
produto = APIRouter()

@ui.page("/produto/{produto_id}")
def product_page(produto_id: str):

    product = session.scalar(select(Product)
                             .where(Product.id==produto_id))

    if not product:
        ui.navigate.to("/produto_busca?error=true")
        return

    ui.markdown("#Produto")

    with ui.row():
        name = ui.input(label="Nome",
                        placeholder="entre com o nome do produto...",
                        on_change=lambda e: e.value,
                        value=product.name)

        description = ui.input(label="Descrição",
                            placeholder="entre com a descrição do produto...",
                            on_change=lambda e: e.value,
                            value=product.description)

    with ui.row():
        value = ui.input(label="Valor(R$)",
                        placeholder="entre com o valor do produto...",
                        on_change=lambda e: e.value.replace(",", "."),
                        validation={
                            "Entre com valores numéricos": lambda value: validate.validate_type(value.replace(",", "."), float),
                            "Entre com valores positivos": lambda value: float(value.replace(",", "."))>0,
                            },
                        value=product.value)

        points = ui.input(label="Pontos",
                        placeholder="entre com a quantidade de pontos do produto...",
                        on_change=lambda e: int(e.value),
                        validation={
                            "Entre com valores numéricos": lambda value: validate.validate_type(value, int),
                            },
                        value=product.points)
        
    def register_product():

        mandatory_columns=[
            name.value,
            description.value,
            value.value,
            points.value,
        ]

        if '' in mandatory_columns:
            ui.notification("Preencha todos os campos corretamente.", color='red')
            return
        
        product.name = name.value
        product.description = description.value
        product.value = value.value
        product.points = points.value

        try:
            session.commit()
            ui.notification("Produto salvo com sucesso!", color='green')

        except exc.IntegrityError as err:
            session.rollback()
            ui.notification("Erro encontrado", color='red')

    with ui.row():
        ui.button("Salvar!", on_click=register_product, color='green')
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))