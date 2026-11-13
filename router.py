import sys
import socket

def parse_packet(IP_packet: bytes):
  # ip en los primeros 4 bytes
  ip = ".".join(str(byte) for byte in IP_packet[0:4])
  # puerto en los siguientes 2 bytes
  puerto = int.from_bytes(IP_packet[4:6], "big")
  # mensaje en los bytes restantes
  mensaje = IP_packet[6:]
  # paquete parseado
  return {"ip": ip, "puerto": puerto, "mensaje": mensaje}

def create_packet(parsed_IP_packet):
  # convierte la ip a 4 bytes
  ip_bytes = bytes(int(num) for num in parsed_IP_packet["ip"].split("."))
  # convierte el puerto a 2 bytes
  puerto_bytes = parsed_IP_packet["puerto"].to_bytes(2, "big")
  # paquete en bytes
  return ip_bytes + puerto_bytes + parsed_IP_packet["mensaje"]

if __name__ == "__main__":

  router_IP = sys.argv[1]
  router_puerto = sys.argv[2]
  router_rutas = sys.argv[3]

  print("router_IP:", router_IP)
  print("router_puerto:", router_puerto)
  print("router_rutas:", router_rutas)

  # crea el socket udp
  router_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  # asocia el socket al par (ip, puerto)
  router_socket.bind((router_IP, int(router_puerto)))

  # paquete de prueba manual
  IP_packet_v1 = bytes([127, 0, 0, 1]) + (8881).to_bytes(2, "big") + b"hola"
  parsed_IP_packet = parse_packet(IP_packet_v1)
  IP_packet_v2 = create_packet(parsed_IP_packet)
  # verificar que ambos paquetes sean iguales
  print("IP_packet_v1 == IP_packet_v2 ? {}".format(IP_packet_v1 == IP_packet_v2))
