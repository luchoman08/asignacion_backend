from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'crear_usuarios': True,
        'eliminar_usuarios': True,
        'editar_usuarios': True,
        'eliminar_aplicacion': True,
    }

class MonitorGeneralServidor(AbstractUserRole):
    available_permissions = {
        'ver_estadisticas_globales': True,
        
    }

class MonitorAplicacion(AbstractUserRole):
    available_permissions = {
        'ver_estadisticas_aplicacion': True,
        
    }
class Usuario(AbstractUserRole):
    available_permissions = {
        'crear_aplicacion': True,
        'eliminar_aplicacion': True,
        'generar_llave': True,
        'eliminar_llave': True,
        'ver_estadisticas_aplicacion': True,
        'personalizar_servicio': True,
        
    }