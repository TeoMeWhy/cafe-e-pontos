import datetime

from nicegui import APIRouter, ui
from sqlalchemy import exc

import utils.models as models
from utils import db

cadastro = APIRouter()
session = db.new_session()


@cadastro.page('/cliente_cadastro')
def new_customer_page():
    ui.markdown('# Cadastro Cliente')

    name = ui.input(
        label='Nome',
        placeholder='entre com o nome...',
        on_change=lambda e: e.value,
    )

    lastname = ui.input(
        label='Sobrenome',
        placeholder='entre com o sobrenome...',
        on_change=lambda e: e.value,
    )

    with ui.input('Aniversário') as birthday:
        with birthday.add_slot('append'):
            ui.icon('edit_calendar').on('click', lambda: menu.open()).classes(
                'cursor-pointer'
            )
        with ui.menu() as menu:
            ui.date().bind_value(birthday)

    email = ui.input(
        label='Email',
        placeholder='entre com o email...',
        on_change=lambda e: e.value,
    )

    document_id = ui.input(
        label='CPF',
        placeholder='entre com o cpf',
        validation={
            'Entre com 11 valores para cpf': lambda value: len(value) == 14
        },
    ).props('mask="###.###.###-##"')

    phone1 = ui.input(
        label='Telefone Cel. (WhatsApp)',
        placeholder='entre com o número de telefone...',
        on_change=lambda e: e.value,
        validation={
            'Entre com 14 valores para telefone': lambda value: len(value)
            == 18
        },
    ).props('mask="+55(##)#.####.####"')

    phone2 = ui.input(
        label='Telefone Comercial',
        placeholder='entre com o número de telefone...',
        validation={
            'Entre com 14 valores para telefone': lambda value: len(value)
            == 18
        },
        on_change=lambda e: e.value,
    ).props('mask="+55(##)#.####.####"')

    instagram = ui.input(
        label='Instagram',
        placeholder='entre com o @ do instagram...',
        on_change=lambda e: e.value,
    )

    def make_signup():
        mandatory_values = [
            name.value,
            lastname.value,
            email.value,
            birthday.value,
            document_id.value,
        ]

        if '' in mandatory_values:
            ui.notify('Entre com os dados necessários', color='red')
            return

        customer = models.Customer(
            name=name.value,
            lastname=lastname.value,
            email=email.value,
            date=datetime.datetime.strptime(birthday.value, '%Y-%m-%d'),
            document=document_id.value,
            phone1=phone1.value,
            phone2=phone2.value,
            instagram=instagram.value,
        )

        try:
            session.add(customer)
            session.commit()
            ui.notify('Cadastro realizado com sucesso!!', color='green')

        except exc.IntegrityError as err:
            print(err)
            session.rollback()
            ui.notify('Usuário já existente', color='red')

    with ui.row():
        ui.button('Cadastrar!', on_click=make_signup)
        ui.button('Início', on_click=lambda: ui.navigate.to('/'))
