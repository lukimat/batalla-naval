import pygame
import random
import sys
from configuracion_batalla import *



pygame.init()
fuente = pygame.font.SysFont('Arial', 25)
mensajes = []
puntaje = 0 


def pedir_nombre(puntaje:int, pantalla:pygame.surface)->str:

    """
    Funcion : Solicita al usuario que ingrese su nombre a través de un campo de texto en la pantalla.

    Parámetros:El puntaje actual del jugador que se muestra en la pantalla y La pantalla de Pygame donde se dibujarán los resultados                      

    Retorna:El nombre ingresado por el jugador.

    """
    imagen_victoria_cargada = pygame.transform.scale(imagen_victoria, (ANCHO, ALTO))
    fuente = pygame.font.SysFont('Arial', 23, bold = True)
    input_box = pygame.Rect(300, 300, 200, 40)
    color = pygame.Color(0, 0, 0)
    text = ''
    texto_puntaje = fuente.render(f"Felicidades !! hizo: {puntaje} puntos!!", True, (0, 0, 0))
    pantalla.blit(texto_puntaje, (250, 250))
    texto_titulo = fuente.render("Ingrese su nombre/nick:", True, (0, 0, 0))

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  
                    return text
                elif evento.key == pygame.K_BACKSPACE:  
                    text = text[0:-1]
                else:  
                    text += evento.unicode 
        pantalla.blit(imagen_victoria, (0, 0))
        pantalla.blit(texto_puntaje, (250, 220)) 
        pantalla.blit(texto_titulo, (250, 270))
        
        pygame.draw.rect(pantalla, color, input_box, 2)
        texto_nombre = fuente.render(text, True, (0, 0, 0))
        pantalla.blit(texto_nombre, (input_box.x + 5, input_box.y + 5))

        pygame.display.flip()  
        


def poner_naves(matriz:list, naves:list)->list:
    """
    Funcion :Coloca las naves en un tablero representado por una matriz

    Parámetros: Recibe la matriz  que representa el tablero de juego y las naves que es una lista de tuplas con los datos (nombre , tamnanio y cantidad)
          
    Retorna:Una lista de listas con las coordenadas de las naves colocadas en el tablero

    """
    tamano_matriz = len(matriz)  
    coordenadas_naves = []  

    for naves,largo, cantidad in naves:
        for _ in range(cantidad): #--- pone la nave la cantidad de veces indicada ---
            colocada = False  # ---bandera para saber si esta puesta o no la nave ---
            while not colocada:
                orientacion = random.choice(["horizontal", "vertical"])  
                fila = random.randint(0, tamano_matriz - 1) # --- selecciona aleatoriamente una fila
                columna = random.randint(0, tamano_matriz - 1) 

                # --- en horizontal ---
                if orientacion == "horizontal" and columna + largo <= tamano_matriz: # ---verifica si entra la nave --
                    espacio_libre = True  
                    for i in range(largo):
                        if matriz[fila][columna + i] != 0: # --- verifica si algun casillero esta ocupado ---
                            espacio_libre = False
                            break  
                    #---si hay espacio libre coloca la nave ---
                    if espacio_libre:  
                        for i in range(largo):
                            matriz[fila][columna + i] = 1  #--- Marca las casillas ocupadas por la nave ---   
                        coordenadas_naves.append([(fila, columna + i) for i in range(largo)]) # --- agrega las coordenadas a la lista y para cada valor de i calcula la columna
                        colocada = True                                                       #     y genera las posiciones horizontales  ---       
                      
                
                # --- en vertical ---
                elif orientacion == "vertical" and fila + largo <= tamano_matriz:
                    espacio_libre = True  
                    for i in range(largo):
                        if matriz[fila + i][columna] != 0: 
                            espacio_libre = False
                            break  

                    if espacio_libre: 
                        for i in range(largo):
                            matriz[fila + i][columna] = 1                        
                        coordenadas_naves.append([(fila + i, columna) for i in range(largo)])
                        colocada = True 
    return coordenadas_naves  


