import pygame, sys, random, requests, datetime, pygame_textinput
from pygame import *
from random import *

blanco = (255,255,255)
gris = (100,100,100)
rojo = (255,0,0)
verde = (0,255,0)

listaSuelos = []
listaNubes = []
listaCactus = []
listaPajaros = []

class dino(pygame.sprite.Sprite):
    def __init__(self, tiempo):
        pygame.sprite.Sprite.__init__(self)
        self.dino= pygame.image.load("imagenesss/juegoDINO/dino.png")
        self.dino1= pygame.image.load("imagenesss/juegoDINO/dino1.png")
        self.dino2= pygame.image.load("imagenesss/juegoDINO/dino2.png")
        self.dinoM = pygame.image.load("imagenesss/juegoDINO/dinoM.png")
        self.dinoA1 = pygame.image.load("imagenesss/juegoDINO/dinoA1.png")
        self.dinoA2 = pygame.image.load("imagenesss/juegoDINO/dinoA2.png")
        self.dibujo = self.dino
        self.rect = self.dino.get_rect()
        self.rect.centerx = 150
        self.rect.centery = 300
        self.mask = pygame.mask.from_surface(self.dibujo)
        self.lista = [self.dino1, self.dino2]
        self.listaA = [self.dinoA1, self.dinoA2]
        self.posicion = 0
        self.agachado = False
        self.tiempoCambio = tiempo

        self.tiempoSalto = 0
        self.tiempoPreSalto = 0
        self.velocidadSalto = 110
        self.gravedad = 30
        self.aire=False
        self.zona = 0

        self.velocidadJuego = 10
        self.muerto = False

        self.listaBalas = []

    def disparar(self):
        rayo = bala(self.rect.centery)
        self.listaBalas.append(rayo)

    def animacion(self, superficie,tiempo):
        if self.muerto == False:
            if self.aire == False:
                if self.agachado == False:
                    self.dibujo = self.lista[self.posicion]
                    self.rect.centery = 300
                else:
                    self.dibujo = self.listaA[self.posicion]
                    self.rect.centery = 340
            else:
                self.dibujo = self.dino
        else:
            self.dibujo = self.dinoM

        if tiempo == self.tiempoCambio:
            self.posicion += 1
            self.tiempoCambio += 1
            if self.posicion == 2:
                self.posicion = 0

        superficie.blit(self.dibujo, self.rect)
        self.mask = pygame.mask.from_surface(self.dibujo)

    def salto(self, tiempo):
        self.aire = True
        self.rect.centery = 290
        self.tiempoPreSalto = tiempo
        self.zona = 1

    def fisica(self, tiempo):
        if self.aire == True:
            self.tiempoSalto = tiempo - self.tiempoPreSalto
            if self.muerto == False:
                self.rect.centery = 300 - (self.velocidadSalto * self.tiempoSalto) + (0.5 * self.gravedad * self.tiempoSalto * self.tiempoSalto)
                if self.rect.centery < 124:
                    self.zona = 2
                if self.rect.centery > 300:
                    self.aire = False
                if self.agachado == True:
                    self.gravedad = 35
                else:
                    self.gravedad = 30
        else:
            if self.agachado == False:
                self.rect.centery = 300
            self.tiempoSalto = 0
            self.zona = 0

class bala (pygame.sprite.Sprite):
    def __init__(self,y):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagenesss/juegoDINO/rayo.png")
        self.rect = self.imagen.get_rect()
        self.mask = pygame.mask.from_surface(self.imagen)
        self.rect.centery = y
        self.rect.centerx = 200
        self.velocidad = 15
        self.offset = (0, 0)
    def movimiento(self,ventana):
        ventana.blit(self.imagen,self.rect)
        self.rect.centerx += self.velocidad

class subsuelo(pygame.sprite.Sprite):
    def __init__(self,x):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagenesss/juegoDINO/suelo.png")
        self.rect=self.imagen.get_rect()
        self.rect.left=x
        self.rect.top=320
        self.compi = False

    def dibujar(self, superficie):
        superficie.blit(self.imagen,self.rect)

    def movimiento(self, velocidad):
        self.rect.left -= velocidad

class cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagenesss/juegoDINO/nube.png")
        self.rect = self.imagen.get_rect()
        self.rect.centerx = 850
        self.rect.centery = randint(80,220)

    def dibujar(self,superficie):
        superficie.blit(self.imagen,self.rect)

    def movimiento(self, velocidad):
        self.rect.centerx -= velocidad

