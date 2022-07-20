from typing import Text
import pygame  
import os
import pygame, sys

from pygame import key
from pygame import draw
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, QUIT
from pygame.sprite import collide_rect 
## Se importara los elementos desde la libreria "Pygame" donde tendremos los recursos necesarios para realizar el videojuego.

##Definimos el tamaño de la pantalla del juego.
WIDTH= 900
HEIGHT= 500
WIN= pygame.display.set_mode((WIDTH,HEIGHT))  #Desde la libreria se llama la siguiente funcion para ejecutar la pantalla.

pygame.font.init() # "font" y "mixer", nos da la posibilidad de agregar sonido y colocar una fuente de texto.
pygame.mixer.init()
##Le pondremos un titulo a nuestro juego, con la siguiente funcion.
pygame.display.set_caption("Maquinas de Guerra")

##Se realiza variables de diferentes colores con el metodo de RGB.Las secuencias de numeros, nos dara un color particular. Dichos colores nos sera de utilidad para mas adelante.

WHITE= (255,255,255)
BLACK= (0,0,0)
RED= (255,0,0)
CRIMSON= (220,20,60)
STEELBLUE=(70,130,180)
SBLUE= (135,206,235)
GREY= (128,128,128)
CIAN= (46,255,157)
LIME= (0,255,0)

VIDANAV= pygame.font.SysFont("bodoni",30) ##Se establece la fuente del indicador de vida de cada jugador.
GANADOR= pygame.font.Font("Objetos\GOS.ttf",50) ##Se establece la fuente del indicador de partida ganada.

MenuTitulo= pygame.font.Font("Objetos\GOS.ttf",45) ## Se establece la fuente del Menu (Titulo de juego).
Menuopc= pygame.font.Font("Objetos\GOS.ttf",20) ##Se establece la fuente de las opciones del menu

#Las siguientes variables seran para introducir el sonido de las armas de nuestras naves.
SONIDOLASER1= pygame.mixer.Sound("Objetos\Laser1.wav") 
SONIDOLASER2= pygame.mixer.Sound("Objetos\Laser1.wav")
SONIDOMISIL1= pygame.mixer.Sound("Objetos\Mis1.wav")
SONIDOMISIL2= pygame.mixer.Sound("Objetos\Mis2.wav")
BORDER= pygame.Rect(WIDTH/2,0,0.5,HEIGHT)  #Se establece un rectangulo que dividira el espacio de ambos jugadores.

pygame.mixer.music.load("Objetos\Heroic Intrusion.wav")  ##Se le agrega musica de fondo.
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

    




FPS= 60 ##Se establece la velocidad a la que correra el juego.
VEL= 5  ##Velocidad en la que se movera la nave de cada jugador.
PROYEC = 4 ##Se establece la cantidad de proyectiles para cada jugador
VEL_PROYEC= 12 ##Velocidad de los proyectiles lanzados.
PROYEC2= 1 #Proyectiles secundarios.
VEL_PROYECS= 8 #Velocidad de misil.

#En las siguientes variables, guardaremos la imagen de fondo, la funcion "pygame.image.load" y la funcion "os.path.join" buscaran entre los ficheros la imagen a utilizar. Con la funcion "pygame.transform.scale" le daremos el tamaño de la imagen.
SPACE= pygame.transform.scale(pygame.image.load(os.path.join("Objetos\stars2.jpg")),(WIDTH,HEIGHT))
SPACEMENU= pygame.transform.scale(pygame.image.load(os.path.join("Objetos\SpaceMenu.png")),(WIDTH,HEIGHT))


#Las siguientes variables seran el tamaño de las naves y laser de cada jugador.
SPACESHIP_WIDTH,SPACESHIP_HEIGTH= 70,70
LASER_WIDTH,LASER_HEIGTH= 42,20
LASER_WIDTH2,LASER_HEIGTH2= 60,30
##Se crea un nuevo evento, en este caso sera el impacto del proyectil en las naves.
NAVE1impact= pygame.USEREVENT + 1 
NAVE2impact= pygame.USEREVENT + 2
NAVE1impactS= pygame.USEREVENT +3
NAVE2impactS= pygame.USEREVENT +4

