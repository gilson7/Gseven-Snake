import pygame
import random
import sys
desired_fps = 40  # FPS desejado


pygame.init()
pygame.mixer.init()
points = 0
#sfxs
eatSFX = pygame.mixer.Sound('sfx/eat.mp3')
music = pygame.mixer.Sound('sfx/soundtrack.wav')
#volume incial
music.set_volume(0.1)
eatSFX.set_volume(0.5)
music.play(loops=-1)
# Carregar o ícone da janela
icone = pygame.image.load("icon.png")
#imagem de fundo
background = pygame.image.load("background.png")
# Definir o ícone da janela
pygame.display.set_icon(icone)

cor1 = pygame.Color("#fbbbad")
cor2 = pygame.Color("#ee8695")
cor3 = pygame.Color("#4a7a96")
cor4 = pygame.Color("#333f58")
cor5 = pygame.Color("#292831")
#allcolors
allColors = [cor1,cor2,cor3,cor4,cor5]
#variavel abaixo serve para armazenar a cor da comida
foodLightInterruptor = 0
#armazena o relogio de temo de animacao(food)
foodClockAnimation = 0

QuitHoverColor = cor4
RestartHoverColor = cor4
botao_restart = [216,279,169,39]
botao_quit = [216,334,169,39]
botao_sfx = [550 , 605,20,20]
botao_music = [575 ,605,20,20]
#armazamento de configuracao de audio, musica e sfx (não ou sim) = (0 ou 1)
is_music = 1
is_sfx = 1
#icones para layaouts
sfx_icons = [pygame.image.load('icons/fxfause.png'),pygame.image.load('icons/fxtrue.png'),] 
music_icons = [pygame.image.load('icons/musicfause.png'),pygame.image.load('icons/musictrue.png')] 
#layouts
class Layout:
    _instance = None
    def __init__(self):
        #botoes e divs
        self.popBolck = (cor4,(130,175,341,250))
        self.menuBolck = (cor4,(0,600,600,30))
        self.popBolckBorder = (cor3,(130-3,175-3,341+6,250+6))
        self.popButtonRestartBorder = (RestartHoverColor,(216-3,279-3,169+6,39+6))
        self.popButtonQuitBorder = (QuitHoverColor,(216-3,334-3,169+6,39+6))
        self.popButtonRestart = (cor3,(216,279,169,39))
        self.popButtonQuit = (cor2,(216,334,169,39))
        #fontes
        self.fonte = pygame.font.Font("fontes/pixel.ttf", 60)
        self.fonte2 = pygame.font.Font("fontes/pixel.ttf", 27)
        self.fonte3 = pygame.font.Font("fontes/pixel.ttf", 27)
        self.fonte4 = pygame.font.Font("fontes/pixel.ttf", 20)
        # textos
        self.texto_lose = (self.fonte.render("You Lose", True, cor2),(213,192))
        self.texto_restart = (self.fonte2.render("Restart", True, cor1),(266,287))
        self.texto_quit = (self.fonte3.render("Quit", True, cor5),(281,340))
        self.texto_pontos = (self.fonte4.render("SCORE - "+str(points), True, cor1),(10,605))
    def reload(self):
        self.popBolck = (cor4,(130,175,341,250))
        self.menuBolck = (cor4,(0,600,600,30))
        self.popBolckBorder = (cor3,(130-3,175-3,341+6,250+6))
        self.popButtonRestartBorder = (RestartHoverColor,(216-3,279-3,169+6,39+6))
        self.popButtonQuitBorder = (QuitHoverColor,(216-3,334-3,169+6,39+6))
        self.popButtonRestart = (cor3,(216,279,169,39))
        self.popButtonQuit = (cor2,(216,334,169,39))
        #fontes
        self.fonte = pygame.font.Font("fontes/pixel.ttf", 60)
        self.fonte2 = pygame.font.Font("fontes/pixel.ttf", 27)
        self.fonte3 = pygame.font.Font("fontes/pixel.ttf", 27)
        self.fonte4 = pygame.font.Font("fontes/pixel.ttf", 20)
        # textos
        self.texto_lose = (self.fonte.render("You Lose", True, cor2),(213,192))
        self.texto_restart = (self.fonte2.render("Restart", True, cor1),(266,287))
        self.texto_quit = (self.fonte3.render("Quit", True, cor5),(281,340))
        self.texto_pontos = (self.fonte4.render("SCORE - "+str(points), True, cor1),(10,605))
        
