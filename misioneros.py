#PRÁCTICA DEL PRIMER PARCIAL - MISIONEROS Y CANÍBALES
# Grupo 1

from collections import deque
import heapq
import time


### 1: VALIDACIÓN DE ESTADOS ###

def es_valido(estado):
    """
    Verifica que un estado cumpla las restricciones del problema:
    - No salirse del rango [0,3]
    - En ninguna orilla los caníbales deben superar a los misioneros
      (solo si hay misioneros en esa orilla)
    """
    m_izq, c_izq, _ = estado
    m_der = 3 - m_izq
    c_der = 3 - c_izq

    # Rango válido
    if not (0 <= m_izq <= 3 and 0 <= c_izq <= 3):
        return False

    # Restricción en la orilla izquierda
    if m_izq > 0 and c_izq > m_izq:
        return False

    # Restricción en la orilla derecha
    if m_der > 0 and c_der > m_der:
        return False

    return True



### 2: GENERACIÓN DE SUCESORES ###

def generar_sucesores(estado):
    """
    Devuelve la lista de estados alcanzables desde 'estado'
    aplicando movimientos válidos.
    """
    m_izq, c_izq, bote = estado
    movimientos = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    sucesores = []

    for m, c in movimientos:
        if bote == 1:  # si el bote esta en la izquierda-- va hacia la derecha (se debe restar)
            nuevo = (m_izq - m, c_izq - c, 0)
        else:          # si el bote esta en la derecha--  regresa a la izquierda (se debe sumar)
            nuevo = (m_izq + m, c_izq + c, 1)

        if es_valido(nuevo):
            sucesores.append(nuevo)

    return sucesores


### 3: BFS - BÚSQUEDA EN ANCHURA ###

def bfs(inicio, meta):
    """
    Búsqueda en anchura (Breadth-First Search).
    Garantiza encontrar la solución óptima (menor número de pasos).
    """
    inicio_tiempo = time.time()

    cola = deque()
    cola.append((inicio, [inicio]))
    visitados = {inicio}
    nodos_expandidos = 0
    max_frontera = 1

    while cola:
        max_frontera = max(max_frontera, len(cola))
        estado, camino = cola.popleft()
        nodos_expandidos += 1

        if estado == meta:
            tiempo_total = (time.time() - inicio_tiempo) * 1000  # ms
            return {
                "algoritmo": "BFS",
                "camino": camino,
                "nodos_expandidos": nodos_expandidos,
                "longitud_solucion": len(camino) - 1,
                "tiempo_ms": round(tiempo_total, 4),
                "max_frontera": max_frontera,
            }

        for suc in generar_sucesores(estado):
            if suc not in visitados:
                visitados.add(suc)
                cola.append((suc, camino + [suc]))

    return None  # si no se encontro una solución



### 4: A* - A ESTRELLA (búsqueda informada) ###

def heuristica(estado):
    """
    Heurística admisible: número de personas que aún faltan
    por cruzar al lado derecho.
    """
    m_izq, c_izq, _ = estado
    return m_izq + c_izq


def a_estrella(inicio, meta):
    """
    Búsqueda A* con heurística admisible.
    Encuentra la solución óptima expandiendo menos nodos que BFS.
    """
    inicio_tiempo = time.time()

    # Cola de prioridad: (f, g, estado, camino)
    cola = []
    heapq.heappush(cola, (heuristica(inicio), 0, inicio, [inicio]))
    visitados = {}
    nodos_expandidos = 0
    max_frontera = 1

    while cola:
        max_frontera = max(max_frontera, len(cola))
        f, g, estado, camino = heapq.heappop(cola)
        nodos_expandidos += 1

        if estado == meta:
            tiempo_total = (time.time() - inicio_tiempo) * 1000
            return {
                "algoritmo": "A*",
                "camino": camino,
                "nodos_expandidos": nodos_expandidos,
                "longitud_solucion": len(camino) - 1,
                "tiempo_ms": round(tiempo_total, 4),
                "max_frontera": max_frontera,
            }

        # Si ya visitamos este estado con un costo menor o igual, lo saltamos
        if estado in visitados and visitados[estado] <= g:
            continue
        visitados[estado] = g

        for suc in generar_sucesores(estado):
            nuevo_g = g + 1
            nuevo_f = nuevo_g + heuristica(suc)
            heapq.heappush(cola, (nuevo_f, nuevo_g, suc, camino + [suc]))

    return None



