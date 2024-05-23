from nicegui import app, ui

from routers.cliente.busca import busca as busca_cliente
from routers.cliente.cadastro import cadastro as cadastro_cliente
from routers.cliente.cliente import cliente as cliente_cliente

from routers.produto.cadastro import cadastro as cadastro_produto
from routers.produto.busca import busca as busca_produto
from routers.produto.produto import produto as produto_produto

from routers.transacao.cadastro import cadastro as transacao_cadastro

app.include_router(busca_cliente)
app.include_router(cadastro_cliente)
app.include_router(cliente_cliente)

app.include_router(cadastro_produto)
app.include_router(busca_produto)
app.include_router(produto_produto)

app.include_router(transacao_cadastro)

ui.markdown('# Boas vindas ao Café e Pontos')

ui.markdown('---')
ui.markdown('## Compras')
with ui.row():
    ui.button("Nova Compra", on_click=lambda: ui.navigate.to('/cadastro_transacao'))
    ui.button("Histórico de compras", on_click=lambda: ui.notification("Pontos resgatados"))

ui.markdown('---')
ui.markdown('## Clientes')
with ui.row():
    ui.button('Cadastrar', on_click=lambda: ui.navigate.to('/cadastro_cliente'))
    ui.button('Buscar', on_click=lambda: ui.navigate.to('/busca_cliente'))

ui.markdown('---')
ui.markdown('## Produtos')
with ui.row():
    ui.button('Cadastrar', on_click=lambda: ui.navigate.to('/cadastro_produto'))
    ui.button('Buscar', on_click=lambda: ui.navigate.to('/busca_produto'))

ui.run(port=8081)