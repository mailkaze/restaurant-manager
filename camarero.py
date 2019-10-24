import json
import datetime
import restaurante

def print_menu(menu):
    for producto in menu:
        print('{}: {} - Bs.{}, quedan {} uds.'.format(
            producto['id_producto'], producto['nombre'], 
            producto['precio'], producto['stock']))

def print_comanda(comanda, menu):
    print('Mesa: {}'.format(comanda.num_mesa))
    for id_producto, cantidad in comanda.dict_pedido.items():
        #por cada elemento en el diccionario creado, anotamos el id_producto y la cantidad
        for producto in menu:
            #buscamos el elemento del menú con ese id_producto, imprimimos la cantidad, el nombre y el precio
            if producto['id_producto'] == int(id_producto):
                precio = producto['precio'] * cantidad
                print('{} X {}: Bs.{}'.format(cantidad, producto['nombre'], precio))
                break

    print('Aclaraciones para cocina: {}'.format(comanda.notas))            
    #finalmente mostramos el total de esa comanda
    print(comanda.hallar_total())

def tomar_pedido(menu):
    print_menu(menu)
    pedido = input('Escribe los números de los elementos solicitados separados por comas, cada uno tantas veces como los pidan: ')
    pedido = pedido.split(',')
    dict_pedido = {}
    for num in pedido:
        #montamos un diccionario con los numeros del pedido y las veces que se repiten
        dict_pedido[num] = dict_pedido.get(num, pedido.count(num))
    return dict_pedido

def nueva_comanda(menu):
    num_mesa = input('Escribe el número de mesa: ')
    dict_pedido = tomar_pedido(menu)
    notas = input('¿Alguna aclaración para cocina? Si no hay nada, solo pusar Enter: ')
    ahora = datetime.datetime.now()
    fecha = '{}/{}/{}'.format(ahora.day, ahora.month, ahora.year)
    hora = '{}:{}'.format(ahora.hour, ahora.minute)
    estado = 'PENDIENTE'
    cobrado = 0
    #crea el objeto comanda
    comanda = restaurante.Comanda(
        0, fecha, hora, num_mesa, dict_pedido, notas, cobrado, estado
    )

    print('Esta es tu comanda:')
    print_comanda(comanda, menu)
    guardar = input('¿Enviar? Y/N: ').upper()
    if guardar == 'Y':
        #guarda la comanda en el archivo json
        comanda.guardar()
    else:
        nueva_comanda(menu)

def abrir_comanda(menu):
    id_comanda = input('Escribe el número de la comanda que quieres ver: ')
    comandas = restaurante.cargar_comandas()
    
    for elemento in comandas:
        if elemento['id_comanda'] == int(id_comanda):
            comanda = restaurante.dict_a_obj(elemento, 'c')
            break
    print_comanda(comanda, menu)
    editar = input('¿Quieres editar esta comanda? Y/N: ').upper()
    if editar == 'Y':
        editar_comanda(comanda, menu)
    else:
        volver = input('¿Quieres buscar otra comanda? Y/N: ').upper()
        if volver == 'Y':
            abrir_comanda(menu)

def editar_comanda(comanda, menu):
    string = '''\
    1- Número de Mesa
    2- Pedido
    3- Aclaraciones para cocina
    '''
    print(string)
    seleccion = int(input('Escribe el número de la opción que quieres editar: '))

    if seleccion == 1:
        comanda.num_mesa = input('Escribe el número de mesa: ')
    elif seleccion == 2:
        comanda.dict_pedido = tomar_pedido(menu)
    elif seleccion == 3:
        comanda.notas = input('Escribe las aclaraciones: ')
    
    comanda.guardar()

menu = restaurante.cargar_menu()
nueva_comanda(menu)
abrir_comanda(menu)