#Se introduce las naves en pantalla..
SPACESHIP1_IMAGE= pygame.image.load(os.path.join("Objetos\spaceship.png")) 
SPACESHIP1= pygame.transform.rotate(pygame.transform.scale(SPACESHIP1_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGTH)),270) 
SPACESHIP2_IMAGE= pygame.image.load(os.path.join("Objetos\spaceships2.png"))
SPACESHIP2= pygame.transform.rotate(pygame.transform.scale(SPACESHIP2_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGTH)),270)

#Se introduciran las imagenes de los proyectiles de cada cada jugador.
LASER1_IMAGE= pygame.image.load(os.path.join("Objetos\Blue.png"))
LASER1= pygame.transform.rotate(pygame.transform.scale(LASER1_IMAGE,(LASER_WIDTH,LASER_HEIGTH)),0)
LASER2_IMAGE= pygame.image.load(os.path.join("Objetos\Red.png"))
LASER2= pygame.transform.rotate(pygame.transform.scale(LASER2_IMAGE,(LASER_WIDTH,LASER_HEIGTH)),180)
MIS1_IMAGE= pygame.image.load(os.path.join("Objetos\BB.png"))
MIS1= pygame.transform.rotate(pygame.transform.scale(MIS1_IMAGE,(LASER_WIDTH2,LASER_HEIGTH2)),0)
MIS2_IMAGE= pygame.image.load(os.path.join("Objetos\BR.png"))
MIS2= pygame.transform.rotate(pygame.transform.scale(MIS2_IMAGE,(LASER_WIDTH2,LASER_HEIGTH2)),180)

##"pygame.transform.rotate" es una funcion que rotara la imagen en los grados que querramos



#La funcion "draw_window" sera de utilidad para actualizar el fondo.
#La funcion "blit" nos permitira ubicar la imagen dentro del cuadro mediante las coordenadas.

def draw_window(yell,red,proy_J1,proy_J2,proyS_J1,proyS_J2,jugador1,jugador2):
     WIN.blit(SPACE,(0,0))
     pygame.draw.rect(WIN,BLACK,BORDER)
     WIN.blit(SPACESHIP1,(yell.x,yell.y))
     WIN.blit(SPACESHIP2,(red.x,red.y))
     
     
     #Las siguientes lineas, nos dara como resultado la barra y el texto de la vida de nuestras naves.
     VID1= VIDANAV.render("Escudo:"+ str(jugador1)+"%",1,CRIMSON)
     pygame.draw.rect(WIN,STEELBLUE,(10, 10,200,15))
     pygame.draw.rect(WIN,SBLUE,(10,10, jugador2 ,15))
     VID2= VIDANAV.render("Escudo:"+ str(jugador2)+"%",1 ,STEELBLUE)
     pygame.draw.rect(WIN,CRIMSON,((WIDTH - 210),10,200,15))
     pygame.draw.rect(WIN,GREY,((WIDTH - 210),10,200 - jugador1 ,15))
     WIN.blit(VID1,(WIDTH - VID1.get_width()-10,30))
     WIN.blit(VID2,(10,30))   

    
     for balas in proy_J1:
         WIN.blit(LASER1,(balas))
     for balas in proy_J2:
         WIN.blit(LASER2,(balas))
     for misil in proyS_J1:
         WIN.blit(MIS1,(misil))
     for misil in proyS_J2:
         WIN.blit(MIS2,(misil))
    
    
     pygame.display.update() 

def jug1_movimiento(keys_press,yell): #Se establece una funcion de movimiento para el jugador n°1
    if keys_press[pygame.K_a] and yell.x - VEL > 0:   #Movimiento a la izquierda
        yell.x -= VEL 
    if keys_press[pygame.K_d] and yell.x + VEL + yell.width < BORDER.x:  #Movimiento a la derecha
        yell.x += VEL
    if keys_press[pygame.K_w] and yell.y - VEL >0: #Movimiento hacia arriba
        yell.y -= VEL
    if keys_press[pygame.K_s] and yell.y + VEL + yell.height < HEIGHT: #Movimiento hacia abajo
        yell.y += VEL
