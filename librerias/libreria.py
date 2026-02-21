import csv
import json
import logging
import os
import sys
import glob
from datetime import datetime
import pandas as pd

# Configuración del sistema de logs
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/ventas.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def cargar_configuracion():
    """Lee el archivo de configuración JSON."""
    try:
        with open('datos/config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: El archivo 'datos/config.json' no existe.")
        return {"password": "admin", "nombre_pizzeria": "Pizzería Default"}

def menu_principal():
    """Menú inicial para redirigir al cliente o al administrador."""
    config = cargar_configuracion()
    nombre_local = config.get('nombre_pizzeria', 'Pizzería')
    
    while True:
        print(f"\n=== Bienvenido a {nombre_local} ===")
        print("1. Realizar pedido")
        print("2. Panel de Administración")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            carrito = menu()
            if carrito:
                total = procesar_venta(carrito)
                registrar_log_venta(total)
                print(f"Venta completada: {total}€")
        elif opcion == '2':
            if verificar_admin(config.get('password')):
                panel_administracion()
        elif opcion == '-3':
            # Opción oculta solicitada
            pass
        elif opcion == '0':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida.")

def verificar_admin(password_correcta):
    """Verifica la contraseña con un máximo de 3 intentos."""
    intentos = 0
    while intentos < 3:
        pwd = input("Introduzca la contraseña de administración: ")
        if pwd == password_correcta:
            logging.info("Acceso autorizado al panel de administración.")
            print("\n-> Acceso concedido.")
            return True
        else:
            intentos += 1
            print(f"Contraseña incorrecta. Intentos restantes: {3 - intentos}")
    
    logging.error("Intentos de acceso fallidos al panel de administración.")
    print("\nDemasiados intentos fallidos. Cerrando el programa por seguridad.")
    sys.exit()

def panel_administracion():
    """Analiza los tickets json usando Pandas."""
    print("\n--- PANEL DE ADMINISTRACIÓN ---")
    archivos_tickets = glob.glob('datos/ticket_*.json')
    
    if not archivos_tickets:
        print("No hay tickets registrados aún para analizar.")
        return

    datos_tickets = []
    for archivo in archivos_tickets:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                ticket = json.load(f)
                datos_tickets.append({
                    'total': ticket.get('total', 0)
                })
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")

    # Análisis de datos con Pandas
    if datos_tickets:
        df = pd.DataFrame(datos_tickets)
        total_recaudado = df['total'].sum()
        media_gasto = df['total'].mean()

        print(f"Total de tickets procesados: {len(df)}")
        print(f"Total de dinero recaudado: {total_recaudado:.2f}€")
        print(f"Media de gasto por ticket: {media_gasto:.2f}€")
        print("-------------------------------")

def menu():
    """Muestra los productos y permite añadirlos al carrito."""
    productos_disponibles = []
    carrito = []
    
    # Comprobar si el archivo de productos existe para lanzar ERROR en el log
    if not os.path.exists('datos/productos.csv'):
        mensaje_err = "Error: El archivo 'datos/productos.csv' no existe."
        print(mensaje_err)
        logging.error(mensaje_err)
        return carrito

    try:
        with open('datos/productos.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            print("\n======= MENÚ =======")
            for fila in reader:
                print(f"{fila['id']} | {fila['nombre']} | Precio: {fila['precio']}€")
                productos_disponibles.append(fila)
        
        while True:
            opcion = input("\nIntroduzca el ID del producto que desea (-1 para terminar): ")
            if opcion == "-1":
                break
            
            encontrado = False
            for p in productos_disponibles:
                if p['id'] == opcion:
                    carrito.append(p)
                    print(f"-> Añadido: {p['nombre']}")
                    encontrado = True
                    break
            
            if not encontrado:
                print("ID no válido. Por favor, consulte el menú.")
                
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}") 
        
    return carrito

def procesar_venta(carrito):
    """Calcula importes y guarda el ticket JSON."""
    if not carrito:
        return 0
    
    precios = []
    for producto in carrito:
        valor_limpio = producto['precio'].replace(',', '.')
        precios.append(float(valor_limpio))
    
    subtotal = sum(precios)
    iva = subtotal * 0.10
    total_final = subtotal + iva

    ticket = {
        "subtotal": round(subtotal, 2),
        "iva": round(iva, 2),
        "total": round(total_final, 2),
        "productos": carrito
    }

    nombre = f"datos/ticket_{datetime.now().strftime('%H%M%S')}.json"
    with open(nombre, 'w') as f:
        json.dump(ticket, f, indent=4)
        
    return total_final

def registrar_log_venta(importe):
    """Genera un log de tipo INFO tras una venta exitosa."""
    mensaje = f"Venta realizada con éxito. Total: {importe}€" 
    logging.info(mensaje) 

def calcular_totales(lista_precios):
    """Calcula subtotal, IVA (10%) y total final."""
    if not lista_precios:
        return 0, 0, 0
    
    subtotal = sum(lista_precios)
    iva = subtotal * 0.10  
    total = subtotal + iva
    return round(subtotal, 2), round(iva, 2), round(total, 2)