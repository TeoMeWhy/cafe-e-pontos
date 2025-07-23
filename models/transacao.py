import datetime

from sqlalchemy.orm import Session

from models.models import Transacao, ProdutoTransacao

def insert_transacao(db: Session, transacao: Transacao):
    db.add(transacao)
    db.commit()
    db.refresh(transacao)
    return transacao

def create_trasacao(db: Session, cliente_id: str, produtos: list):

    valor_moeda_cento = sum([p.preco_venda * q for p,q in produtos])
    valor_moeda_cento_final = valor_moeda_cento
    valor_pontos = sum([p.pontos_compra * q for p,q in produtos])

    transacao = Transacao(
        cliente_id=cliente_id,
        data=datetime.datetime.now(),
        valor_moeda_cento=valor_moeda_cento,
        valor_moeda_cento_final=valor_moeda_cento_final,
        valor_pontos=valor_pontos
    )
    db.add(transacao)
    db.flush()

    produto_transacoes = []
    for produto, qtde in produtos:
        produto_transacoes.append(ProdutoTransacao(
                transacao=transacao,
                produto=produto,
                quantidade=qtde)
                )
    db.add_all(produto_transacoes)

    db.commit()

    return valor_pontos