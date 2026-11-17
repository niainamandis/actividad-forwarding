# Actividad: Forwarding básico

Simulación de un mini-Internet en python, donde cada router es un proceso con un socket UDP, una tabla de rutas y paquetes IP codificados en bytes.

## Características

- Forwarding según tablas de rutas (red CIDR y rango de puertos)
- Round-robin por área cuando hay varias rutas posibles
- Header de 7 bytes: IP (4), puerto (2) y TTL (1)
- Descarte de paquetes con TTL 0 y decremento del TTL en cada salto

## Estructura del repositorio

```
.
├── router.py             # router: parse_packet, create_packet, check_routes y loop
├── enviar.py             # envía un paquete 
├── prueba_router.py      # envía un archivo línea por línea con TTL
├── rutas/                # tablas de rutas por versión
│   ├── v1/               # ejemplo 1 (2 routers)
│   ├── v2/               # ejemplo 2 (3 routers) y tabla mal configurada
│   ├── v3/               # red de 5 routers
│   ├── v3_default/       # red de 5 routers con router default (7000)
│   └── v4/               # red con R0 y R6
└── ttl/                  # pruebas con TTL
    ├── analizar_salidas.py
    ├── entradas/         # archivos a enviar
    └── salidas/          # salidas guardadas de los routers
```

## Requisitos

- Python 3 (probado con 3.13)
- Solo librerías estándar (`sys`, `socket`, `re`)

## Ejecución

Todos los comandos se ejecutan desde la raíz del repositorio.

**1. Levantar un router** (una terminal por router):

```
python3 router.py <IP> <puerto> <archivo_de_rutas>
```

Ejemplo:

```
python3 router.py 127.0.0.1 8881 rutas/v3/rutas_R1_v3.txt
```

**2. Enviar un archivo línea por línea** (con TTL):

```
python3 prueba_router.py "<IP_destino>;<puerto_destino>;<TTL>" <IP_router_inicial> <puerto_router_inicial> <archivo>
```

Ejemplo, de R1 a R5 con TTL 10:

```
python3 prueba_router.py "127.0.0.1;8885;10" 127.0.0.1 8881 ttl/entradas/archivo_grande.txt
```

**3. Analizar las salidas guardadas** (opcional):

```
python3 ttl/analizar_salidas.py
```
