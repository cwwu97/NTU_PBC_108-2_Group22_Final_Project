import pygame
import sys, time
import random
import pygame.font
from pygame.locals import *

pygame.init()  # 初始化

# 參數設定
window_width = 1080  # 視窗寬度
window_height = 720  # 視窗高度
pink =  (255, 123, 172)
yellow = (241,192,95)
red = (255, 125, 125)
purple = (217, 125, 255)
brown = (255, 156, 125)
blue = (63, 169, 245)
green = (187, 205, 74)

scoreboard_font = pygame.font.SysFont('Helvetica.ttc', 34) # 計分板字體
scoreboard_font.set_bold(True)
textbox_font = pygame.font.SysFont("Helvetica.ttc", 32)  # 玩家輸入單字字體
vocab_font = pygame.font.SysFont("Helvetica.ttc", 24)  # 病毒對應單字字體
level_font = pygame.font.SysFont("Helvetica.ttc", 34)  # 關卡字體
level_font.set_bold(True)
clock = pygame.time.Clock()

# 視窗
window = pygame.display.set_mode((window_width, window_height))  # 製作視窗，命名為window
caption = pygame.display.set_caption("Virus Attack")  # 視窗標題

# 開始畫面與結束畫面
cover = pygame.image.load("封面.png")
cover = pygame.transform.rotozoom(cover, 0, 0.84)
win = pygame.image.load("勝利.png")
win = pygame.transform.rotozoom(win, 0, 0.84)
loss = pygame.image.load("失敗.png")
loss = pygame.transform.rotozoom(loss, 0, 0.84)

# 遊戲規則
rule = pygame.image.load("遊戲規則.png")
rule = pygame.transform.rotozoom(rule, 0, 0.84)

# 背景
background1 = pygame.image.load("背景一.png")  # 匯入背景圖片，命名為background
background1 = pygame.transform.rotozoom(background1,0, 0.84)
background2 = pygame.image.load("背景二.png")  # 匯入背景圖片，命名為background
background2 = pygame.transform.rotozoom(background2,0, 0.84)
background3 = pygame.image.load("背景三.png")  # 匯入背景圖片，命名為background
background3 = pygame.transform.rotozoom(background3,0, 0.84)

# 前景
foreground = pygame.image.load("前景.png")  # 匯入背景圖片，命名為background
foreground = pygame.transform.rotozoom(foreground,0, 0.84)
redfilter = pygame.image.load("紅色遮罩.png")
redfilter = pygame.transform.rotozoom(redfilter, 0, 0.84)

# 單字選擇表
easy = pygame.image.load("初級單字.png")
easy = pygame.transform.rotozoom(easy, 0, 0.84)
medium = pygame.image.load("中級單字.png")
medium = pygame.transform.rotozoom(medium, 0, 0.84)
hard = pygame.image.load("高級單字.png")
hard = pygame.transform.rotozoom(hard, 0, 0.84)
Vocab_choice = [easy, medium, hard]

# 匯入單字
vocab1 = open("國中單字.txt", "r")
vocab1 = vocab1.readlines()[0].split(',')[:-1]
vocab2 = open("高中單字.txt", "r")
vocab2 = vocab2.readlines()[0].split(',')[:-1]
vocab3 = open("GRE單字.txt", "r")
vocab3 = vocab3.readlines()[0].split(',')[:-1]
Vocab_list = [vocab1, vocab2, vocab3]

# 生命值（口罩）
mask = pygame.image.load("口罩.png")
mask = pygame.transform.rotozoom(mask, 30.0, 0.15)
all_masks = [mask]*3  # 將口罩圖片全部裝進all_masks這個list中

# 計分板
score = 280
scoreboard = scoreboard_font.render("Score: %d" %score, True, pink)

# 匯入初始座標與移動路徑 -->可再寫成一個函數
coords = open('病毒初始座標.txt','r')
coords = coords.readlines()[0].split(';')
for i in range(len(coords)):
    coords[i] = coords[i].split(',')
    coords[i][0] = int(coords[i][0])
    coords[i][1] = int(coords[i][1])
    coords[i][2] = int(coords[i][2])
    coords[i][3] = int(coords[i][3])
    
