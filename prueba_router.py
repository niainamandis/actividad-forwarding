import sys
import socket
from router import create_packet

if __name__ == "__main__":

  # formato ip;puerto;ttl
  headers = sys.argv[1]
  IP_router_inicial = sys.argv[2]
  puerto_router_inicial = int(sys.argv[3])
  # archivo a enviar
  archivo_nombre = sys.argv[4]

  IP_destino, puerto_destino, ttl = headers.split(";")

  # socket udp
  prueba_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  with open(archivo_nombre) as archivo:
    for linea in archivo:
      # arma el paquete con la línea como mensaje
      parsed_IP_packet = {"ip": IP_destino, "puerto": int(puerto_destino), "ttl": int(ttl), "mensaje": linea.encode()}
      IP_packet = create_packet(parsed_IP_packet)
      # envía el paquete al router inicial
      prueba_socket.sendto(IP_packet, (IP_router_inicial, puerto_router_inicial))
