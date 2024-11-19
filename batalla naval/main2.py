import pygame
import random
pygame.mixer.init()
sonido_acierto = pygame.mixer.Sound("musica/medium-explosion-40472.mp3")
sonido_error = pygame.mixer.Sound("musica/object-drops-in-water-84639.mp3")


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
    "tamaño_de_celda": 20,
    "tablero": None,
    "revelado": None,
    "puntaje": 0
}


# Función para crear el tablero
def crear_tablero(dificultad, barcos:dict):
    tablero = [[0] * dificultad for _ in range(dificultad)]
    for tamaño, cantidad in barcos.items():
        for _ in range(cantidad):
            colocado = False
            while not colocado:
                orientacion = random.choice([0, 1])
                if orientacion == 0:
                    fila = random.randint(0, dificultad - 1)
                    col = random.randint(0, dificultad - tamaño)
                else:
                    fila = random.randint(0, dificultad - tamaño)
                    col = random.randint(0, dificultad - 1)

                if espacio_libre(tablero, fila, col, tamaño, orientacion):
                    for i in range(tamaño):
                        if orientacion == 0:
                            tablero[fila][col + i] = 1
                        else:
                            tablero[fila + i][col] = 1
                    colocado = True
    return tablero



# Función para verificar si hay espacio libre
def espacio_libre(tablero, fila, col, tamaño, orientacion):
    for i in range(tamaño):
        if orientacion == 0 and tablero[fila][col + i] != 0:
            return False
        if orientacion == 1 and tablero[fila + i][col] != 0:
            return False
    return True


# Función para dibujar el tablero
def dibujar_tablero(estado_juego:dict, pantalla):
    dificultad = estado_juego["dificultad"]
    tamaño_de_celda = estado_juego["tamaño_de_celda"]
    tablero = estado_juego["tablero"]
    revelado = estado_juego["revelado"]

    tablero_ancho = dificultad * tamaño_de_celda
    tablero_alto = dificultad * tamaño_de_celda
    offset_x = (tamaño_pantalla[0] - tablero_ancho) // 2
    offset_y = (tamaño_pantalla[1] - tablero_alto) // 2

    for fila in range(dificultad):
        for columna in range(dificultad):
            x = columna * tamaño_de_celda + offset_x
            y = fila * tamaño_de_celda + offset_y
            rect = pygame.Rect(x, y, tamaño_de_celda, tamaño_de_celda)
            pygame.draw.rect(pantalla, WHITE, rect, 1)
            if revelado[fila][columna]:
                if tablero[fila][columna] == 1:
                    pantalla.blit(equis,(x,y))
                else:
                    pantalla.blit(circulo,(x,y))

# Función para manejar clics
def manejar_clic(pos, estado_juego):
    dificultad = estado_juego["dificultad"]
    tamaño_de_celda = estado_juego["tamaño_de_celda"]
    tablero = estado_juego["tablero"]
    revelado = estado_juego["revelado"]

    tablero_ancho = dificultad * tamaño_de_celda
    tablero_alto = dificultad * tamaño_de_celda
    offset_x = (tamaño_pantalla[0] - tablero_ancho) // 2
    offset_y = (tamaño_pantalla[1] - tablero_alto) // 2

    col = (pos[0] - offset_x) // tamaño_de_celda
    fila = (pos[1] - offset_y) // tamaño_de_celda

    if 0 <= col < dificultad and 0 <= fila < dificultad:
        if not revelado[fila][col]:
            revelado[fila][col] = True
            if tablero[fila][col] == 1:  # Disparo acertado
                estado_juego["puntaje"] += 5  # Sumar 5 puntos por acierto
                print(f"Acierto en ({fila}, {col}). Puntaje actual: {estado_juego['puntaje']}")
                
                # Comprobar si la nave se hundió y sumar los puntos extra
                tamaño_nave = es_nave_hundida(tablero, revelado, fila, col)
                if tamaño_nave > 0:  # Si la nave se hunde
                    estado_juego["puntaje"] += 10 * tamaño_nave  # Sumar 10 puntos por cada parte de la nave
                    print(f"Nave hundida! Sumas {10 * tamaño_nave} puntos. Puntaje actual: {estado_juego['puntaje']}")
                    sonido_acierto.play()
                else:
                    sonido_acierto.play()  
            else:  # Disparo erróneo
                estado_juego["puntaje"] -= 1  # Restar 1 punto por disparo erróneo
                print(f"Error en ({fila}, {col}). Puntaje actual: {estado_juego['puntaje']}")
                sonido_error.play()


