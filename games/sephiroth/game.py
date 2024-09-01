# @name Name of my Amazing Example Game
# @author Jane & John Smith
x = 0
y = 30
import os

from HiScore import HiScore
from TimeSpanTracker import TimeSpanTracker
from vector import vector
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import pgzrun
import random
import sys
import time
import pickle

WIDTH = 800
HEIGHT = 600
lives = int(3)

try:
  with open("hiscore", "rb") as f:
    hiScore = pickle.load(f)
except:
  hiScore = HiScore()

gemvector = vector()

ship = Actor('playership1_blue')
ship.x = 370
ship.y = 550

###gold shield will make you immune for 3secs
###gold bolt will slow the gems down for 3 secs

gem = Actor('gemgreen')
gem_images = ['gemblue', 'gemgreen', 'gemred', 'gemyellow','star_gold','meteorbrown_big3','bolt_gold', 'shieldgold']
gem.images = gem_images
gem.x = random.randint(20, 780)
gem.y = 0

score = 0
game_over = False

immunityTracker =  TimeSpanTracker()
slowdownTracker = TimeSpanTracker()

def update():
  global score, game_over, lives, gemvector, immunityTracker, slowdownTracker, hiScore

  if keyboard.escape:
    exit()
    sys.exit()
  if game_over:
    return
  if keyboard.left:
    ship.x = (ship.x - 5 - score / 5) % WIDTH
  if keyboard.right:
    ship.x = (ship.x + 5 + score / 5) % WIDTH

  if keyboard.up:
    ship.y = (ship.y - 5 - score / 5) % HEIGHT
  if keyboard.down:
    ship.y = (ship.y + 5 + score / 5) % HEIGHT

  ship.image = 'playership1_red' if immunityTracker.IsActive() else 'playership1_blue'

  wasmeteor = False
  newgem = False


  gem.y = gem.y + gemvector.vy  + (score / 5 if not slowdownTracker.IsActive() else 0)
  gem.x = (gem.x + gemvector.vx) % WIDTH 
  if gem.y > 600:
    if gem.image == 'star_gold' or gem.image == 'shieldgold' or gem.image == 'bolt_gold':
      newgem = True
    elif gem.image == 'meteorbrown_big3':
      wasmeteor = True
    else:
      newgem = True 
      lives = lives -1
      if lives == 0:
        game_over = True

  collision = gem.colliderect(ship) 


  if collision:
    if gem.image == 'bolt_gold':
      slowdownTracker.StartTimer(3)
    elif gem.image == 'shieldgold':
      immunityTracker.StartTimer(3)
    elif gem.image == 'gemblue':
      score = score + 1
    elif gem.image == 'gemgreen':
      score = score + 2
    elif gem.image == 'gemred':
      score = score + 3
    elif gem.image == 'gemyellow':
      score = score + 4
    elif gem.image == 'star_gold':
      lives = lives + 1
    elif gem.image == 'meteorbrown_big3' and not immunityTracker.IsActive():
      game_over = True
    
  if collision | wasmeteor | newgem:
    gem.x = random.randint(20, 780)
    gem.y = 0
    gem.image = random.choice(gem_images)
    gemvector.vx = random.randint(-5,5)
    gemvector.vy = random.randint(1,5)

def draw():
  screen.fill((80,0,70))
  if game_over:
    newHiScore = score >= hiScore.HiScore
    if(score > hiScore.HiScore):
      hiScore.HiScore = score
      with open("hiscore", "wb") as f:
        pickle.dump(hiScore, f) 


    screen.draw.text('Game Over', centerx=WIDTH/2, top=200, color=(255,255,255), fontsize=150)
    screen.draw.text(('New High Score!!'  if newHiScore == True else 'Final Score: ' + str(score)), centerx=WIDTH/2, top=320, color=(255,255,255), fontsize=50)
    screen.draw.text('Hi Score: ' + str(hiScore.HiScore), centerx=WIDTH/2, top=420, color=(255,255,255), fontsize=30)
  else:
    gem.draw()
    ship.draw()
    screen.draw.text('Score: ' + str(score) + ' Lives: ' + str(lives), (15,10), color=(255,255,255), fontsize=30)

pgzrun.go() # Must be last line