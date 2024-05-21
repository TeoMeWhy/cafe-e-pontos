from nicegui import app, ui

from routers.busca import busca

# AQUI!!!
from routers.cadastro import cadastro
from routers.cliente import cliente

app.include_router(cadastro)
app.include_router(busca)
app.include_router(cliente)


ui.markdown('# Boas vindas ao Café e Pontos')

ui.markdown('---')
ui.markdown('## Clientes')
with ui.row():
    ui.button(
        'Cadastrar', on_click=lambda: ui.navigate.to('/cliente_cadastro')
    )
    ui.button('Buscar', on_click=lambda: ui.navigate.to('/cliente_busca'))


ui.markdown('---')
ui.markdown('## Produtos')
with ui.row():
    ui.button('Buscar', on_click=lambda: ui.notify('Buscando produto'))

ui.run(port=8081)
