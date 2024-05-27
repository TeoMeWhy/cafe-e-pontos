from nicegui import APIRouter, ui

from sqlalchemy import select

from models.product import Product
from models.transaction import Transaction, TransactionProduct
from models.customer import Customer

from utils import db, validate

session = db.new_session()
cadastro = APIRouter()

@cadastro.page("/cadastro_transacao")
def create_transaction(document_value=''):
    ui.markdown("# Crie uma compra")

    products = session.execute(select(Product.id, Product.name)).all()
    descriptions = [f'{i[0]:02} - {i[-1]}' for i in products]

    document_id = (ui.input(label="CPF",
                            placeholder="entre com o cpf",
                            validation={
                                'Entre com 11 valores para cpf': lambda value: len(value) == 14,
                                'Entre com um usuário existente': lambda value: validate.validate_customer_exists(value, session),
                                },
                            value=document_value)
                        .props('mask="###.###.###-##"'))
    
    with ui.row():
        description = ui.select(label="Produto", options=descriptions, with_input=True)
        quantity = ui.number(label="Quantidade", min=1, max=20, value=1)


    def prepare_transaction():
        product_id = (description.value.split(" - ")[0]
                                       .lstrip("0")
                                       .rstrip(" "))
        
        product = (session.scalar(select(Product).where(Product.id==product_id)))

        total_points = product.points * quantity.value
        total_value = product.value * quantity.value

        transaction = Transaction(
            customer_id=document_id.value,
            points=total_points,
            value=total_value)

        transaction_product = TransactionProduct(
            transaction_id=transaction.id,
            product_id=product.id,
            quantity=quantity.value)
        
        customer = (session.scalar(select(Customer).where(Customer.document==document_id.value)))

        return customer, product, transaction, transaction_product

    async def execute_commit():
        
        customer, product, transaction, transaction_product = prepare_transaction()
        
        if (-1 * transaction.points) > customer.points:
            ui.notification("O cliente não tem pontos suficientes.", color='red')
            return
        
        customer.points += transaction.points

        with ui.dialog() as dialog, ui.card():
            ui.markdown('###Confira os dados do cliente e confirme a execução.')

            with ui.grid(columns=2):

                ui.markdown(f'**Nome**: {customer.name} {customer.lastname}')
                ui.markdown(f'**Compra**: {transaction_product.quantity:.0f}x {product.name}')
                ui.markdown(f'**Valor**: R${transaction.value:.2f}')
                ui.markdown(f'**Pontos**: {transaction.points:.0f}')
        
            with ui.grid(columns=2):
                ui.button('Confirmar', on_click=lambda: dialog.submit(True), color='green')
                ui.button('Cancelar', on_click=lambda: dialog.submit(False), color='red')
        
        result = await dialog
        if result:
            try:
                session.add(transaction)
                session.add(transaction_product)
                session.commit()
                ui.notification("Compra concluida!", color='green')
            
            except Exception as err:
                session.rollback()
                print(err)
                ui.notification("Não foi possível realizar a compra", color='red')

    with ui.row():
        ui.button("Executar", on_click=execute_commit, color='green')
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))