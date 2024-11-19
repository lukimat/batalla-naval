import pygame 
import random
from constantes import *
from funciones import *

# constastes
tamaño_pantalla=(800,800)

tamaño_de_celda=[20]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW=(255, 255, 0)

    # Definir los barcos

barcos = {
        1: 4,  # 4 submarinos de 1 casillero
        2: 3,  # 3 destructores de 2 casilleros
        3: 2,  # 2 cruceros de 3 casilleros
        4: 1   # 1 acorazado de 4 casilleros
    }



def crear_tablero(dificultad, barcos:dict):
    # Inicializar tablero vacío
    tablero= [[0] * dificultad for _ in range(dificultad)]
    # Colocar cada tipo de barco
    for tamaño , cantidad in barcos.items():
        for _ in range(cantidad):
            colocado=False
            while not colocado:
                # Elegir orientación: 0 = horizontal, 1 = vertical
                orientacion = random.choice([0, 1])
                if orientacion == 0:  # Horizontal
                    fila = random.randint(0, dificultad - 1)
                    col = random.randint(0, dificultad - tamaño)
                else:  # Vertical
                    fila = random.randint(0, dificultad - tamaño)
                    col = random.randint(0, dificultad - 1)

                # Verificar si el espacio está libre
                if espacio_libre(tablero, fila, col, tamaño, orientacion):
                    # Colocar barco
                    for i in range(tamaño):
                        if orientacion == 0:  # Horizontal
                            tablero[fila][col + i] = 1
                        else:  # Vertical
                            tablero[fila + i][col] = 1
                    colocado = True


    return tablero




def espacio_libre(tablero, fila, col, tamaño, orientacion):
    """Verifica si el espacio está libre para colocar un barco."""
    for i in range(tamaño):
        if orientacion == 0:  # Horizontal
            if tablero[fila][col + i] != 0:
                return False
        else:  # Vertical
            if tablero[fila + i][col] != 0:
                return False
    return True









def dibujar_tablero():
    # Calcular dimensiones del tablero
    tablero_ancho = dificultad * tamaño_de_celda[0]
    tablero_alto = dificultad * tamaño_de_celda[0]
    # Calcular desplazamientos para centrar
    offset_x = (tamaño_pantalla[0] - tablero_ancho) // 2
    offset_y = (tamaño_pantalla[1] - tablero_alto) // 2

    for filas in range(dificultad):
        for columnas in range(dificultad):
            # Calcular la posición de la celda
            x= columnas * tamaño_de_celda[0] + offset_x
            y= filas * tamaño_de_celda[0] + offset_y
            # Dibujar el contorno de la celda
            rect = pygame.Rect(x, y, tamaño_de_celda[0], tamaño_de_celda[0])
            pygame.draw.rect(pantalla, WHITE, rect, 1)  # Dibujar borde
            # Revisar si la celda está revelada
            if revelado[filas][columnas]:
                if tablero[filas][columnas] == 1:  # Barco
                    pantalla.blit(equis, (x, y))
                else:  # Agua
                    pantalla.blit(circulo, (x, y))



# def manejar_clic(pos):
#     # Calcular dimensiones del tablero
#     tablero_ancho = dificultad * tamaño_de_celda[0]
#     tablero_alto = dificultad * tamaño_de_celda[0]
#     # Calcular desplazamientos dinámicos
#     offset_x = (tamaño_pantalla[0] - tablero_ancho) // 2
#     offset_y = (tamaño_pantalla[1] - tablero_alto) // 2

#     # Ajustar posición del clic según el desplazamiento
#     col = (pos[0] - offset_x) // tamaño_de_celda[0]
#     fila = (pos[1] - offset_y) // tamaño_de_celda[0]

#     # Verificar que el clic esté dentro del tablero
#     if 0 <= col < dificultad and 0 <= fila < dificultad:
#         if not revelado[fila][col]:  # Solo actúa si no está revelada
#             revelado[fila][col] = True
#             return tablero[fila][col] == 1  # Devuelve True si es un barco
#     return None

