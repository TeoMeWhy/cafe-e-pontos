from nicegui import APIRouter, ui

from models.product import Product
from utils import db, validate

from sqlalchemy import exc

session = db.new_session()
cadastro = APIRouter()

@cadastro.page("/cadastro_produto")
def new_product_page():
    ui.markdown("#Cadastro Produto")

    name = ui.input(label="Nome",
                    placeholder="entre com o nome do produto...",
                    on_change=lambda e: e.value)

    description = ui.input(label="Descrição",
                           placeholder="entre com a descrição do produto...",
                           on_change=lambda e: e.value)

    value = ui.input(label="Valor(R$)",
                     placeholder="entre com o valor do produto...",
                     on_change=lambda e: e.value.replace(",", "."),
                     validation={
                         "Entre com valores numéricos": lambda value: validate.validate_type(value.replace(",", "."), float),
                         "Entre com valores positivos": lambda value: float(value.replace(",", "."))>0,
                         })

    points = ui.input(label="Pontos",
                     placeholder="entre com a quantidade de pontos do produto...",
                     on_change=lambda e: int(e.value),
                     validation={
                         "Entre com valores numéricos": lambda value: validate.validate_type(value, int),
                         })
    
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

        product = Product(
            name = name.value,
            description = description.value,
            value = value.value,
            points = points.value,
        )

        try:
            session.add(product)
            session.commit()
            ui.notification("Produto criado com sucesso!", color='green')

        except exc.IntegrityError as err:
            session.rollback()
            ui.notification("Erro encontrado", color='red')

    with ui.row():
        ui.button("Cadastrar!", on_click=register_product, color='green')
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))