import json
import datetime
import restaurante

#PASOS: coprobar_pendientes -> aceptar_rechazar -> mostrar_aceptadas -> listo

def comprobar_pendientes(menu):
    comandas = restaurante.cargar_comandas()
    #buscamos comandas pendientes de hoy
    for comanda in comandas:
        ahora = datetime.datetime.now()
        hoy = '{}/{}/{}'.format(ahora.day, ahora.month, ahora.year)
        if comanda['estado'] == 'PENDIENTE' and comanda['fecha'] == hoy:
            comanda = restaurante.dict_a_obj(comanda, 'c')
            aceptar_rechazar(comanda, menu)
    #actualizamos la lista del menú porque al aceptar comandas se actualizaron los stocks
    menu = restaurante.cargar_menu()
    #mostramos en pantalla la lista de trabajo de cocina
    mostrar_aceptadas(menu)

def aceptar_rechazar(comanda, menu):
    print('NUEVA COMANDA PENDIENTE:')
    print('Mesa {}:'.format(comanda.num_mesa))
    #preparamos un diccionario de productos y cantidades que van alterar su stock
    productos = {}
    for id_producto, cantidad in comanda.dict_pedido.items():
        for prod in menu:
            if prod['id_producto'] == int(id_producto):
                #encontramos ese producto en el menú
                print('{} X {}, tenemos {}'.format(cantidad, prod['nombre'], prod['stock']))
                #cargamos los id_producto y cantidad a restar en un diccionario, 
                #si se acepta la comanda, sus stocks deben cambiar.
                productos[id_producto] = productos.get(id_producto, 0) + cantidad
                break
    print('Aclaraciones: {}'.format(comanda.notas))
    aceptar = input('Pulsa "A" para ACEPTAR esta comanda, o "R" para RECHAZAR: ').upper()
    if aceptar == 'A':
        #ACEPTADO: cambia el estado de la comanda
        comanda.estado = 'ACEPTADO'
        #resta el stock del producto en la lista menu
        for id_producto, cantidad in productos.items():
            for producto in menu:
                if producto['id_producto'] == int(id_producto):
                    producto['stock'] -= cantidad
                    #convertimos el diccionario producto en un objeto
                    producto = restaurante.dict_a_obj(producto, 'p')
                    #guardamos el producto con el stock actualizado en el archivo menu.json
                    producto.guardar()
                    break
    elif aceptar == 'R':
        comanda.estado =  'RECHAZADO'
    comanda.guardar()

def mostrar_aceptadas(menu):
    #llama a cargar_comandas para tener la lista actualizada
    comandas = restaurante.cargar_comandas()
    #muestra las comandas aceptadas de hoy
    print('COMANDAS EN PREPARACIÓN:')
    for comanda in comandas:
        ahora = datetime.datetime.now()
        hoy = '{}/{}/{}'.format(ahora.day, ahora.month, ahora.year)
        if comanda['estado'] == 'ACEPTADO' and comanda['fecha'] == hoy:
            comanda = restaurante.dict_a_obj(comanda, 'c')
            print('\n---------------------------')
            print('Mesa {}'.format(comanda.num_mesa))
            print('Hora: {}'.format(comanda.hora))
            for id_producto, cantidad in comanda.dict_pedido.items():
                for prod in menu:
                    if prod['id_producto'] == int(id_producto):
                        print('{} X {}'.format(cantidad, prod['nombre']))
            print('Aclaraciones: {}'.format(comanda.notas))
    print('\n---------------------------')
    num_mesa = input('Escribe el número de la mesa que tengas lista: ')
    listo(num_mesa)
    #llama a comprobar pendientes para reiniciar todo el proceso
    comprobar_pendientes(menu)
    #TODO aqui hay un tiempo de espera en el que debería llamarse periodicamente a comprobar_pendientes(menu) mientras no haya resuesta a listo.

def listo(num_mesa):
    #busca entre las comandas aceptadas de hoy el num_mesa y cambia su estado a LISTO
    comandas = restaurante.cargar_comandas()
    ahora = datetime.datetime.now()
    hoy = '{}/{}/{}'.format(ahora.day, ahora.month, ahora.year)
    for comanda in comandas:
        if comanda['num_mesa'] == num_mesa and comanda['estado'] == 'ACEPTADO' and comanda['fecha'] == hoy:
            #crea el objeto comanda
            comanda = restaurante.dict_a_obj(comanda, 'c')
            comanda.estado = 'LISTO'
            comanda.guardar()
            break
    comprobar_pendientes(menu)

menu = restaurante.cargar_menu()
comprobar_pendientes(menu)