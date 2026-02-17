from librerias import libreria as lib

def ejecutar():
    # Obtener los datos del pedido
    carrito = lib.menu() 
    
    if carrito:
        # Procesar
        # Guardar el resultado en la variable 'total'
        total = lib.procesar_venta(carrito)
        
        # Registrar log, solo si la venta se completa 
        lib.registrar_log_venta(total)
        print(f"Venta completada: {total}€")

if __name__ == "__main__":
    ejecutar()