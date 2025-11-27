# ====== CLASES BASADAS EN LA BASE DE DATOS NIKE ======

class TipoCalzado:
    def __init__(self, id_tipo_calzado, tipo_calzado):
        self.id_tipo_calzado = id_tipo_calzado
        self.tipo_calzado = tipo_calzado


class Medida:
    def __init__(self, id_medida, medida):
        self.id_medida = id_medida
        self.medida = medida


class TipoLocal:
    def __init__(self, id_tipo_local, tipo_local):
        self.id_tipo_local = id_tipo_local
        self.tipo_local = tipo_local


class Ciudad:
    def __init__(self, id_ciudad, ciudad, estado, pais):
        self.id_ciudad = id_ciudad
        self.ciudad = ciudad
        self.estado = estado
        self.pais = pais


class Estilo:
    def __init__(self, id_estilo, estilo, id_tipo_calzado):
        self.id_estilo = id_estilo
        self.estilo = estilo
        self.id_tipo_calzado = id_tipo_calzado


class Local:
    def __init__(self, id_local, local, id_tipo_local, id_ciudad):
        self.id_local = id_local
        self.local = local
        self.id_tipo_local = id_tipo_local
        self.id_ciudad = id_ciudad


class Producto:
    def __init__(self, id_estilo, id_medida, precio_lista, costo_unitario):
        self.id_estilo = id_estilo
        self.id_medida = id_medida
        self.precio_lista = precio_lista
        self.costo_unitario = costo_unitario


class Ticket:
    def __init__(self, ticket, fecha_venta, id_local, venta_ticket):
        self.ticket = ticket
        self.fecha_venta = fecha_venta
        self.id_local = id_local
        self.venta_ticket = venta_ticket


class Item:
    def __init__(self, ticket, item, id_estilo, id_medida, cantidad, precio_venta,
                 venta_item, costo_venta, utilidad):
        self.ticket = ticket
        self.item = item
        self.id_estilo = id_estilo
        self.id_medida = id_medida
        self.cantidad = cantidad
        self.precio_venta = precio_venta
        self.venta_item = venta_item
        self.costo_venta = costo_venta
        self.utilidad = utilidad

class Inventario:
    def __init__(self, id_local, id_estilo, id_medida, stock):
        self.id_local = id_local
        self.id_estilo = id_estilo
        self.id_medida = id_medida
        self.stock = stock
