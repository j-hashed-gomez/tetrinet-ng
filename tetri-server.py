import asyncio
import websockets
import logging
from datetime import datetime

# Configurar el registro para verbose y errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clase Connection para almacenar la IP y la hora de conexión
class Connection:
    def __init__(self, client_ip, connect_time):
        self.client_ip = client_ip  # Dirección IP del cliente
        self.connect_time = connect_time  # Timestamp de la conexión

# Lista para almacenar los objetos de conexiones
connections = []

# Función que manejará cada nueva conexión
async def handle_connection(websocket, path):
    try:
        # Obtener la IP del cliente
        client_ip = websocket.remote_address[0]
        connection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Crear una nueva conexión y agregarla a la lista de conexiones
        new_connection = Connection(client_ip, connection_time)
        connections.append(new_connection)
        
        # Registro verbose
        logging.info(f'Nueva conexión desde {client_ip} a las {connection_time}')
        
        # Mantener la conexión abierta (si deseas recibir mensajes)
        async for message in websocket:
            logging.info(f'Mensaje recibido de {client_ip}: {message}')
        
    except Exception as e:
        # Registrar cualquier error que ocurra durante la conexión
        logging.error(f'Error con la conexión desde {client_ip}: {str(e)}')
    
    finally:
        # Al desconectar, eliminar la conexión de la lista
        connections[:] = [conn for conn in connections if conn.client_ip != client_ip]
        logging.info(f'Conexión cerrada desde {client_ip}')

# Función principal para iniciar el servidor WebSocket
async def main():
    # Iniciar el servidor en el puerto 5432
    server = await websockets.serve(handle_connection, '0.0.0.0', 5432)
    
    logging.info('Servidor WebSocket iniciado en el puerto 5432')
    
    # Mantener el servidor corriendo
    await server.wait_closed()

# Ejecutar el servidor
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f'Error al iniciar el servidor: {str(e)}')
