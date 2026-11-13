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

def check_routes(routes_file_name: str, destination_address: tuple[str, int]) -> tuple[str, int]:
  destination_ip, destination_puerto = destination_address
  # ip de destino a entero
  destination_num = int.from_bytes(bytes(int(num) for num in destination_ip.split(".")), "big")

  with open(routes_file_name) as archivo:
    for linea in archivo:
      campos = linea.split()
      # salta las líneas vacías
      if len(campos) == 0:
        continue
      # separa la red cidr en ip y prefijo
      red_ip, prefijo = campos[0].split("/")
      # ip de la red a entero
      red_num = int.from_bytes(bytes(int(num) for num in red_ip.split(".")), "big")
      # máscara a partir del prefijo
      mascara = (0xFFFFFFFF << (32 - int(prefijo))) & 0xFFFFFFFF
      # rango de puertos
      puerto_inicial = int(campos[1])
      puerto_final = int(campos[2])
      # si la ip está en la red y el puerto en el rango
      if (destination_num & mascara) == (red_num & mascara) and puerto_inicial <= destination_puerto <= puerto_final:
        # siguiente salto
        return (campos[3], int(campos[4]))
  # none si no hay ruta
  return None

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

  router_address = (router_IP, int(router_puerto))

  while True:
    IP_packet, sender_address = router_socket.recvfrom(1024)
    parsed_IP_packet = parse_packet(IP_packet)
    destination_address = (parsed_IP_packet["ip"], parsed_IP_packet["puerto"])

    # si el paquete es para este router
    if destination_address == router_address:
      # imprime mensaje sin headers
      print(parsed_IP_packet["mensaje"].decode())
    else:
      # busca el siguiente salto
      next_hop_address = check_routes(router_rutas, destination_address)
      # si existe una ruta
      if next_hop_address is None:
        # ignora el paquete
        print("No hay rutas hacia {} para paquete {}".format(destination_address, IP_packet))
      else:
        # informa el forward
        print("redirigiendo paquete {} con destino final {} desde {} hacia {}".format(IP_packet, destination_address, router_address, next_hop_address))
        # reenvía el paquete al siguiente salto
        router_socket.sendto(IP_packet, next_hop_address)

