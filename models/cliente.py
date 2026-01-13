from sqlalchemy.orm import Session

from models.models import Cliente


def insert_cliente(db:Session, cliente: Cliente):
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def get_cliente_by_cpf(db: Session, cpf: str):
    return db.scalar(db.query(Cliente).filter(Cliente.cpf == cpf))


def get_all_clientes(db: Session):
    return db.query(Cliente).all()


def delete_cliente_by_cpf(db: Session, cpf: str):
    cliente = get_cliente_by_cpf(db, cpf)
    if cliente:
        db.delete(cliente)
        db.commit()
        return True
    return False


def update_cliente(db: Session, cliente: Cliente):
    db.merge(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente
