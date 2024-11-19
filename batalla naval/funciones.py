import pygame
import random

# Constantes
tamaño_pantalla = (800, 800)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

barcos = {
    1: 4,  # Submarinos
    2: 3,  # Destructores
    3: 2,  # Cruceros
    4: 1   # Acorazado
}

# Inicializar estado del juego
estado_juego = {
    "dificultad": 10,
    "tamaño_de_celda": 30,
    "tablero": None,
    "revelado": None,
    "puntaje": 0
}

# Funciones del juego
def crear_tablero(dificultad, barcos):
    tablero = [[0] * dificultad for _ in range(dificultad)]
    for tamaño, cantidad in barcos.items():
        for _ in range(cantidad):
            colocado = False
            while not colocado:
                orientacion = random.choice([0, 1])
                fila, col = random.randint(0, dificultad - 1), random.randint(0, dificultad - tamaño)
                if orientacion == 1: fila, col = random.randint(0, dificultad - tamaño), random.randint(0, dificultad - 1)

                if espacio_libre(tablero, fila, col, tamaño, orientacion):
                    for i in range(tamaño):
                        if orientacion == 0: tablero[fila][col + i] = 1
                        else: tablero[fila + i][col] = 1
                    colocado = True
    return tablero

def espacio_libre(tablero, fila, col, tamaño, orientacion):
    for i in range(tamaño):
        if orientacion == 0 and tablero[fila][col + i] != 0: return False
        if orientacion == 1 and tablero[fila + i][col] != 0: return False
    return True

def dibujar_tablero(estado_juego, pantalla):
    dificultad, tamaño_celda = estado_juego["dificultad"], estado_juego["tamaño_de_celda"]
    tablero, revelado = estado_juego["tablero"], estado_juego["revelado"]
    offset_x = (tamaño_pantalla[0] - dificultad * tamaño_celda) // 2
    offset_y = (tamaño_pantalla[1] - dificultad * tamaño_celda) // 2

    for fila in range(dificultad):
        for col in range(dificultad):
            x, y = col * tamaño_celda + offset_x, fila * tamaño_celda + offset_y
            rect = pygame.Rect(x, y, tamaño_celda, tamaño_celda)
            pygame.draw.rect(pantalla, WHITE, rect, 1)
            if revelado[fila][col]:
                color = RED if tablero[fila][col] == 1 else BLUE
                pygame.draw.rect(pantalla, color, rect)

def manejar_clic(pos, estado_juego):
    dificultad, tamaño_celda = estado_juego["dificultad"], estado_juego["tamaño_de_celda"]
    tablero, revelado = estado_juego["tablero"], estado_juego["revelado"]
    offset_x = (tamaño_pantalla[0] - dificultad * tamaño_celda) // 2
    offset_y = (tamaño_pantalla[1] - dificultad * tamaño_celda) // 2

    col, fila = (pos[0] - offset_x) // tamaño_celda, (pos[1] - offset_y) // tamaño_celda
    if 0 <= fila < dificultad and 0 <= col < dificultad and not revelado[fila][col]:
        revelado[fila][col] = True
        if tablero[fila][col] == 1:
            estado_juego["puntaje"] += 5
        else:
            estado_juego["puntaje"] -= 1

def mostrar_puntaje(estado_juego, pantalla):
    font = pygame.font.Font(None, 36)
    texto = font.render(f"Puntaje: {estado_juego['puntaje']:04}", True, WHITE)
    pantalla.blit(texto, (10, 10))

def menu_dificultad(estado_juego, pantalla):
    boton_facil, boton_medio, boton_dificil = pygame.Rect(300, 200, 200, 50), pygame.Rect(300, 300, 200, 50), pygame.Rect(300, 400, 200, 50)
    botones = [(boton_facil, "Fácil", 10, 30), (boton_medio, "Medio", 20, 20), (boton_dificil, "Difícil", 40, 15)]
    fondo = pygame.Surface(tamaño_pantalla).fill(BLACK)

    menu_activo = True
    while menu_activo:
        pantalla.blit(fondo, (0, 0))
        for boton, texto, *_ in botones:
            pygame.draw.rect(pantalla, BLUE, boton)
            pantalla.blit(pygame.font.Font(None, 36).render(texto, True, WHITE), boton.topleft)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for boton, _, dificultad, tamaño_celda in botones:
                    if boton.collidepoint(event.pos):
                        estado_juego.update(dificultad=dificultad, tamaño_de_celda=tamaño_celda)
                        menu_activo = False

# Configuración del juego
pygame.init()
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Batalla Naval")
estado_juego.update(tablero=crear_tablero(estado_juego["dificultad"], barcos), revelado=[[False] * estado_juego["dificultad"] for _ in range(estado_juego["dificultad"])])

# Bucle Principal
menu_dificultad(estado_juego, pantalla)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: manejar_clic(pygame.mouse.get_pos(), estado_juego)

    pantalla.fill(BLACK)
    dibujar_tablero(estado_juego, pantalla)
    mostrar_puntaje(estado_juego, pantalla)
    pygame.display.flip()


















