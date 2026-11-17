import sys
import socket
from router import create_packet

if __name__ == "__main__":

  IP_router_final = sys.argv[1]
  puerto_router_final = int(sys.argv[2])
  mensaje = sys.argv[3]
  IP_envio = sys.argv[4]
  puerto_envio = int(sys.argv[5])
  ttl = int(sys.argv[6])

  # arma el paquete con el destino final, ttl y el mensaje
  parsed_IP_packet = {"ip": IP_router_final, "puerto": puerto_router_final, "ttl": ttl, "mensaje": mensaje.encode()}
  IP_packet = create_packet(parsed_IP_packet)

  # crea el socket udp
  envio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # envía el paquete a la dirección de envío
  envio_socket.sendto(IP_packet, (IP_envio, puerto_envio))
