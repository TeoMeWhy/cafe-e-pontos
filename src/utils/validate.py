from models.customer import Customer

from sqlalchemy import select

def validate_type(x, obj_type):
    try:
        x = obj_type(x)
        return True
    except ValueError as err:
        return False

def validate_customer_exists(document_id, session):
    customer = session.scalar(select(Customer).where(Customer.document==document_id))
    return customer != None