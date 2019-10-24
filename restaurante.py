import json

class Producto():
    def __init__(self, id_producto, nombre, descripcion, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    def guardar(self):
        menu = cargar_menu()
        if self.id_producto == 0:
            #es un producto nuevo, le asignamos el siguiente ID que toca y la añadimos al final de la lista
            self.id_producto = len(menu)
            #creamos el diccionario que se convertirá en json
            dict_producto = {
                "id_producto": self.id_producto,
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "precio": self.precio,
                "stock": self.stock
            }
            #añadimos el producto convertido en json a la lista existente y sobreescribimos el archivo completo
            menu.append(dict_producto)
        else:
            #el producto ya existe en el archivo y estamos editándolo. Buscamos la coincidencia y actualizamos los valores
            for producto in menu:
                if producto['id_producto'] == int(self.id_producto):
                    #actualizamos los 4 datos que podrían haber sido editados.
                    producto['nombre'] = self.nombre
                    producto['descripcion'] = self.descripcion
                    producto['precio'] = self.precio
                    producto['stock'] = self.stock
                    print('El producto fue actualizado.')
                    break
        ruta = 'menu.json'
        with open(ruta, 'w') as f:
            json.dump(menu, f, indent=4)

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
        comandas = cargar_comandas()
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
                if comanda['id_comanda'] == int(self.id_comanda):
                    #actualizamos los 5 datos que podrían haber sido editados.
                    comanda['num_mesa'] = self.num_mesa
                    comanda['dict_pedido'] = self.dict_pedido
                    comanda['notas'] = self.notas
                    comanda['estado'] = self.estado
                    comanda['cobrado'] = self.cobrado
                    print('La comanda fue actualizada.')
                    break
        ruta = 'comandas.json'
        with open(ruta, 'w') as f:
            json.dump(comandas, f, indent=4)

#funciones globales:
def cargar_menu():
    ruta = 'menu.json'
    with open(ruta, 'r') as f:
        menu = json.load(f)
    return menu

def cargar_comandas():
    ruta = 'comandas.json'
    with open(ruta, 'r') as f:
        comandas = json.load(f)
    return comandas

def dict_a_obj(diccionario, comanda_o_producto):
    '''El segundo parámetro debe ser "c"
    para objeto comanda o "p" para objeto producto'''
    #Crea un objeto de la clase Comanda o Producto a partir de un diccionario
    if comanda_o_producto == 'c':
        objeto = Comanda(
                    diccionario['id_comanda'], diccionario['fecha'], diccionario['hora'],
                    diccionario['num_mesa'], diccionario['dict_pedido'],
                    diccionario['notas'], diccionario['cobrado'], diccionario['estado']
                )
    elif comanda_o_producto == 'p':
        objeto =  Producto(
                    diccionario['id_producto'], diccionario['nombre'],
                    diccionario['descripcion'], diccionario['precio'], 
                    diccionario['stock']
                )
    return objeto