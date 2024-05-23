def validate_type(x, obj_type):
    try:
        x = obj_type(x)
        return True
    except ValueError as err:
        return False