def dibujar_tablero(matriz: list, intentos: list, tamano_matriz: int) -> None:
    """
    Función: Dibuja un tablero de juego en la pantalla de Pygame con una imagen que cubre todo el tablero.

    Parámetros:
        - matriz: Una matriz que representa el tablero de juego.
        - intentos: Una segunda matriz de igual tamaño que la primera donde cada celda contiene 1, 0 o -1.
        - tamano_matriz: El tamaño del tablero de juego.
        
    Retorno: None.
    """
    tamano_celda = min(ANCHO, ALTO) // tamano_matriz

    # Cargar y ajustar la imagen para cubrir el tablero completo
    imagen_tablero = pygame.image.load("imagenes/fondo juego.png")
    imagen_tablero = pygame.transform.scale(imagen_tablero, (800,600))

    # Dibujar la imagen del tablero
    pantalla.blit(imagen_tablero, (0, 0))

    # Dibujar las celdas con bordes y marcas (intentos)
    for fila in range(tamano_matriz):
        for columna in range(tamano_matriz):
            x = columna * tamano_celda
            y = fila * tamano_celda

            # Dibujar el borde negro de cada celda
            pygame.draw.rect(pantalla, NEGRO, (x, y, tamano_celda, tamano_celda), 1)

            if intentos[fila][columna] == 1:  # Si hay un disparo acertado
                # Dibujar una X roja
                    pygame.draw.line(pantalla, (255, 0, 0), (x, y), (x + tamano_celda, y + tamano_celda), 3)
                    pygame.draw.line(pantalla, (255, 0, 0), (x + tamano_celda, y), (x, y + tamano_celda), 3)
            elif intentos[fila][columna] == -1:  # Si hay un disparo fallido
                # Dibujar un círculo azul
                centro = (x + tamano_celda // 2, y + tamano_celda // 2)
                pygame.draw.circle(pantalla, (0, 0, 255), centro, tamano_celda // 3, 0)





def mostrar_pantalla_puntajes(pantalla:pygame.surface)->None:
    """
    Funcion : Muestra una pantalla con los 5 puntajes más altos del juego

    Parámetros: No recibe parámetros

    Retorna: No retorna ningún valor
    """

    corriendo = True
    fondo = pygame.transform.scale(pygame.image.load('imagenes/fondo2.1.png'), (ANCHO, ALTO))
    puntajes = []

    while corriendo:
        pantalla.blit(fondo, (0, 0))
        mostrar_texto("Puntajes", NEGRO, 330, 30)
        with open("puntajes.txt", "a+") as archivo:  # --- Abre el archivo de puntajes en modo lectura/escritura, creando el archivo si no existe ---  
            archivo.seek(0) 
        for linea in archivo.readlines():  # Itera sobre cada línea del archivo
            linea = linea.strip()  # Elimina los espacios en blanco iniciales y finales
            if linea:  # Comprueba que la línea no esté vacía
                puntajes.append(linea.split(","))  # Divide la línea por comas y la agrega a la lista
            puntajes.sort(key=lambda x: x[1], reverse=True) # --- Ordena la lista de puntajes de mayor a menor, segun el segundo elemento  --


        # Crear fondo semitransparente para los puntajes
        fondo_puntajes = pygame.Surface((265, 100))  # Superficie que abarca el área de los puntajes
        fondo_puntajes.set_alpha(180)  # Establecer la transparencia
        fondo_puntajes.fill((100, 150, 230))  # Color de fondo (blanco suave)

        # Dibujar el fondo semitransparente
        pantalla.blit(fondo_puntajes, (265, 140))


        for i in range(min(3, len(puntajes))):
            nombre, puntos = puntajes[i]
            mostrar_texto(f"{i+1}. {nombre}: {puntos} puntos", NEGRO, 275, 150 + i * 30)

       
        for i in range(len(puntajes), 3):
            mostrar_texto(f"{i+1}.      ---------- ", NEGRO, 275, 150 + i * 30)

        # Obtener la posición del mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Verificar si el mouse está sobre el botón "Volver"
        hover_volver = 300 <= mouse_x <= 500 and 360 <= mouse_y <= 410
       
        dibujar_boton("Volver", 300, 360, 200, 50, (135, 206, 235), NEGRO, hover=hover_volver)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 300 <= x <= 500 and 360 <= y <= 410:
                    corriendo = False

        pygame.display.flip()





def crear_matriz(tamano_matriz:int)->list:

    """
    Función: Crea una matriz cuadrada 
    Parámetros: El tamaño de la matriz 
    Retorna: Una matriz 
    """
    matriz = [] 
    for _ in range(tamano_matriz):
        fila = [0] * tamano_matriz # --- crea una fila de elementos , todos iniciados en 0 ---
        matriz.append(fila) # ---agrega la fila a la matriz ---
    return matriz











######################### FUNCIONES AUXILIARES ################################

def mostrar_texto(texto: str, color: tuple, x: int, y: int, centrado: bool = False) -> None:
    """
    Función: Muestra un texto en la pantalla.
    Parámetros:
    texto : El texto a mostrar.
    color: Color del texto en formato RGB.
    x : Posición horizontal del texto.
    y : Posición vertical del texto.
    Retorno: None
    """
    fuente = pygame.font.Font(None, 36)  # Fuente y tamaño
    texto_renderizado = fuente.render(texto, True, color)
    texto_rect = texto_renderizado.get_rect(center=(x, y) if centrado else (0, 0))
    pantalla.blit(texto_renderizado, texto_rect if centrado else (x, y))



def mostrar_puntaje(puntaje: int) -> None:
    """
    Función: Muestra el puntaje en la pantalla.
    Parámetros:El puntaje a mostrar en pantalla.
    Retorno:None
    """
    fuente = pygame.font.SysFont("Arial", 25)  
    texto = fuente.render(f"Puntaje: {puntaje:04d}", True, NEGRO) 
    pantalla.blit(texto, (625, 10)) 



def guardar_puntaje(nombre: str, puntaje: int) -> None:
    """
    Función: Guarda el puntaje en un archivo de texto.
    Parámetros:El nombre del jugador y el puntaje obtenido por el jugador.
    Retorno: None
    """
    with open("puntajes.txt", "a") as archivo:
        archivo.write(f"{nombre},{puntaje}\n")



def agregar_mensaje(mensaje: str) -> None:
    """
    Función: Agrega un mensaje a la lista de mensajes, eliminando el más antiguo si hay más de 5 mensajes.
    Parámetros:El mensaje a agregar a la lista de mensajes.
    Retorno:None
    """
    if len(mensajes) >= 5:
        mensajes.pop(0)  # Elimina el mensaje más antiguo si ya hay 3
    mensajes.append(mensaje)  # Agrega el nuevo mensaje


def mostrar_mensajes() -> None:
    """
    Función: Muestra los mensajes almacenados en la lista de mensajes en la pantalla
    Parámetros: Ninguno
    Retorno: None
    """
    y_pos = 150  
    x_pos = 610  
    fuente_mensajes = pygame.font.SysFont('Arial', 18)  
    for mensaje in mensajes:
        texto_renderizado = fuente_mensajes.render(mensaje, True, 'blue')  
        pantalla.blit(texto_renderizado, (x_pos, y_pos)) 
        y_pos += 20



def boton_presionado(x: int, y: int, ancho: int, alto: int, mouse_x: int, mouse_y: int) -> bool:
    """
    Función: Verifica si un clic de ratón ha ocurrido dentro de las coordenadas de un botón
    Parámetros:
    x : La coordenada x de la esquina superior izquierda del botón.
    y : La coordenada y de la esquina superior izquierda del botón.
    ancho : El ancho del botón.
    alto : El alto del botón.
    mouse_x : La coordenada x del clic del ratón.
    mouse_y : La coordenada y del clic del ratón.
    Retorno:bool: Devuelve True si el clic del ratón está dentro de los límites del botón, de lo contrario False
    """
    return x < mouse_x < x + ancho and y < mouse_y < y + alto


def dibujar_boton(texto: str, x: int, y: int, ancho: int, alto: int, color_base: tuple, color_texto: tuple, hover: bool = False, color_borde: tuple = (0, 0, 0), radio_bordes: int = 8) -> None:
    """
    Dibuja un botón redondeado con borde y texto, y opcionalmente cambia de color si el mouse está sobre él.
    
    Parámetros:
    texto (: Texto a mostrar en el botón.
    x, y : Coordenadas de la esquina superior izquierda del botón.
    ancho, alto: Dimensiones del botón.
    color_base: Color principal del botón.
    color_texto: Color del texto.
    hover : Indica si el botón está en estado "hover" (cursor encima).
    color_borde : Color del borde del botón.
    radio_bordes: Radio de los bordes redondeados.
    """
   
    if hover:
      
        color_satinado = (min(color_base[0] + 20, 255),  
                          min(color_base[1] + 20, 255),  
                          min(color_base[2] + 20, 255))  
        color_base = color_satinado

    # --- dibuja el fondo del boton ---
    pygame.draw.rect(pantalla, color_borde, (x - 1, y - 1, ancho + 6, alto + 6), border_radius=radio_bordes)

    # ---dibuja el rectángulo del botón con bordes redondeados---
    pygame.draw.rect(pantalla, color_base, (x, y, ancho, alto), border_radius=radio_bordes)

    fuente = pygame.font.Font(None, 36)  
    texto_superficie = fuente.render(texto, True, color_texto)
    texto_rect = texto_superficie.get_rect(center=(x + ancho // 2, y + alto // 2)) # --- obtiene un rectangilo con el tamanio del texto y centra el texto ----
    pantalla.blit(texto_superficie, texto_rect)