layout = Layout()
step = 20
size = 30
gameProps = {"width":size*step,"height":(size*step)+30}
left = False 
right = False
top =False
down = False
screen = pygame.display.set_mode((gameProps['width'], gameProps['height']))
pygame.display.set_caption("GSEVEN SNAKE")
clock = pygame.time.Clock()
food = [cor1,(random.randint(1, size)*step)-step  ,(random.randint(1, size)*step)-step ,step,step]
snake = [14*step,14*step,step,step]
body = [[14*step,14*step,step,step]]
screen.fill(cor5)
stateGame = True
filaDeInputs = [""]
myindex = 0

def update():
    global myindex
    global food
    global stateGame
    global points
    global music
    global eatSFX
    global layout
    global foodLightInterruptor
    global foodClockAnimation
    
    #animando a comida(food)
    intervalo = 10
    fullTime  = intervalo*2
    if(foodClockAnimation<intervalo):
        foodClockAnimation+=1
        foodLightInterruptor = 1
    elif(foodClockAnimation >= intervalo and foodClockAnimation < fullTime):
        foodClockAnimation+=1
        foodLightInterruptor = 4
    elif(foodClockAnimation >= fullTime):
        foodClockAnimation = 0
        
    #ativando e desativando sons
    if(is_music):
        music.set_volume(0.1)
    else:
        music.set_volume(0)
    if(is_sfx):
        eatSFX.set_volume(0.5)
    else:
        eatSFX.set_volume(0)
    #fim da config de sons
    if stateGame and snake[0] > -1 and snake[0] < size*step and snake[1] > -1 and snake[1] < size*step:
        temp_pos = list(snake)  # Armazena a posição atual antes de qualquer atualização
        for index, value in enumerate(body):
            if index > 0:
                body[index] = list(temp_pos)  # Atribui a posição anterior ao item atual
            temp_pos = list(value)
        body[0] = list(snake)

        last = filaDeInputs [len(filaDeInputs)-1]
        if len(filaDeInputs)<2:
            if left and last != "left":
                filaDeInputs.append("left")
            # snake[0] -= step
            elif right and last !="right":
                filaDeInputs.append("right")
            # snake[0] += step
            elif top and last !="top":
                filaDeInputs.append("top")
            # snake[1] -= step
            elif down and last !="down":
                filaDeInputs.append("down")
            # snake[1] += step
        if len(filaDeInputs):
            direction = filaDeInputs[0]
            if direction == "left":
                snake[0] -= 5
            elif direction == "right":
                snake[0] += 5
            elif direction == "top":
                snake[1] -= 5
            elif direction == "down":
                snake[1] += 5

            if myindex == 3:
                myindex = 0
                if(len(filaDeInputs)>1):
                    filaDeInputs.pop(0)
            else:
                myindex += 1
              
        for index, value in enumerate(body):
            if index:
                if body[index][0] == snake[0] and body[index][1]  == snake[1]:
                    stateGame = False
        if(snake[0] == food[1] and snake[1] == food[2]):
            body.append(snake)
            body.append(snake)
            body.append(snake)
            body.append(snake)
            body.append(snake)
            food = [cor1,(random.randint(1, size)*step)-step  ,(random.randint(1, size)*step)-step ,step,step]
            eatSFX.play()
            points+=1
            layout.reload()
    else:
        stateGame = False