def jug2_movimiento(keys_press,red): #Se establece una funcion de movimiento para el jugador n°2
    if keys_press[pygame.K_RIGHT] and red.x + VEL <= 840: #Movimiento hacia la derecha
        red.x += VEL
    if keys_press[pygame.K_LEFT] and red.x - VEL > BORDER.x: #Movimiento hacia la izquierda
        red.x -= VEL
    if keys_press[pygame.K_UP] and red.y - VEL >0:  #Moviemiento hacia arriba
        red.y -= VEL
    if keys_press[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: #Movimiento hacia abajo.
        red.y += VEL

def proyectiles(proy_J1,proy_j2,yell,red): #Funcion de arma principal para ambos jugadores.                                                     
    for balas in proy_J1:
        balas.x += VEL_PROYEC
        if red.colliderect(balas):                                               
            proy_J1.remove(balas)
            pygame.event.post(pygame.event.Event(NAVE1impact))  ##"pygame.event.EVENT 
                             #Crea un nuevo evento con el tipo Y los atributos dados.
        elif balas.x > WIDTH:#"pygame.event.post",coloca el evento dado al final de la cola deeventos
            proy_J1.remove(balas) #Suele utilizarse para colocar pygame.USEREVENT en la cola. Aunque se puede colocar cualquier tipo de evento
    for balas in proy_j2:
        balas.x -= VEL_PROYEC
        if yell.colliderect(balas):
            proy_j2.remove(balas)
            pygame.event.post(pygame.event.Event(NAVE2impact))
        if balas.x < 0:
            proy_j2.remove(balas)

# La siguiente funcion le correspondera al funcionamiento de las armas secundarias.
def proyectilesS(proyS_J1,proyS_J2,yell,red):
    for misil in proyS_J1:
        misil.x += VEL_PROYECS
        if red.colliderect(misil):
            proyS_J1.remove(misil)
            pygame.event.post(pygame.event.Event(NAVE1impactS))
        elif misil.x > WIDTH:
            proyS_J1.remove(misil)
    for misil in proyS_J2:
        misil.x -= VEL_PROYECS
        if yell.colliderect(misil):
            proyS_J2.remove(misil)
            pygame.event.post(pygame.event.Event(NAVE2impactS))
        if misil.x < 0:
            proyS_J2.remove(misil)


# "draw_vencerdor",sera la funcion que nos dira quien es el ganador del encuentro.
def draw_vencedor(text):
    WINN= GANADOR.render(text,1,STEELBLUE)
    WIN.blit(WINN,(WIDTH/2 - WINN.get_width()/2 , HEIGHT/2 - WINN.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main_menu(): #La siguiente def sera del menu!
    clock= pygame.time.Clock()
    run= True
    while run:
        clock.tick(FPS)
        mx,my= pygame.mouse.get_pos() #Para el menu utilizaremos el mouse, mx y my seran las coordenadas del mouse
   ## La tarea siguiente es elaborar el menu del juego, en donde ubicaremos el titulo,
   # y las opciones.     
        #Al menu, le daremos un fondo de pantalla distinto del fondo del juego.
        WIN.blit((SPACEMENU),(0,0)) 
        Titulo= "Maquinas de Guerra"
        TITLE= MenuTitulo.render(Titulo,1,LIME)
        WIN.blit((TITLE),(150,150))
        opc1= pygame.Rect(360,250,180,40)
        pygame.draw.rect(WIN,BLACK,(360,250,180,40))
        ready= "A la batalla!"
        opc1T= Menuopc.render(ready,1,LIME)
        WIN.blit((opc1T),(370,255))
        if opc1.collidepoint((mx,my)): #Le daremos funcionamiento a nuestras opciones 
            pygame.draw.rect(WIN,BLACK,(360,250,180,40))
            opc1T= Menuopc.render(ready,1,RED)
            WIN.blit((opc1T),(370,255))
            if clickm:
                main()
        opc2= pygame.Rect(360,300,180,40)
        pygame.draw.rect(WIN,BLACK,(360,300,180,40))
        exitt= "Salir"
        opc2T= Menuopc.render(exitt,1,LIME)
        WIN.blit((opc2T),(410,305))
        if opc2.collidepoint((mx,my)):
             pygame.draw.rect(WIN,BLACK,(360,300,180,40))
             opc2T= Menuopc.render(exitt,1,STEELBLUE)
             WIN.blit((opc2T),(410,305))
             if clickm:
                 sys.exit()
        
        clickm= False 
        
        for event in pygame.event.get():
            if event.type == QUIT:
                run= False
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 :
                    clickm= True
            
        pygame.display.update()

def main():
    clock= pygame.time.Clock() 
    run= True ##A la variable "run" se le asignara un atributo "True". Para que el juego funcione hasta que se lo digan.
              # True tendra la funcion de poner en funcionamiento el bucle.
    proy_J1 = [] #En las siguientes listas almacenaremos los proyectiles de cada jugador
    proy_J2 = []
    proyS_J1 = []
    proyS_J2 = []
    ## Las siguientes variables seran la vida de cada jugador.
    jugador1= 200 
    jugador2= 200

    #yell y red, seran las variables de cada nave, le da un cuerpo a las imagenes.
    yell= pygame.Rect(100,200,SPACESHIP_WIDTH,SPACESHIP_HEIGTH) 
    red= pygame.Rect(700,200,SPACESHIP_WIDTH,SPACESHIP_HEIGTH) 
    
    while run:
        clock.tick(FPS) ##Le daremos las veces que se repita el bucle 60 veces por segundo.
         ##pygame.event.get() registrara todos los eventos del usuario en una cola.
        ## Los eventos son las acciones del jugador dentro del juego(presionar determinada tecla,pulsar boton de mouse, etc)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  ##De todos los elementos dentro de la funcion, solo lo compararemos con "pygame.Quit"
                run= False ## Cuando lo encuentre, la variable "run" cambiara a False, abandonando el bucle.
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(proy_J1) < PROYEC:#Control de arma principal (Jugador1)
                    proyec= pygame.Rect(yell.x + yell.width , yell.y + yell.height/2-10,10,5)
                    proy_J1.append(proyec)
                    SONIDOLASER1.play()
                if event.key == pygame.K_LALT and len(proyS_J1) < PROYEC2:   #Control de arma secundaria (Jugado1)
                    proyec2= pygame.Rect(yell.x + yell.width , yell.y + yell.height/2-10,10,5)
                    proyS_J1.append(proyec2)
                    SONIDOMISIL1.play()
                if event.key == pygame.K_RCTRL and len(proy_J2) < PROYEC: #control de arma principal(Jugador2)
                    proyec= pygame.Rect(red.x + red.width- red.width, red.y + red.height/2-10,10,5)
                    proy_J2.append(proyec)
                    SONIDOLASER2.play()
                if event.key == pygame.K_RALT and len(proyS_J2) < PROYEC2: #Control de arma secundaria(Jugador2)
                    proyec2= pygame.Rect(red.x + red.width-60 , red.y + red.height/2-10,10,5)
                    proyS_J2.append(proyec2)
                    SONIDOMISIL2.play()
                if event.key == K_ESCAPE:
                    sys.exit()
            #Le daremos a cada arma un porcentaje de daño. 10 Para el arma principal 30 para la secunaria.
            if event.type == NAVE1impact:
                jugador1 -= 10
            if event.type == NAVE1impactS:
                jugador1 -= 30
            if event.type == NAVE2impact:
                jugador2 -= 10
            if event.type == NAVE2impactS:
                jugador2 -= 30

        WINN= ""  #Cuando alguno de los dos jugadores llega a 0, dira quien es el ganador.
        if jugador1 <= 0:
            WINN= "JUGADOR UNO,HAS VENCIDO!"
        if jugador2 <= 0:
            WINN= "JUGADOR DOS,HAS VENCIDO!"
        if WINN != "":
            draw_vencedor(WINN)
            break
        keys_press= pygame.key.get_pressed()  ##En la variable "keys_press" se "guardara" las teclas que los jugadores aprieten.
        jug1_movimiento(keys_press,yell)  #"jug1_moviento" sera la funcion responsable de los movimientos.
        jug2_movimiento(keys_press,red)   # "jug2_movimiento" sera la funcion responsable de los movimientos.
        proyectiles(proy_J1,proy_J2,yell,red)
        proyectilesS(proyS_J1,proyS_J2,yell,red)   
        draw_window(yell,red,proy_J1,proy_J2,proyS_J1,proyS_J2,jugador1,jugador2)

main_menu()
main()##"main" es llamada para comenzar con el juego.Siempre y cuando el jugador lo decida.


if __name__ == "__main__" : ##Se commprueba si el fichero se llama "main".
    main()
    

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