### 5: VISUALIZACIÓN DE LA SOLUCIÓN (mostrara en una tabla) ###

def mostrar_camino(resultado):
    print(f"\n{'=' * 55}")
    print(f"  Algoritmo: {resultado['algoritmo']}")
    print(f"{'=' * 55}")
    print(f"  Nodos expandidos : {resultado['nodos_expandidos']}")
    print(f"  Longitud solución: {resultado['longitud_solucion']} pasos")
    print(f"  Tiempo ejecución : {resultado['tiempo_ms']} ms")
    print(f"  Máx. frontera    : {resultado['max_frontera']}")
    print(f"{'-' * 55}")
    print(f"  {'#':<3} {'M_izq':<6} {'C_izq':<6} {'Bote':<6} {'Acción'}")
    print(f"{'-' * 55}")

    camino = resultado["camino"]
    for i, estado in enumerate(camino):
        m_izq, c_izq, bote = estado
        bote_txt = "Izq" if bote == 1 else "Der"

        # Descripción del movimiento respecto al estado anterior
        if i == 0:
            accion = "Estado inicial"
        else:
            m_ant, c_ant, b_ant = camino[i - 1]
            dm = m_ant - m_izq if b_ant == 1 else m_izq - m_ant
            dc = c_ant - c_izq if b_ant == 1 else c_izq - c_ant
            partes = []
            if dm > 0:
                partes.append(f"{dm} misionero(s)")
            if dc > 0:
                partes.append(f"{dc} caníbal(es)")
            direccion = "→" if b_ant == 1 else "←"
            accion = f"Mover {direccion} " + " y ".join(partes)

        print(f"  {i:<3} {m_izq:<6} {c_izq:<6} {bote_txt:<6} {accion}")

    print(f"{'=' * 55}\n")



### 6: TABLA COMPARATIVA ###

def tabla_comparativa(res_bfs, res_a):
    print(f"\n{'=' * 70}")
    print(f"  TABLA COMPARATIVA — MISIONEROS Y CANÍBALES")
    print(f"{'=' * 70}")
    print(f"  {'Métrica':<30} {'BFS':<18} {'A*':<18}")
    print(f"{'-' * 70}")

    metricas = [
        ("Nodos expandidos", "nodos_expandidos"),
        ("Longitud de solución", "longitud_solucion"),
        ("Tiempo (ms)", "tiempo_ms"),
        ("Máx. tamaño frontera", "max_frontera"),
    ]
    for etiqueta, clave in metricas:
        print(f"  {etiqueta:<30} {str(res_bfs[clave]):<18} {str(res_a[clave]):<18}")

    print(f"  {'¿Óptimo?':<30} {'Sí':<18} {'Sí':<18}")
    print(f"  {'¿Completo?':<30} {'Sí':<18} {'Sí':<18}")
    print(f"{'=' * 70}\n")


### 7: PROGRAMA PRINCIPAL ###

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  RESOLUCIÓN: MISIONEROS Y CANÍBALES")
    print("  Algoritmos: BFS y A*")
    print("=" * 55)

    estado_inicial = (3, 3, 1)   # 3 misioneros, 3 caníbales, bote izquierda
    estado_meta    = (0, 0, 0)   # todos a la derecha, bote derecha

    # Ejecutar BFS
    res_bfs = bfs(estado_inicial, estado_meta)
    if res_bfs:
        mostrar_camino(res_bfs)
    else:
        print("BFS no encontró solución")

    # Ejecutar A*
    res_a = a_estrella(estado_inicial, estado_meta)
    if res_a:
        mostrar_camino(res_a)
    else:
        print("A* no encontró solución")

    # Tabla comparativa
    if res_bfs and res_a:
        tabla_comparativa(res_bfs, res_a)