def draw():
    #background
    screen.blit(background,(0,0))
    #menu infos 
    pygame.draw.rect(screen ,*layout.menuBolck) 
    screen.blit(*layout.texto_pontos)
    screen.blit(pygame.transform.scale(sfx_icons[is_sfx],(20,20)), (botao_sfx[0], botao_sfx[1]))
    screen.blit(pygame.transform.scale(music_icons[is_music],(20,20)), (botao_music[0],botao_music[1]))
    if stateGame:
        pygame.draw.rect(screen, allColors[foodLightInterruptor], ( food[1], food[2],food[3], food[4]))
        pygame.draw.rect(screen, cor3, ( snake[0], snake[1],snake[2], snake[3]))
        for elment in body:
            pygame.draw.rect(screen, cor3, ( elment[0], elment[1],elment[2], elment[3]))
    
    else:
        #popup dead
        pygame.draw.rect(screen,*layout.popBolckBorder)
        pygame.draw.rect(screen,*layout.popBolck)
        screen.blit(*layout.texto_lose)
        #botao  restart
        pygame.draw.rect(screen ,*layout.popButtonRestartBorder)
        pygame.draw.rect(screen ,*layout.popButtonRestart)
        screen.blit(*layout.texto_restart)
        #botao  quit
        pygame.draw.rect(screen ,*layout.popButtonQuitBorder)
        pygame.draw.rect(screen ,*layout.popButtonQuit)
        screen.blit(*layout.texto_quit)
        
     

# Loop principal do jogo
while True:

    # Verificação de eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if(stateGame == True):
            if event.type == pygame.KEYDOWN and stateGame:
                if event.key == pygame.K_a and right==False:
                    down = False
                    top = False
                    right = False
                    left = True
                if event.key  == pygame.K_d and left==False:
                    down = False
                    top = False
                    left = False
                    right = True
                if event.key  == pygame.K_w and down==False:
                    down = False
                    left = False
                    right = False
                    top = True
                if event.key == pygame.K_s and top==False:
                    left = False
                    right = False
                    top = False
                    down = True
        else:
            
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if (
                    botao_quit[0] <= mouse_pos[0] <= botao_quit[0] + botao_quit[2] and
                    botao_quit[1] <= mouse_pos[1] <= botao_quit[1] + botao_quit[3] 
                ):
                    
                    QuitHoverColor = cor1
                else:
                    QuitHoverColor = cor4
                if (
                    botao_restart[0] <= mouse_pos[0] <= botao_restart[0] + botao_restart[2] and
                    botao_restart[1] <= mouse_pos[1] <= botao_restart[1] + botao_restart[3] 
                ):
                    RestartHoverColor = cor1
                else:
                    RestartHoverColor = cor4
                
            layout.reload()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (event.button == 1 and
                    botao_quit[0] <= mouse_pos[0] <= botao_quit[0] + botao_quit[2] and
                    botao_quit[1] <= mouse_pos[1] <= botao_quit[1] + botao_quit[3] 
                ):
                    pygame.quit()
                    sys.exit()
                if (event.button == 1 and
                    botao_restart[0] <= mouse_pos[0] <= botao_restart[0] + botao_restart[2] and
                    botao_restart[1] <= mouse_pos[1] <= botao_restart[1] + botao_restart[3] 
                ):
                    down = False
                    top = False
                    filaDeInputs = [""]
                    right = False
                    left = False
                    food = [cor1,(random.randint(1, size)*step)-step  ,(random.randint(1, size)*step)-step ,step,step]
                    snake = [14*step,14*step,step,step]
                    body = [[14*step,14*step,step,step]]
                    stateGame = True    
                    points = 0
                    layout.reload()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #checando click no botão de musica e sfx
            mouse_pos = pygame.mouse.get_pos()
            if (event.button == 1 and
                botao_sfx[0] <= mouse_pos[0] <= botao_sfx[0] + botao_sfx[2] and
                botao_sfx[1] <= mouse_pos[1] <= botao_sfx[1] + botao_sfx[3] 
            ):
                if is_sfx == 1:
                    is_sfx=0
                    layout.reload()
                else:
                    is_sfx = 1
                    layout.reload()
            if (event.button == 1 and
                botao_music[0] <= mouse_pos[0] <= botao_music[0] + botao_music[2] and
                botao_music[1] <= mouse_pos[1] <= botao_music[1] + botao_music[3] 
            ):
                if is_music == 1:
                    is_music=0
                    layout.reload()
                else:
                    is_music = 1
                    layout.reload()
    update()
    screen.fill(cor5)
    draw()
    # Atualização da tela
    pygame.display.flip()
    clock.tick(desired_fps)

 
