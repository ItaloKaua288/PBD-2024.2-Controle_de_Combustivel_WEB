from django.core.exceptions import ValidationError

def username_validator(value:str):
    if value[0] == ' ' or value[len(value)-1] == ' ':
        raise ValidationError('Usuario não pode conter espaços no começo ou fim')
    if len_validator(min=4, max=50, value=value):
        return value
    raise ValidationError('Usuario deve conter de 4 a 50 caracteres')

def password_validator(value:str):
    if len_validator(min=4, max=12, value=value):
        return value
    raise ValidationError('Senha deve conter de 4 a 12 caracteres')

def len_validator(min, max, value):
    if len(value) < min or len(value) > max:
        return False
    return True