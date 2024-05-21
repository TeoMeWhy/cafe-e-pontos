from nicegui import APIRouter, ui

busca = APIRouter()


@busca.page('/cliente_busca')
def search_customer_page(error=None):
    ui.markdown('# Buscar Cliente')
    ui.markdown('Busca de cliente pelo documento')

    if error:
        ui.notify('Usuário não encontrado', color='red')

    document_id = ui.input(
        label='CPF',
        placeholder='entre com o cpf',
        validation={
            'Entre com 11 valores para cpf': lambda value: len(value) == 14
        },
    ).props('mask="###.###.###-##"')

    with ui.row():
        ui.button(
            'Buscar!',
            on_click=lambda: ui.navigate.to(f'/cliente/{document_id.value}'),
        )
        ui.button('Início', on_click=lambda: ui.navigate.to('/'))
