from rolepermissions.roles import AbstractUserRole

class Motorista(AbstractUserRole):
    available_permissions = {}

class Administrador(AbstractUserRole):
    available_permissions = {}
