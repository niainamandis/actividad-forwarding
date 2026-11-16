import re

# define los archivos de salida de cada router
archivos = ["salida_ttl_R1.txt", "salida_ttl_R2.txt", "salida_ttl_R3.txt", "salida_ttl_R4.txt", "salida_ttl_R5.txt"]
# define cuántas líneas se enviaron
total_enviadas = 30

if __name__ == "__main__":

  # lee las líneas de R5
  with open("salida_ttl_R5.txt") as archivo:
    lineas_R5 = [linea.rstrip("\n") for linea in archivo]

  # cuenta las líneas que llegaron a R5
  llegadas = [linea for linea in lineas_R5 if linea.startswith("linea")]
  print("líneas que llegaron a R5: {} de {}".format(len(llegadas), total_enviadas))

  # arma el orden de llegada
  orden = []
  for linea in lineas_R5:
    # extrae "linea n" al inicio de la línea
    coincidencia = re.match(r"linea [0-9]*", linea)
    if coincidencia:
      orden.append(coincidencia.group())
  print("orden de llegada en R5:")
  print(" ".join(orden))

  # busca las líneas que faltan
  print("líneas que faltan:")
  for i in range(1, total_enviadas + 1):
    # revisa si existe la línea exacta
    if "linea {}".format(i) not in lineas_R5:
      print("falta linea {}".format(i))

  # cuenta los redirigiendo y los TTL 0 de cada router
  print("conteo por router:")
  for nombre in archivos:
    with open(nombre) as archivo:
      lineas = archivo.readlines()
    # cuenta las líneas con redirigiendo
    redirigidos = sum(1 for linea in lineas if "redirigiendo" in linea)
    # cuenta las líneas con TTL 0
    descartados = sum(1 for linea in lineas if "TTL 0" in linea)
    print("{}: redirigiendo={} ttl0={}".format(nombre, redirigidos, descartados))
