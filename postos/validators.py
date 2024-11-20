from django.core.exceptions import ValidationError
from itertools import cycle

def cnpj_validator(value):
    value = value.replace('.', '').replace('/', '').replace('-', '')
    if len(value) != 14 or value in (c * 14 for c in "1234567890"):
        raise ValidationError('CNPJ inválido!')

    cnpj_r = value[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            raise ValidationError('CNPJ inválido!')

def preco_validator(value):
    try:
        value = float(value)
    except ValueError:
        raise ValidationError('Preço precisa ser um numero!')
    
    if value < 0:
        raise ValidationError('Preço deve ser maior que 0!')
    return float(value)