from sqlalchemy.orm import Session
import sqlalchemy
from models.models import Cliente


def insert_cliente(db:Session, cliente: Cliente):
    db.add(cliente)
    db.commit()
    return cliente


def get_cliente_by_cpf(db: Session, cpf: str):
    return db.scalar(db.query(Cliente).filter(Cliente.cpf == cpf))


def get_all_clientes(db: Session):
    return db.query(Cliente).all()


def get_aniversariantes(db: Session):
    today = sqlalchemy.func.strftime("%m-%d", sqlalchemy.func.current_date())
    aniversariantes =  (db.query(Cliente)
                          .filter(sqlalchemy.func.strftime("%m-%d", Cliente.aniversario) == today)
                          .all())
    return aniversariantes


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
    return cliente
