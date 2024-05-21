from nicegui import ui, app
import datetime
from utils import db
import utils.models as models

from sqlalchemy import exc, select

@ui.page('/cliente_busca')
def search_customer_page(error=None):
    ui.markdown('# Buscar Cliente')
    ui.markdown("Busca de cliente pelo documento")

    if error:
        ui.notify("Usuário não encontrado", color='red')

    document_id = (ui.input(label="CPF",
                           placeholder="entre com o cpf",
                           validation={'Entre com 11 valores para cpf': lambda value: len(value) == 14}
                           )
                      .props('mask="###.###.###-##"'))
        
    with ui.row():
        ui.button("Buscar!", on_click=lambda: ui.navigate.to(f"/cliente/{document_id.value}"))
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))


@ui.page('/cliente/{document}')
def customer_page(document: str):

    ui.markdown("#Cliente")
    customer = session.scalar(select(models.Customer)
                              .where(models.Customer.document==document))
    if not customer:
        ui.navigate.to("/cliente_busca?error=true")

    else:
        ui.notify("Usuário encontrado", color='green')

    ui.markdown(f"##{customer.name} {customer.lastname}")

    with ui.row():

        name = ui.input(label='Nome',
                        placeholder='entre com o nome...',
                        on_change=lambda e: e.value,
                        value=customer.name)
        
        lastname = ui.input(label='Sobrenome',
                        placeholder='entre com o sobrenome...',
                        on_change=lambda e: e.value,
                        value=customer.lastname)
    
        with ui.input('Aniversário', value=customer.date.date()) as birthday:
            with birthday.add_slot('append'):
                ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date().bind_value(birthday)


    with ui.row():
        document_id = (ui.input(label="CPF",
                            placeholder="entre com o cpf",
                            validation={'Entre com 11 valores para cpf': lambda value: len(value) == 14},
                            value=customer.document
                            )
                        .props('mask="###.###.###-##"'))
        
        email = ui.input(label='Email',
                        placeholder='entre com o email...',
                        on_change=lambda e: e.value,
                        value=customer.email)


        phone1 = (ui.input(label='Telefone Cel. (WhatsApp)',
                        placeholder='entre com o número de telefone...',
                        on_change=lambda e: e.value,
                        validation={'Entre com 14 valores para telefone': lambda value: len(value) == 18},
                        value=customer.phone1,
                        )
                    .props('mask="+55(##)#.####.####"'))
        
        phone2 = (ui.input(label='Telefone Comercial',
                        placeholder='entre com o número de telefone...',
                        validation={'Entre com 14 valores para telefone': lambda value: len(value) == 18},
                        on_change=lambda e: e.value,
                        value=customer.phone2)
                    .props('mask="+55(##)#.####.####"'))
    
    instagram = ui.input(label='Instagram',
                         placeholder='entre com o @ do instagram...',
                         on_change=lambda e: e.value,
                         value=customer.instagram)
    
    points = ui.input(label='Pontos',
                         placeholder='entre com a quantidade de pontos...',
                         on_change=lambda e: e.value,
                         value=customer.points)

    with ui.row():
        ui.button("Resgatar pontos", on_click=lambda: ui.notification("Pontos resgatados"))
        ui.button("Compras", on_click=lambda: ui.notification("Página de compras ainda não foi implementada"))
        ui.button("Estatísticas", on_click=lambda: ui.notification("Página de estatísticas ainda não foi implementada"))

    with ui.dialog() as dialog, ui.card():
        ui.label('Tem certeza que quer excluir este cliente?')
        with ui.row():
            ui.button('Sim', on_click=lambda: dialog.submit('Sim'))
            ui.button('Não', on_click=lambda: dialog.submit('Não'))

    async def delete_customer():
        result = await dialog
        if result == "Sim":
            try:
                session.delete(customer)
                ui.notification("Voce excluiu o usuário com sucesso!")
                session.commit()
            except Exception as err:
                session.rollback()
                print(err)
                ui.notification("Não foi possível excluir o usuário", color='red')

    def update_customer():

        mandatory_values = [
            name.value,
            lastname.value,
            email.value,
            birthday.value,
            document_id.value
        ]

        if '' in mandatory_values:
            ui.notify("Entre com os dados necessários", color='red')
            return
    
        customer.name = name.value
        customer.lastname = lastname.value
        customer.date = birthday.value
        customer.document = document_id.value
        customer.email = email.value
        customer.phone1 = phone1.value
        customer.phone2 = phone2.value
        customer.instagram = instagram.value
        customer.points = points.value
        session.commit()
        ui.notification("Usuário Salvo com sucesso!", color='green')

    with ui.row():
        ui.button("Salvar", on_click=update_customer, color='green')
        ui.button("Excluir", on_click=delete_customer, color='red')
    
    with ui.row():
        ui.button("Voltar", on_click=lambda: ui.navigate.to('/cliente_busca'))
        ui.button("Início", on_click=lambda: ui.navigate.to('/'))


session = db.new_session()

ui.markdown('# Boas vindas ao Café e Pontos')

ui.markdown('---')
ui.markdown('## Clientes')
with ui.row():
    ui.button('Cadastrar', on_click=lambda: ui.navigate.to('/cliente_cadastro'))
    ui.button('Buscar', on_click=lambda: ui.navigate.to('/cliente_busca'))


ui.markdown('---')
ui.markdown('## Produtos')
with ui.row():
    # ui.button('Cadastrar', on_click=get_go)
    ui.button('Buscar', on_click=lambda: ui.notify('Buscando produto'))


# AQUI!!!
from routers.cadastro import cadastro
app.include_router(cadastro)

ui.run(port=8081)
