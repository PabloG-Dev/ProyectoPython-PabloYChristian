import csv
import json
import logging
import os
from datetime import datetime


def menu():
    
    productos_disponibles = []
    carrito = []
    
    try:
        # Leer archivo CSV con separador ;
        with open('datos/productos.csv', mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            print("\n======= MENÚ PIZZERÍA EL HORNO =======")
            for fila in reader:
                print(f"{fila['id']} | {fila['nombre']} | Precio: {fila['precio']}€")
                productos_disponibles.append(fila)
        
        # Bucle  
        while True:
            opcion = input("\nIntroduzca el ID del producto que desea (-1 para terminar): ")
            
            if opcion == "-1":
                break
            
            # Buscar producto por su ID 
            encontrado = False
            for p in productos_disponibles:
                if p['id'] == opcion:
                    carrito.append(p)
                    print(f"-> Añadido: {p['nombre']}")
                    encontrado = True
                    break
            
            if not encontrado:
                print("ID no válido. Por favor, consulte el menú.")
                
    except FileNotFoundError:
        print("Error: El archivo 'datos/productos.csv' no existe.") 
        
    return carrito

def procesar_venta(carrito):
    """Calcula importes y guarda el ticket JSON."""
    if not carrito:
        return 0
    
    # Limpiamos comas y convertimos a número
    precios = []
    for producto in carrito:
        valor_limpio = producto['precio'].replace(',', '.') # Cambia , por .
        precios.append(float(valor_limpio))
    
    # Cálculos 
    subtotal = sum(precios)
    iva = subtotal * 0.10  # IVA del 10% 
    total_final = subtotal + iva

    # Crear el ticket JSON 
    ticket = {
        "subtotal": round(subtotal, 2),
        "iva": round(iva, 2),
        "total": round(total_final, 2),
        "productos": carrito
    }

    # Guardar archivo JSON
    nombre = f"datos/ticket_{datetime.now().strftime('%H%M%S')}.json"
    with open(nombre, 'w') as f:
        json.dump(ticket, f, indent=4)
        
    return total_final # DEVOLVEMOS EL VALOR, NO LLAMAMOS A LA FUNCIÓN OTRA VEZ


# Configuración del sistema de logs
# Asegura que la carpeta 'logs' exista antes de configurar
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/ventas.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def registrar_log_venta(importe):
    """
    Genera un log de tipo INFO tras una venta exitosa.
    """
    # Mensaje de log 
    mensaje = f"Venta realizada con éxito. Total: {importe}€" 
    logging.info(mensaje) 
    print(f"{mensaje}")

def calcular_totales(lista_precios):
    """
    Calcula subtotal, IVA (10%) y total final.
    """
    if not lista_precios:
        return 0, 0, 0
    
    subtotal = sum(lista_precios)
    iva = subtotal * 0.10  
    total = subtotal + iva
    return round(subtotal, 2), round(iva, 2), round(total, 2)