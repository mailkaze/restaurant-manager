import json

class Producto():
    def __init__(self, id_producto, nombre, descripcion, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    def actualizar_stock(self, cant):
        '''El parámetro será un número positivo
        para sumar stock o un número negativo
        para restar stock.'''
        self.stock += cant
        #Es posible que haga falta escribir el archivo desde aquí.

class Comanda():
    def __init__(self, id_comanda, fecha, hora, num_mesa, dict_pedido, notas, cobrado, estado):
        '''dict_pedido es un diccionario donde las keys son
        id_productos y los valores son las cantidades de los
        productos pedidos. Estado solo puede tener estos valores:
        PENDIENTE, ACEPTADO, RECHAZADO, LISTO, COBRADO.'''
        self.id_comanda = id_comanda
        self.fecha = fecha
        self.hora = hora
        self.num_mesa = num_mesa
        self.dict_pedido = dict_pedido
        self.notas = notas
        self.cobrado = cobrado
        self.estado = estado

    def hallar_total(self):
        ruta = 'menu.json'
        total = 0
        with open(ruta, 'r') as f:
            menu = json.load(f)

        for id_producto, cantidad in self.dict_pedido.items():
            for producto in menu:
                if producto['id_producto'] == int(id_producto):
                    total += (producto['precio'] * cantidad)
                    break
        return round(total, 1)  

    def guardar(self):
        ruta = 'comandas.json'
        with open(ruta, 'r') as f:
            comandas = json.load(f)
            #asignamos al objeto comanda el id que le toca en la lista
        if self.id_comanda == 0:
            #es una comanda nueva, le asignamos el siguiente ID que toca y la añadimos al final de la lista
            self.id_comanda = len(comandas)
            #creamos el diccionario que se convertirá en json
            dict_comanda = {
                "id_comanda": self.id_comanda,
                "fecha": self.fecha,
                "hora": self.hora,
                "num_mesa": self.num_mesa,
                "dict_pedido": self.dict_pedido,
                "notas": self.notas,
                "cobrado": self.cobrado,
                "estado": self.estado
            }
            #añadimos la comanda convertida en json a la lista existente y sobreescribimos el archivo completo
            comandas.append(dict_comanda)
        else:
            #la comanda ya existe en el archivo y estamos editándola. Buscamos la coincidencia y actualizamos los valores
            for comanda in comandas:
                if comanda['id_comanda'] == self.id_comanda:
                    #actualizamos los 3 datos que podrían haber sido editados.
                    comanda['num_mesa'] = self.num_mesa
                    comanda['dict_pedido'] = self.dict_pedido
                    comanda['notas'] = self.notas
                    print('La comanda fue actualizada.')
                    break

        with open(ruta, 'w') as f:
            json.dump(comandas, f, indent=4)