def manejar_clic(pos):
    tablero_ancho = dificultad * tamaño_de_celda
    tablero_alto = dificultad * tamaño_de_celda
    offset_x = (tamaño_pantalla[0] - tablero_ancho) // 2
    offset_y = (tamaño_pantalla[1] - tablero_alto) // 2

    # Calcular la fila y columna del clic
    col = (pos[0] - offset_x) // tamaño_de_celda
    fila = (pos[1] - offset_y) // tamaño_de_celda

    # Verificar que el clic esté dentro del tablero
    if 0 <= col < dificultad and 0 <= fila < dificultad:
        if not revelado[fila][col]:  # Solo actuar si la casilla no ha sido revelada
            revelado[fila][col] = True  # Marcar la casilla como revelada

            if tablero[fila][col] == 1:  # Acierto
                puntaje[0] += 5  # Sumar puntos por el acierto
                print(f"Acierto en ({fila}, {col}). Puntaje actual: {puntaje[0]}")
                
                # Verificar si la nave a la que pertenece está hundida
                if es_nave_hundida(tablero, revelado, fila, col):
                    print("¡Nave hundida!")
                    # Calcular el tamaño de la nave hundida
                    tamaño_nave = calcular_tamaño_nave(tablero, revelado, fila, col)
                    puntaje[0] += 10 * tamaño_nave  # Sumar puntos adicionales por cada casilla de la nave
                    print(f"Nave hundida de tamaño {tamaño_nave}. Puntaje actual: {puntaje[0]}")
            else:  # Error
                puntaje[0] -= 1  # Restar puntos por fallar
                print(f"Disparo errado en ({fila}, {col}). Puntaje actual: {puntaje[0]}")





def calcular_tamaño_nave(tablero, revelado, fila, col):
    tamaño_nave = 0

    # Contar casillas horizontalmente
    c = col
    while c >= 0 and tablero[fila][c] == 1:  # Hacia la izquierda
        tamaño_nave += 1
        c -= 1
    c = col + 1  # Evitar contar la casilla inicial dos veces
    while c < len(tablero) and tablero[fila][c] == 1:  # Hacia la derecha
        tamaño_nave += 1
        c += 1

    # Contar casillas verticalmente
    f = fila
    while f >= 0 and tablero[f][col] == 1:  # Hacia arriba
        tamaño_nave += 1
        f -= 1
    f = fila + 1  # Evitar contar la casilla inicial dos veces
    while f < len(tablero) and tablero[f][col] == 1:  # Hacia abajo
        tamaño_nave += 1
        f += 1

    return tamaño_nave













def dibujar_boton(pantalla, rect, texto, color_fondo, color_texto):
    """Dibuja un botón con texto."""
    pygame.draw.rect(pantalla, color_fondo, rect)  # Dibuja el rectángulo del botón
    texto_render = font.render(texto, True, color_texto)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)  # Dibuja el texto centrado en el botón








def mostrar_puntaje(puntaje):
    font = pygame.font.Font(None, 36)  # Crear fuente para el texto
    texto = font.render(f"Puntaje: {str(puntaje[0]).zfill(4)}", True, WHITE)  # Formatear puntaje
    pantalla.blit(texto, (10, 10))  # Dibujar el texto en la pantalla