def es_nave_hundida(tablero, revelado, fila, col):
    # Verificar horizontalmente
    tamaño_nave = 0
    total_casillas = 0

    # Revisar hacia la izquierda
    c = col
    while c >= 0 and tablero[fila][c] == 1:
        total_casillas += 1
        if revelado[fila][c]:
            tamaño_nave += 1
        c -= 1

    # Revisar hacia la derecha
    c = col + 1
    while c < len(tablero) and tablero[fila][c] == 1:
        total_casillas += 1
        if revelado[fila][c]:
            tamaño_nave += 1
        c += 1

    # Si la nave está completamente revelada horizontalmente, regresar el tamaño de la nave
    if total_casillas > 1 and tamaño_nave == total_casillas:
        return total_casillas

    # Verificar verticalmente
    tamaño_nave = 0
    total_casillas = 0

    # Revisar hacia arriba
    f = fila
    while f >= 0 and tablero[f][col] == 1:
        total_casillas += 1
        if revelado[f][col]:
            tamaño_nave += 1
        f -= 1

    # Revisar hacia abajo
    f = fila + 1
    while f < len(tablero) and tablero[f][col] == 1:
        total_casillas += 1
        if revelado[f][col]:
            tamaño_nave += 1
        f += 1

    # Si la nave está completamente revelada verticalmente, regresar el tamaño de la nave
    if total_casillas > 1 and tamaño_nave == total_casillas:
        return total_casillas

    return 0  # Si la nave no está completamente hundida, regresamos 0


# Función para mostrar el puntaje
def mostrar_puntaje(estado_juego, pantalla):
    if isinstance(estado_juego, dict) and 'puntaje' in estado_juego:
        font = pygame.font.Font(None, 36)
        texto = font.render(f"Puntaje: {str(estado_juego['puntaje']).zfill(4)}", True, WHITE)
        pantalla.blit(texto, (10, 10))
    else:
        print("Error: estado_juego no es un diccionario o no contiene 'puntaje'.")


# Función para el menú de dificultad
def menu_dificultad(estado_juego, pantalla):
    fondo_guerra = pygame.image.load("imagenes/Diseño sin título.png")
    fondo_guerra = pygame.transform.scale(fondo_guerra, tamaño_pantalla)
    menu_activo = True



    # Crear botones
    boton_facil = pygame.Rect(300, 200, 200, 50)
    boton_medio = pygame.Rect(300, 300, 200, 50)
    boton_dificil = pygame.Rect(300, 400, 200, 50)
    boton_salir = pygame.Rect(300, 500, 200, 50)
    while menu_activo:
        # Dibujar el fondo
        pantalla.blit(fondo_guerra, (0, 0))

        # Dibujar botones
        dibujar_boton(pantalla, boton_facil, "Fácil", BLUE, WHITE)
        dibujar_boton(pantalla, boton_medio, "Medio", YELLOW, WHITE)
        dibujar_boton(pantalla, boton_dificil, "Difícil", RED, WHITE)
        dibujar_boton(pantalla, boton_salir, "Salir", BLACK, WHITE)

        pygame.display.update()  # Actualizar la pantalla

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si el jugador cierra la ventana
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo
                if boton_facil.collidepoint(event.pos):  # Verificar si clicó en "Fácil"
                    estado_juego["dificultad"] = 10
                    estado_juego["tamaño_de_celda"] = 30
                    menu_activo = False  # Salir del menú
                elif boton_medio.collidepoint(event.pos):  # Verificar si clicó en "Medio"
                    estado_juego["dificultad"] = 20
                    estado_juego["tamaño_de_celda"] = 20
                    for k in barcos:
                            barcos[k] *= 2  # Multiplicar barcos
                    menu_activo = False  # Salir del menú
                elif boton_dificil.collidepoint(event.pos):  # Verificar si clicó en "Difícil"
                    estado_juego["dificultad"] = 40
                    estado_juego["tamaño_de_celda"] = 15
                    for k in barcos:
                            barcos[k] *= 3 # Multiplicar barcos
                    menu_activo = False  # Salir del menú
                elif boton_salir.collidepoint(event.pos):  # Verificar si clicó en "Salir"
                    pygame.quit()
                    exit()





def dibujar_boton(pantalla, rect, texto, color_fondo, color_texto):
    """Dibuja un botón con texto."""
    pygame.draw.rect(pantalla, color_fondo, rect)  # Dibuja el rectángulo del botón
    texto_render = font.render(texto, True, color_texto)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)  # Dibuja el texto centrado en el botón












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


boton_jugar = pygame.Rect(300, 200, 200, 50)
boton_ver_puntajes = pygame.Rect(300, 300, 200, 50)
boton_salir = pygame.Rect(300, 700, 200, 50)


















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
circulo = pygame.transform.scale(circulo, (estado_juego["tamaño_de_celda"], estado_juego["tamaño_de_celda"]))
equis = pygame.image.load("imagenes/x.png")
equis = pygame.transform.scale(equis, (estado_juego["tamaño_de_celda"], estado_juego["tamaño_de_celda"]))




menu_principal()
menu_dificultad(estado_juego, pantalla)
estado_juego["tablero"] = crear_tablero(estado_juego["dificultad"], barcos)
estado_juego["revelado"] = [[False] * estado_juego["dificultad"] for _ in range(estado_juego["dificultad"])]
game_over = False
while not game_over:
    reloj.tick(60)
    for event in pygame.event.get():
        mostrar_puntaje(estado_juego,pantalla)
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo
                resultado = manejar_clic(pygame.mouse.get_pos(),estado_juego)










    # Dibujar fondo y tablero
    pantalla.blit(fondo, (0, 0))
    dibujar_tablero(estado_juego, pantalla)
    mostrar_puntaje(estado_juego,pantalla)
    pygame.display.update()










pygame.quit()




