from sqlalchemy.orm import Session

from models.models import Produto


def insert_produto(db: Session, produto: Produto):
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def get_produtos(db: Session):
    return [i.nome for i in db.query(Produto).all()]


def get_produto_by_name(db: Session, nome: str):
    return db.query(Produto).filter(Produto.nome == nome).first()


def delete_produto_by_name(db: Session, nome: str):
    produto = get_produto_by_name(db, nome)
    if produto:
        db.delete(produto)
        db.commit()
        return True
    return False