def menu_principal():
    fondo_guerra = pygame.image.load("imagenes/desktop-wallpaper-war-ship-sea-battle.jpg")
    fondo_guerra = pygame.transform.scale(fondo_guerra, tamaño_pantalla)
    menu_activo=True
    while menu_activo:
        pantalla.blit(fondo_guerra,(0,0))
                # Dibujar botones
        dibujar_boton(pantalla, boton_jugar, "Jugar", BLUE, WHITE)
        dibujar_boton(pantalla, boton_ver_puntajes, "Ver Puntajes", BLUE, WHITE)
        dibujar_boton(pantalla, boton_salir, "Salir", BLUE, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    if boton_jugar.collidepoint(event.pos):
                        print("Jugar presionado")
                        menu_activo = False  # Sal del menú para empezar el juego
                    elif boton_ver_puntajes.collidepoint(event.pos):
                        print("Ver Puntajes presionado")
                        # Aquí podrías mostrar una pantalla de puntajes
                    elif boton_salir.collidepoint(event.pos):
                        print("Salir presionado")
                        pygame.quit()
                        exit()
        pygame.display.update()
        reloj.tick(60)




def menu_dificultad():
    global dificultad, tablero, revelado, barcos
    fondo_guerra = pygame.image.load("imagenes/Diseño sin título.png")
    fondo_guerra = pygame.transform.scale(fondo_guerra, tamaño_pantalla)
    menu_activo = True
    while menu_activo:
        pantalla.blit(fondo_guerra, (0, 0))
        # Dibujar botones
        dibujar_boton(pantalla, boton_facil, "Fácil", BLUE, WHITE)
        dibujar_boton(pantalla, boton_medio, "Medio", YELLOW, WHITE)
        dibujar_boton(pantalla, boton_dificil, "Difícil", RED, WHITE)
        dibujar_boton(pantalla, boton_salir, "Salir", BLUE, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    if boton_facil.collidepoint(event.pos):
                        print("Fácil presionado")
                        dificultad = 10
                        tablero = crear_tablero(dificultad, barcos)  # Regenerar el tablero
                        revelado = [[False] * dificultad for _ in range(dificultad)]  # Reiniciar revelado
                        menu_activo = False
                    elif boton_medio.collidepoint(event.pos):
                        print("Medio presionado")
                        dificultad = 20
                        for k in barcos:
                            barcos[k] *= 2  # Multiplicar barcos
                        tablero = crear_tablero(dificultad, barcos)
                        revelado = [[False] * dificultad for _ in range(dificultad)]
                        menu_activo = False
                    elif boton_dificil.collidepoint(event.pos):
                        print("Difícil presionado")
                        dificultad = 40
                        tamaño_de_celda[0]=15
                        for k in barcos:
                            barcos[k] *= 3 # Multiplicar barcos
                        tablero = crear_tablero(dificultad, barcos)
                        revelado = [[False] * dificultad for _ in range(dificultad)]
                        menu_activo = False
                    elif boton_salir.collidepoint(event.pos):
                        print("Salir presionado")
                        pygame.quit()
                        exit()
        pygame.display.update()
        reloj.tick(60)













def es_nave_hundida(tablero, revelado, fila, col):
    # Verificar horizontalmente
    c = col
    while c >= 0 and tablero[fila][c] == 1:  # Hacia la izquierda
        if not revelado[fila][c]:
            return False
        c -= 1
    c = col
    while c < len(tablero) and tablero[fila][c] == 1:  # Hacia la derecha
        if not revelado[fila][c]:
            return False
        c += 1

    # Verificar verticalmente
    f = fila
    while f >= 0 and tablero[f][col] == 1:  # Hacia arriba
        if not revelado[f][col]:
            return False
        f -= 1
    f = fila
    while f < len(tablero) and tablero[f][col] == 1:  # Hacia abajo
        if not revelado[f][col]:
            return False
        f += 1

    return True  # Si no hay casillas pendientes, la nave está hundida



























pygame.mixer.init()
sonido_acierto = pygame.mixer.Sound("musica/medium-explosion-40472.mp3")
sonido_error = pygame.mixer.Sound("musica/object-drops-in-water-84639.mp3")


pygame.init()

# Configuración básica
reloj = pygame.time.Clock()
pantalla = pygame.display.set_mode(tamaño_pantalla)
pygame.display.set_caption("Batalla Naval")
font = pygame.font.Font(None, 36)

# Cargar imágenes
fondo = pygame.image.load("imagenes/mar.jpg")
fondo = pygame.transform.scale(fondo, tamaño_pantalla)
circulo = pygame.image.load("imagenes/circle.png")
circulo = pygame.transform.scale(circulo, (tamaño_de_celda[0], tamaño_de_celda[0]))
equis = pygame.image.load("imagenes/x.png")
equis = pygame.transform.scale(equis, (tamaño_de_celda[0], tamaño_de_celda[0]))

# Variables del juego
dificultad = 10



# Crear botones (Rectángulos)
boton_jugar = pygame.Rect(300, 200, 200, 50)
boton_ver_puntajes = pygame.Rect(300, 300, 200, 50)
boton_facil = pygame.Rect(300, 190, 200, 50)
boton_medio = pygame.Rect(300, 350, 200, 50)
boton_dificil = pygame.Rect(300, 500, 200, 50)
boton_salir = pygame.Rect(300, 700, 200, 50)



menu_principal()
menu_dificultad()
tablero = crear_tablero(dificultad, barcos)
revelado = [[False] * dificultad for _ in range(dificultad)]
puntaje=[0]
game_over = False
while not game_over:
    reloj.tick(60)
    for event in pygame.event.get():
        mostrar_puntaje(puntaje)
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo
                resultado = manejar_clic(pygame.mouse.get_pos())
                if resultado is not None:
                    if resultado:
                        print("¡Acierto!")
                        sonido_acierto.play()
                    else:
                        print("Fallaste.")
                        sonido_error.play()











    # Dibujar fondo y tablero
    pantalla.blit(fondo, (0, 0))
    dibujar_tablero()
    mostrar_puntaje(puntaje)
    pygame.display.update()










pygame.quit()