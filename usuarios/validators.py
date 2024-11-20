from django.core.exceptions import ValidationError

def username_validator(value:str):
    if value[0] == ' ' or value[len(value)-1] == ' ':
        raise ValidationError('Usuario não pode conter espaços no começo ou fim')
    if len_validator(min=4, max=50, value=value):
        return value
    raise ValidationError('Usuario deve conter de 4 a 50 caracteres')

# def cpf_validator(value):
#     cpf = [int(char) for char in value if char.isdigit()]

#     if len(cpf) != 11 or cpf == cpf[::-1]:
#         raise ValidationError('CPF inválido!')

#     for i in range(9, 11):
#         value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
#         digit = ((value * 10) % 11) % 10
#         if digit != cpf[i]:
#             raise ValidationError('CPF inválido!')
#     return value

def password_validator(value:str):
    if len_validator(min=4, max=12, value=value):
        return value
    raise ValidationError('Senha deve conter de 4 a 12 caracteres')

def len_validator(min, max, value):
    if len(value) < min or len(value) > max:
        return False
    return True