class trampa(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.cactusP1 = pygame.image.load("imagenesss/juegoDINO/cactusP1.png")
        self.cactusP2 = pygame.image.load("imagenesss/juegoDINO/cactusP2.png")
        self.cactusP3 = pygame.image.load("imagenesss/juegoDINO/cactusP3.png")
        self.cactusG1 = pygame.image.load("imagenesss/juegoDINO/cactusG1.png")
        self.cactusG2 = pygame.image.load("imagenesss/juegoDINO/cactusG2.png")
        self.cactusG3 = pygame.image.load("imagenesss/juegoDINO/cactusG3.png")
        self.aleatorio = randint(1,10)
        if self.aleatorio == 1:
            self.imagen = self.cactusP1
            self.posy = 310
        elif self.aleatorio == 2:
            self.imagen = self.cactusP1
            self.posy = 310
        elif self.aleatorio == 3:
            self.imagen = self.cactusG1
            self.posy = 300
        elif self.aleatorio == 4:
            self.imagen = self.cactusG1
            self.posy = 300
        elif self.aleatorio == 5:
            self.imagen = self.cactusP2
            self.posy = 310
        elif self.aleatorio == 6:
            self.imagen = self.cactusP2
            self.posy = 310
        elif self.aleatorio == 7:
            self.imagen = self.cactusG2
            self.posy = 300
        elif self.aleatorio == 8:
            self.imagen = self.cactusG2
            self.posy = 300
        elif self.aleatorio == 9:
            self.imagen = self.cactusP3
            self.posy = 310
        else:
            self.imagen = self.cactusG3
            self.posy = 300
        self.rect = self.imagen.get_rect()
        self.rect.centery = self.posy
        self.rect.centerx = 850
        self.offset = (0,0)

    def dibujar(self, superficie):
        self.mask = pygame.mask.from_surface(self.imagen)
        superficie.blit(self.imagen, self.rect)

    def movimiento(self, velocidad):
        self.rect.centerx -= velocidad

class ptera(pygame.sprite.Sprite):
    def __init__(self, tiempo):
        pygame.sprite.Sprite.__init__(self)
        self.pajaro1 = pygame.image.load("imagenesss/juegoDINO/pajaro1.png")
        self.pajaro2 = pygame.image.load("imagenesss/juegoDINO/pajaro2.png")
        self.listaImg = [self.pajaro1, self.pajaro2]
        self.posicion = 0
        self.tiempoCambio = int(tiempo)
        self.rect = self.pajaro1.get_rect()
        self.rect.centery = choice([280,240,200,150])
        self.rect.centerx = 850
        self.bonito = choice([-1,0,1])
        self.fin = False
        self.offset = (0,0)

    def aleteo(self,superficie, tiempo, gameover):
        superficie.blit(self.listaImg[self.posicion], self.rect)
        self.mask = pygame.mask.from_surface(self.listaImg[self.posicion])
        if gameover == False:
            if int(tiempo) == self.tiempoCambio:
                self.posicion += 1
                self.tiempoCambio += 2
                if self.posicion == 2:
                    self.posicion = 0
        else:
            self.fin = True
    def movimiento(self, velocidad):
        if self.fin is False:
            self.rect.centerx -= (velocidad + self.bonito)

class boton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagenesss/juegoDINO/boton.png")

        self.rect = self.imagen.get_rect()
        self.rect.centery = 200
        self.rect.centerx = 400

    def dibujar(self, superficie):
        superficie.blit(self.imagen, self.rect)

class btnCambiarSkin(pygame.sprite.Sprite):
    def __init__(self,fuente):
        pygame.sprite.Sprite.__init__(self)
        self.fondo = pygame.image.load("imagenesss/juegoDINO/marcoGris.png")
        self.rect = self.fondo.get_rect()
        self.rect.left = 45
        self.rect.top = -35
        self.texto = fuente.render("cambiar skin",1,gris)
    def dibujar(self,ventana):
        ventana.blit(self.fondo,self.rect)
        ventana.blit(self.texto,(70,20))

class btnCambiarUsuario(pygame.sprite.Sprite):
    def __init__(self,fuente):
        pygame.sprite.Sprite.__init__(self)
        self.fondo = pygame.image.load("imagenesss/juegoDINO/marcoGris.png")
        self.rect = self.fondo.get_rect()
        self.rect.left = 45
        self.rect.top = 55
        self.texto = fuente.render("cambiar user",1,gris)
    def dibujar(self,ventana):
        ventana.blit(self.fondo,self.rect)
        ventana.blit(self.texto,(70,110))

class skins(pygame.sprite.Sprite):
    def __init__(self, numero):
        pygame.sprite.Sprite.__init__(self)
        self.nada = pygame.image.load("imagenesss/juegoDINO/nada.png")
        self.santa = pygame.image.load("imagenesss/juegoDINO/santa.png")
        self.globos = pygame.image.load("imagenesss/juegoDINO/globos.png")
        self.pipa = pygame.transform.flip(pygame.image.load("imagenesss/juegoDINO/pipa.png"), True, False)
        self.lista = [self.nada, self.santa, self.globos, self.pipa]
        self.imagen =self.lista[numero]
        self.rect = self.imagen.get_rect()
        self.numero = numero

    def dibujar(self,ventana,x,y):
        self.rect.centerx = x
        self.rect.centery = y
        ventana.blit(self.imagen, self.rect)

class candado(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("imagenesss/juegoDINO/candado.png")
    def dibujar(self,ventana,x,y):
        ventana.blit(self.imagen,(x,y))

class marco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.naranja = pygame.image.load("imagenesss/juegoDINO/marcoN.png")
        self.amarillo = pygame.image.load("imagenesss/juegoDINO/marcoA.png")
        self.lista = [self.naranja,self.amarillo]
    def dibujar(self,ventana,numero,x,y):
        ventana.blit(self.lista[numero],(x,y))

def nuevoSuelo(x):
    terreno=subsuelo(x)
    listaSuelos.append(terreno)

def nuevaNube():
    nube = cloud()
    listaNubes.append(nube)

def nuevoCactus():
    cactus = trampa()
    listaCactus.append(cactus)

def nuevoPajaro(tiempo):
    pajaro = ptera(tiempo)
    listaPajaros.append(pajaro)

def registrar(puntos, usuario):
    if puntos > 20:
        fecha = datetime.datetime.today()
        accion = 'INSERT INTO `records_dinosaurio`(`fecha`, `usuario`, `puntos`) VALUES ("' + str(fecha) + '","' + usuario + '","' + str(puntos) + '")'
        requests.get('http://espidominio.atwebpages.com/conectar.php?orden=' + accion)

def obtenerRecord(usuario):
    orden = 'SELECT MAX(`puntos`) AS max FROM `records_dinosaurio` WHERE `usuario` = "' + usuario + '"'
    consulta = requests.get('http://espidominio.atwebpages.com/record.php?orden=' + orden)
    return consulta.text

def obtenerRecordGlobal():
    orden = 'SELECT MAX(`puntos`) AS max FROM `records_dinosaurio` WHERE 1'
    orden2 = 'SELECT `usuario` FROM `records_dinosaurio` WHERE `puntos` = (SELECT MAX(`puntos`) FROM `records_dinosaurio`)'
    consulta = requests.get('http://espidominio.atwebpages.com/record2.php?orden=' + orden + '&orden2=' + orden2)
    return consulta.text

def obtenerSkins(usuario):
    orden = 'SELECT `numero` FROM `skins` WHERE `usuario` = "' + usuario + '"'
    orden2 = 'INSERT INTO `skins` (`usuario`,`numero`) VALUES ("' + usuario + '","0")'
    consultaS = requests.get('http://espidominio.atwebpages.com/skins.php?orden=' + orden +'&orden2='+ orden2)
    return consultaS.text

def actualizarSkins(usuario, puntuacion):
    if puntuacion > 250:
        numero = 1
        if puntuacion > 500:
            numero = 2
            if puntuacion > 1000:
                numero = 3
    else:
        numero = 0
    orden = 'UPDATE `skins` SET `numero`=' + str(numero) + ' WHERE `usuario` = "' + usuario + '"'
    requests.get('http://espidominio.atwebpages.com/conectar.php?orden=' + orden)

def seleccionarSkins(numero,record,usuario):
    pygame.init()
    ventana = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Seleccione skin")
    fuente = pygame.font.Font("fuentes/SuperMario256.ttf", 30)
    texto = fuente.render("skins", 1, gris,(200,200,200))
    textoRecord = fuente.render("Record de " + usuario + ": " + str(record),1,gris)
    seleccionado = False
    rex = dino(0)
    rex.rect.centerx = 100
    rex.rect.centery = 250
    santa = skins(1)
    globos = skins(2)
    arma = skins(3)
    seleccion = 0
    c1 = candado()
    c2 = candado()
    c3 = candado()
    cuadro = marco()
    posicion = 0
    disponible = True
    while seleccionado == False:
        ventana.fill(blanco)
        ventana.blit(rex.dino,rex.rect)
        ventana.blit(texto, (150,25))
        ventana.blit(textoRecord,(300,25))
        santa.dibujar(ventana,300,250)
        globos.dibujar(ventana,500,250)
        arma.dibujar(ventana,700,250)
        events = pygame.event.get()
        if numero < 1:
            c1.dibujar(ventana,300,250)
            txt1 = fuente.render("250p",0,rojo)
        else:
            txt1 = fuente.render("250p", 0, verde)
        if numero < 2:
            c2.dibujar(ventana,500,250)
            txt2 = fuente.render("500p", 0, rojo)
        else:
            txt2 = fuente.render("500p", 0, verde)
        if numero < 3:
            c3.dibujar(ventana,700,250)
            txt3 = fuente.render("1000p", 0, rojo)
        else:
            txt3 = fuente.render("1000p", 0, verde)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_RIGHT:
                    if posicion < 3:
                        posicion += 1
                if event.key == pygame.K_LEFT:
                    if posicion > 0:
                        posicion -= 1
                if event.key == pygame.K_RETURN:
                    if disponible == True:
                        seleccionado = True
        if posicion == 0:
            cuadro.dibujar(ventana,1,50,200)
            seleccion = 0
            disponible = True
        elif posicion == 1:
            if numero > 0:
                cuadro.dibujar(ventana, 1, 250, 200)
                seleccion = 1
                disponible = True
            else:
                cuadro.dibujar(ventana, 0, 250, 200)
                disponible = False
        elif posicion == 2:
            if numero > 1:
                cuadro.dibujar(ventana, 1, 450, 200)
                seleccion = 2
                disponible = True
            else:
                cuadro.dibujar(ventana, 0, 450, 200)
                disponible = False
        elif posicion == 3:
            if numero > 2:
                cuadro.dibujar(ventana, 1, 650, 200)
                seleccion = 3
                disponible = True
            else:
                cuadro.dibujar(ventana, 0, 650, 200)
                disponible = False
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if santa.rect.collidepoint(pygame.mouse.get_pos()):
                if numero > 0:
                    seleccion = 1
                    seleccionado = True
            if globos.rect.collidepoint(pygame.mouse.get_pos()):
                if numero > 1:
                    seleccion = 2
                    seleccionado = True
            if arma.rect.collidepoint(pygame.mouse.get_pos()):
                if numero > 2:
                    seleccion = 3
                    seleccionado = True
            if rex.rect.collidepoint(pygame.mouse.get_pos()):
                seleccion = 0
                seleccionado = True
        ventana.blit(txt1,(300,280))
        ventana.blit(txt2,(500,280))
        ventana.blit(txt3,(700,280))
        pygame.display.update()
    return seleccion

def NoInternet():
    pygame.init()
    ventana=pygame.display.set_mode((520,520))
    pygame.display.set_caption("NO HAY CONEXION")
    imagen = pygame.image.load("imagenesss/juegoDINO/noWIFI.png")
    while True:
        ventana.fill(blanco)
        ventana.blit(imagen,(6,6))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def inicio():
    pygame.init()
    ventana = pygame.display.set_mode((600, 50))
    pygame.display.set_caption("Usuario")
    fuente = pygame.font.Font("fuentes/SuperMario256.ttf", 30)
    texto = pygame_textinput.TextInput(font_family="fuentes/SuperMario256.ttf")
    ready = False
    usuario = ""
    while ready == False:
        ventana.fill(blanco)
        ayuda = fuente.render("Usuario: ", 1, gris)
        ventana.blit(ayuda, (10, 10))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if texto.update(events):
            usuario = texto.get_text()
            ready = True
        ventana.blit(texto.get_surface(), (170, 10))
        pygame.display.update()
    return usuario

def juego(userInicio, numeroSkinInicio):
    pygame.init()
    ventana = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("DINOBRO")
    nuevoTiempo = 0
    fuente = pygame.font.Font("fuentes/SuperMario256.ttf", 30)
    botonCambiarSkin = btnCambiarSkin(fuente)
    botonCambiarUser = btnCambiarUsuario(fuente)
    clock = pygame.time.Clock()
    numeroSkin = numeroSkinInicio
    usuario = userInicio

    while True:
        record = int(obtenerRecord(usuario))
        actualizarSkins(usuario, record)
        tiempo = int(pygame.time.get_ticks() / 100)
        nuevoTiempo = int(tiempo)
        rex = dino(tiempo)
        skin = skins(numeroSkin)
        suelo1 = subsuelo(0)
        reset = boton()
        listaSuelos.append(suelo1)
        masRapido = pygame.USEREVENT
        aparecerNube = pygame.USEREVENT + 1
        aparecerCactus = pygame.USEREVENT + 2
        pygame.time.set_timer(masRapido, 15000)
        tempNube = False
        tempCactus = False
        gameover = False
        reinicio = False
        puntuacion = 0
        conectado = False
        armado = True if numeroSkin == 3 else False
        if armado:
            skin.imagen = pygame.transform.scale(skin.pipa,(30,21))

        while True:
            ventana.fill(blanco)
            tiempo = (pygame.time.get_ticks() / 100)

            if gameover == False:
                if tempNube == False:
                    pygame.time.set_timer(aparecerNube, randint(1200,3000))
                    tempNube = True
                if tempCactus == False:
                    pygame.time.set_timer(aparecerCactus, randint(700, 1900))
                    tempCactus = True
                puntuacion = int(((int(tiempo) - nuevoTiempo)/10) * rex.velocidadJuego)

            if gameover == True:
                rex.muerto = True
                rex.velocidadJuego = 0
                reset.dibujar(ventana)
                botonCambiarSkin.dibujar(ventana)
                botonCambiarUser.dibujar(ventana)
                nuevoTiempo = int(tiempo)
                if conectado == False:
                    registrar(puntuacion, usuario)
                    record = int(obtenerRecord(usuario))
                    actualizarSkins(usuario, record)
                    conectado=True
                if pygame.mouse.get_pressed() == (1,0,0):
                    if reset.rect.collidepoint(pygame.mouse.get_pos()):
                        reinicio = True
                        for suelo in listaSuelos:
                            listaSuelos.remove(suelo)
                    if botonCambiarSkin.rect.collidepoint(pygame.mouse.get_pos()):
                        numeroSkin = seleccionarSkins(int(obtenerSkins(usuario)),record,usuario)
                        reinicio = True
                        for suelo in listaSuelos:
                            listaSuelos.remove(suelo)
                    if botonCambiarUser.rect.collidepoint(pygame.mouse.get_pos()):
                        usuario = inicio()
                        record = int(obtenerRecord(usuario))
                        numeroSkin = seleccionarSkins(int(obtenerSkins(usuario)),record,usuario)
                        reinicio = True
                        for suelo in listaSuelos:
                            listaSuelos.remove(suelo)

            marcador = fuente.render(str(puntuacion),1,gris)
            ventana.blit(marcador,(650,20))
            lblRecord = fuente.render("Record: " + str(record), 1, gris)
            ventana.blit(lblRecord,(370,20))
            dificultad = fuente.render("Dificultad: " + str(rex.velocidadJuego-9),1,gris)
            if gameover == False:
                ventana.blit(dificultad,(70,20))
            else:
                lblTopRecord = fuente.render("Top Record: " ,1,gris)
                lblTopRecord2 = fuente.render(str(obtenerRecordGlobal()),1,gris)
                ventana.blit(lblTopRecord,(370,100))
                ventana.blit(lblTopRecord2,(370, 125))
            keys = pygame.key.get_pressed()
            if keys[K_DOWN]:
                rex.agachado = True
            else:
                rex.agachado = False

            if gameover == False:
                if puntuacion > 5:
                    if keys[K_SPACE]:
                        if rex.aire == False:
                            rex.salto(tiempo)
                    if keys[K_UP]:
                        if rex.aire == False:
                            rex.salto(tiempo)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if gameover == False:
                        if rex.aire== False:
                            if event.key == K_SPACE:
                                rex.salto(tiempo)
                            if event.key == K_UP:
                                rex.salto(tiempo)
                        if event.key == K_RIGHT:
                            if armado == True:
                                rex.disparar()
                    else:
                        if event.key == K_SPACE:
                            reinicio = True
                            for suelo in listaSuelos:
                                listaSuelos.remove(suelo)
                if event.type == aparecerNube:
                    if gameover == False:
                        nuevaNube()
                        tempNube = False
                if event.type == aparecerCactus:
                    if gameover == False:
                        if puntuacion < 400:
                            nuevoCactus()
                        else:
                            k = choice([1,2,3])
                            if k == 1:
                                nuevoPajaro(tiempo)
                            else:
                                nuevoCactus()
                        tempCactus = False
                if event.type == masRapido:
                    if gameover == False:
                        rex.velocidadJuego += 1

            #poner en marcha las funciones de las clases
            for suelo in listaSuelos:
                suelo.dibujar(ventana)
                suelo.movimiento(rex.velocidadJuego)
                if suelo.rect.left >= -1600:
                    if suelo.rect.left <= -1550:
                        if suelo.compi == False:
                            nuevoSuelo(suelo.rect.left+2400)
                            suelo.compi = True
                if suelo.rect.left <= -2400:
                    listaSuelos.remove(suelo)
                if reinicio == True:
                    listaSuelos.remove(suelo)

            for nube in listaNubes:
                nube.dibujar(ventana)
                nube.movimiento(rex.velocidadJuego * 0.5)
                if nube.rect.centerx < (-50):
                    listaNubes.remove(nube)
                if gameover == True:
                    listaNubes.remove(nube)

            for cactus in listaCactus:
                cactus.dibujar(ventana)
                cactus.movimiento(rex.velocidadJuego)
                if cactus.rect.centerx < (-50):
                    listaCactus.remove(cactus)
                if cactus.rect.colliderect(rex.rect):
                    cactus.offset = (rex.rect.left - cactus.rect.left, rex.rect.top - cactus.rect.top)
                    resultado = cactus.mask.overlap(rex.mask, cactus.offset)
                    if resultado:
                        gameover = True
                if reinicio == True:
                    listaCactus.remove(cactus)

            for pajaro in listaPajaros:
                pajaro.aleteo(ventana,tiempo,gameover)
                pajaro.movimiento(rex.velocidadJuego)
                if pajaro.rect.centerx < (-50):
                    listaPajaros.remove(pajaro)
                if pajaro.rect.colliderect(rex.rect):
                    pajaro.offset = (rex.rect.left - pajaro.rect.left, rex.rect.top - pajaro.rect.top)
                    resultado = pajaro.mask.overlap(rex.mask, pajaro.offset)
                    if resultado:
                        gameover = True
                if reinicio == True:
                    listaPajaros.remove(pajaro)

            if armado:
                for bala in rex.listaBalas:
                    bala.movimiento(ventana)
                    for pajaro in listaPajaros:
                        if bala.rect.colliderect(pajaro.rect):
                            bala.offset = (pajaro.rect.left - bala.rect.left, pajaro.rect.top-bala.rect.top)
                            if bala.mask.overlap(pajaro.mask, bala.offset):
                                listaPajaros.remove(pajaro)
                                rex.listaBalas.remove(bala)
                    if bala.rect.centerx > 800:
                        rex.listaBalas.remove(bala)
                    if gameover:
                        rex.listaBalas.remove(bala)

            rex.animacion(ventana, int(tiempo))
            #para poner las skins en el lugar bueno
            if numeroSkin == 0:
                skin.dibujar(ventana, rex.rect.centerx, rex.rect.centery)
            elif numeroSkin == 1:
                skin.dibujar(ventana, rex.rect.centerx+17, rex.rect.centery-57)
            elif numeroSkin == 2:
                skin.dibujar(ventana, rex.rect.centerx+30, rex.rect.centery-32)
            elif numeroSkin == 3:
                skin.dibujar(ventana, rex.rect.centerx+45, rex.rect.centery+20)
            rex.fisica(tiempo)

            pygame.display.update()
            clock.tick(60)

            if reinicio == True:
                for cactus in listaCactus:
                    listaCactus.remove(cactus)
                break

try:
    usuario = inicio()
    numeroSkin = seleccionarSkins(int(obtenerSkins(usuario)),obtenerRecord(usuario),usuario)
    juego(usuario, numeroSkin)

except ValueError:
    NoInternet()
    
