import pygame
import sys
import os
import random

# Establecer el directorio de trabajo al directorio donde se encuentran las imágenes
os.chdir(os.path.dirname(os.path.abspath(r"Ten-Candles-Game")))

# Inicializar Pygame
pygame.init()

# Inicializar el módulo de sonido
pygame.mixer.init()

# Cargar el sonido del encendedor
encendedor_sound = pygame.mixer.Sound(r"Ten-Candles-Game\sounds\encendedor.mp3")

# Cargar el sonido de apagar la vela
apagar_sound = pygame.mixer.Sound(r"Ten-Candles-Game\sounds\apagar.mp3")

# Configuración de la pantalla
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("10 Candles Game")

# Cargar imágenes
table_image = pygame.image.load(r"Ten-Candles-Game\objects\mesa2.png")
candle_image = pygame.image.load(r"Ten-Candles-Game\objects\vela.png")

# Escalar la vela
candle_width = 60
candle_height = 120
candle_image = pygame.transform.scale(candle_image, (candle_width, candle_height))

# Crear una fuente para los números
font = pygame.font.Font(None, 36)

# Lista de posiciones para las velas
velas_positions = [
    (240, 430), # Posicion vela n-1
    (305, 405), # Posicion vela n-2
    (375, 390), # Posicion vela n-3
    (440, 380), # Posicion vela n-4
    (505, 370), # Posicion vela n-5
    (570, 370), # Posicion vela n-6
    (635, 380), # Posicion vela n-7
    (700, 390), # Posicion vela n-8
    (765, 405), # Posicion vela n-9
    (825, 430)  # Posicion vela n-10
]

# Lista de estados de las velas (encendidas o apagadas)
candles_lit = [False] * len(velas_positions)

# Cargar imágenes de la animación de la llama
flame_animation_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(os.getcwd(), "Ten-Candles-Game", "flama_animacion", f"flama_{i}.png")), (20, 20)) for i in range(1, 9)
]

# Variables para la animación
flame_animation_delay = 80  # Cambia esto para ajustar la velocidad de la animación
flame_animation_frames = [0] * len(velas_positions)  # Lista de frames independientes para cada vela

# Lista de estados de las velas (encendidas o apagadas) para controlar el sonido
candles_sound_state = [False] * len(velas_positions)

# Cargar la imagen de la portada
portada_image = pygame.image.load(r"Ten-Candles-Game\objects\portada.jpg")
portada_width = 1200
portada_height = 100
portada_image = pygame.transform.scale(portada_image, (portada_width, portada_height))

# Cargar la imagen de la habitación como fondo
habitacion_image = pygame.image.load(r"Ten-Candles-Game\objects\habitacion.jpg")
habitacion_width = 1200
habitacion_height = 900
habitacion_image = pygame.transform.scale(habitacion_image, (habitacion_width, habitacion_height))

# Definir las posiciones iniciales de la mesa
table_x = 120
table_y = 440  # Ajustar la posición vertical de la mesa aquí

# Cambiar el tamaño de la mesa al 300%
table_width = 900
table_height = 600
table_image = pygame.transform.scale(table_image, (table_width, table_height))

# Números para colocar en las velas
numeros_velas = list(range(1, 11))

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Detectar clic en una vela
            for i, (candle_x, candle_y) in enumerate(velas_positions):
                if candle_x < event.pos[0] < candle_x + candle_width and \
                   candle_y < event.pos[1] < candle_y + candle_height:
                    # Verificar si la vela está apagada antes de encenderla
                    if not candles_lit[i]:
                        # Reproducir el sonido del encendedor
                        encendedor_sound.play()
                    candles_lit[i] = not candles_lit[i]
                    candles_sound_state[i] = candles_lit[i]
                    
                    # Generar un número aleatorio entre 1 y 10
                    random_number = random.randint(1, 10)
                    # Si el número es 1, reproducir el sonido de apagar la vela
                    if random_number == 1 and not candles_lit[i]:
                        apagar_sound.play()

    # Limpiar la pantalla
    screen.fill((0, 0, 0))

    # Dibujar la imagen de la habitación como fondo (detras de la mesa y las velas)
    screen.blit(habitacion_image, (0, 0))

    # Dibujar la imagen de la portada (imagen estática)
    screen.blit(portada_image, (0, 0))

    # Dibujar la mesa
    screen.blit(table_image, (table_x, table_y))

    # Dibujar las velas apagadas o encendidas según el estado y colocar los números en el centro
    for i, (candle_x, candle_y) in enumerate(velas_positions):
        screen.blit(candle_image, (candle_x, candle_y))
        if candles_lit[i]:
            # Calcular la posición de la llama encima de la vela
            flame_x = candle_x + candle_width // 2 - 10
            flame_y = candle_y - 20
            # Cambiar la imagen de la llama para la animación
            screen.blit(flame_animation_images[flame_animation_frames[i]], (flame_x, flame_y))
            flame_animation_frames[i] = (flame_animation_frames[i] + 1) % len(flame_animation_images)
        
        # Colocar el número en el centro de la vela
        numero_text = font.render(str(numeros_velas[i]), True, (255, 255, 255))
        numero_rect = numero_text.get_rect(center=(candle_x + candle_width // 2, candle_y + candle_height // 2))
        screen.blit(numero_text, numero_rect)
        
        # Verificar si la vela está apagada y si se debe restablecer el sonido
        if not candles_lit[i] and candles_sound_state[i]:
            candles_sound_state[i] = False

    # Actualizar la pantalla
    pygame.display.flip()

    # Control de velocidad de la animación
    pygame.time.delay(flame_animation_delay)

# Salir del juego
pygame.quit()
sys.exit()