# 主角物件（陳時中）
class Character(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()  
        self.raw_image = pygame.image.load(filename)  # 載入圖片
        self.image = pygame.transform.smoothscale(self.raw_image, (109,141))  # 縮小圖片
        self.rect = self.image.get_rect()  # 回傳位置
        self.rect.topleft = (493, 275)  # 定位

# 病毒物件
class Virus(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__() 
        self.filename = filename
        self.raw_image = pygame.image.load(filename) #載入圖片
        self.image = pygame.transform.rotozoom(self.raw_image, 0, 0.1) #縮小圖片
        self.rect = self.image.get_rect()  #回傳位置
        #定位
        
        coord_index = random.randint(0, 11)  # 隨機生成初始位置和路徑
        self.x = coords[coord_index][0]  # x座標
        self.y = coords[coord_index][1]  # y座標
        self.xPath = coords[coord_index][2]
        self.yPath = coords[coord_index][3]
        self.rect.topleft = (self.x, self.y)
        #病毒單字
        vocab_index = random.randint(0, len(vocab)-1)  
        self.vocab = vocab[vocab_index]
        
    def virus_Move(self):
        self.x += self.xPath / level_speed
        self.y += self.yPath / level_speed
        self.rect.topleft = (self.x, self.y)


# 成立病毒精靈物件的群組
all_viruses = pygame.sprite.Group()

# 文字輸入對話框
validChars = "abcdefghijklmnopqrstuvwxyz"
class TextBox(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = textbox_font
        self.image = self.font.render("Let's GO!", True, blue)
        self.rect = self.image.get_rect()
    def add_chr(self, char):
        if char in validChars:
            self.text += char
        self.update()
    def update(self):
        old_rect_pos = self.rect.center
        self.image = self.font.render(self.text, True, blue)   # 更新文字，設定字體黑色
        self.rect = self.image.get_rect()
        self.rect.center = old_rect_pos
        
textBox = TextBox()
textBox.rect.center = [860, 670]  # 調整文字輸入框位置，以符合前景
		
# 畫面更新指令
def GameUpdate(all_viruses, filter):
    window.blit(background, (0,0))  # 視窗填滿background image，以座標(0,0)對齊
    window.blit(character.image, character.rect)  # 顯示陳時中

    for virus in all_viruses.sprites():  # 針對每個群組中的病毒物件，畫出對應的圖片
        virus.virus_Move()
        window.blit(virus.image, virus.rect.topleft)
        if virus.filename == virus1:
            vocab_color = blue
        elif virus.filename == virus2:
            vocab_color = purple
        elif virus.filename == virus3:
            vocab_color = red
        elif virus.filename == virus4:
            vocab_color = pink
        elif virus.filename == virus5:
            vocab_color = brown
        else:
            vocab_color = green
        
        vocab_image = vocab_font.render(virus.vocab, True, vocab_color)  # 建立單字
        vocab_image_rect = vocab_image.get_rect()
        vocab_image_rect.center = virus.rect.center
        window.blit(vocab_image, (vocab_image_rect.x, virus.rect.y - 25))  # 顯示單字
        
    window.blit(foreground, (0,0))  # 顯示前景
    window.blit(textBox.image, textBox.rect)  # 文字輸入框
    
    for i in range(len(all_masks)):  # 口罩更新的顯示
    	window.blit(all_masks[i], ((20 + 70*i), -10))
    	
    scoreboard = scoreboard_font.render("score: %d" %score, True, pink)  # 計分板更新
    window.blit(scoreboard, (850, 34))
    
    levelboard = level_font.render("LEVEL %d" %level, True, levelboard_color)  # 關卡表更新
    window.blit(levelboard, (470, 34))
    
    if filter:
    	window.blit(redfilter, (0,0))
    	filter = False
    	
    pygame.display.update()
    return filter
    
"""
遊戲主系統運行
"""
Game = True
while Game:  # 最外圈
	
	# 背景音樂
	pygame.mixer.init()
	pygame.mixer.music.load("BGM.mp3")
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(-1) #開始始播放
	
	# 封面
	Cover = True
	while Cover:
		window.blit(cover, (0,0))
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					Cover = False
					
	# 遊戲規則
	Rule = True
	while Rule:
		window.blit(rule, (0,0))
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					Rule = False
					
	# 選擇遊戲關卡
	Vocab = True
	choice = 0
	while Vocab:
		window.blit(Vocab_choice[choice], (0,0))
		pygame.display.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					choice += 1
					if choice > 2:
						choice = 2
				elif event.key == pygame.K_LEFT:
					choice -= 1
					if choice < 0:
						choice = 0
				elif event.key == pygame.K_SPACE:
					Vocab = False
					
		vocab = Vocab_list[choice]
	
	# 遊戲畫面
	# 初始值設定
	gametime = 0
	level = 1
	level_speed = 120
	levelboard_color = yellow
	background = background1
	words = []  # 畫面中病毒頭上的文字列表
	answer = "" # 預設答案
	filter = False
	
	character = Character("陳時中.png")
	virus1 = "病毒一.png"
	virus2 = "病毒二.png"
	virus3 = "病毒三.png"
	virus4 = "病毒四.png"
	virus5 = "病毒五.png"
	viruslist = [virus1, virus2, virus3, virus4, virus5]  # 將所有病毒圖片裝進viruslist這個list中

	MainGame = True      
	while MainGame:
		clock.tick(24)  # 每秒跑24張圖的速度
		gametime += 1
	
		if gametime == 1:  # 初始的病毒      
			first_virus = Virus(random.choice(viruslist))
			all_viruses.add(first_virus)
			words.append(first_virus.vocab)

		if gametime % 60 == 0:  # 之後每秒叫出一隻病毒
			new_virus = Virus(random.choice(viruslist))
			all_viruses.add(new_virus)
			words.append(new_virus.vocab)

		virus_hit = pygame.sprite.spritecollide(character, all_viruses, True)  # 碰撞到陳時中的病毒精靈清單
		for i in virus_hit:  # 把該病毒物件從群組刪除
			words.remove(i.vocab)
			if all_masks != []:
				all_masks.remove(all_masks[0])
				soundwav = pygame.mixer.Sound("陳時中音效.ogg")
				soundwav.play() #病毒消失金幣音效
				filter = True
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		
			if event.type == pygame.KEYDOWN:  # 將輸入的文字加入text
				textBox.add_chr(pygame.key.name(event.key))
				if len(textBox.text) >= 20:
					textBox.text = ""
				if event.key == pygame.K_BACKSPACE:
					textBox.text = textBox.text[:-1]
				if event.key == pygame.K_RETURN:  # 如果按下Enter鍵(Return)，送出文字check
					if len(textBox.text) > 0:
						answer = textBox.text
						textBox.text = ""
				textBox.update()		
			
		if answer in words:  # 若輸入答案吻合畫面中的單字，消除病毒，加10分
			soundwav = pygame.mixer.Sound("病毒消失音效.wav")
			soundwav.play() #病毒消失金幣音效
			words.remove(answer)
			score += 10
			for virus in all_viruses:
				if virus.vocab == answer:
					all_viruses.remove(virus)

			if 0 <= score < 100:
				level = 1
				level_speed = 120
				levelboard_color = yellow
				background = background1
			elif 100 <= score < 200:
				level = 2
				level_speed = 90
				levelboard_color = green
				background = background2
			elif 200 <= score:
				level = 3
				level_speed = 70
				levelboard_color = pink
				background = background3
		
		elif score >= 300:
			MainGame = False
			GameResult = "Win"
		elif len(all_masks) == 0:
			MainGame = False
			GameResult = "Loss"
			
		filter = GameUpdate(all_viruses, filter)
	
	
	# 結束	
	Gameover = True
	pygame.mixer.music.stop()
	
	if GameResult == "Win":  #勝利音效
		pygame.mixer.init()
		pygame.mixer.music.load("victory.mp3")
		pygame.mixer.music.set_volume(1)
		pygame.mixer.music.play(1) #開始播放一次
		
	elif GameResult == "Loss":  #失敗音效
		pygame.mixer.init()
		pygame.mixer.music.load("loss.mp3")
		pygame.mixer.music.set_volume(1)
		pygame.mixer.music.play(1) #開始始播放一次
	
	while Gameover:
		if GameResult == "Win":
			window.blit(win, (0,0))
			scoreboard = scoreboard_font.render("Score: %d" %score, True, pink)  # 計分板更新
			window.blit(scoreboard, (850, 34))
			pygame.display.update()
		elif GameResult == "Loss":
			window.blit(loss, (0,0))
			scoreboard = scoreboard_font.render("Score: %d" %score, True, pink)  # 計分板更新
			window.blit(scoreboard, (850, 34))
			pygame.display.update()
			
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
						Gameover = False
						Cover = True
						MainGame = True
						score = 0
						textBox.text = ""
						textBox = TextBox()
						textBox.rect.center = [860, 670] 
						all_masks = [mask]*3
						all_viruses = pygame.sprite.Group()
						words = []						
						print("restart")
				if event.key == pygame.K_ESCAPE: # 按Esc會跳出遊戲
						Gameover = False
						Game = False
						
pygame.quit()

# ==========================《NOTE》==============================
# 2. 迴圈中的暫停功能