from turtle import *
import random

"""
CLASSES AND FUNCTIONS
"""
class Player(Turtle):
	def __init__(self, screen):
		super().__init__()
		self.ht()
		self.pu()
		self.shape("player.gif")
		self.goto(0,-200)
		self.st()
		self.rounds = []
		self.score = 0
		self.screen = screen
		self.setheading(90)
		self.alive = True
		self.screen.onkeypress(self.move_right,"Right")
		self.screen.onkeypress(self.move_left, "Left")
		self.screen.onkey(self.fire, "space")

	def move_left(self):
		if self.xcor()>-340:
			self.setx(self.xcor()-5)

	def move_right(self):
		if self.xcor()<340:
			self.setx(self.xcor()+5)

	def fire(self):
		if len(self.rounds)<5:
			self.rounds.append(Bullet(self,self.rounds))

	def delete(self):
		self.ht()
		self.alive = False

class Alien(Turtle):
	def __init__(self, x, y):
		super().__init__()
		self.speed(0)
		self.ht()
		self.pu()
		self.shape("space_invader1.gif")
		self.goto(x,y)
		self.st()
		self.move_count = 0
		self.delta_x = -1
		self.setheading(-90)
		self.rounds = []
		self.speed(1)

	def move(self):
		if self.move_count%100 ==0:
			self.down()
		self.setx(self.xcor()+self.delta_x)
		self.move_count +=1

	def down(self):
		self.sety(self.ycor()-25)
		self.delta_x *= -1

	def delete(self, list):
		self.ht()
		list.remove(self)


class Bullet(Turtle):
	def __init__(self, player, list):
		super().__init__()
		self.speed(0)
		self.ht()
		self.pu()
		self.color("white")
		self.goto(player.xcor(), player.ycor())
		self.setheading(player.heading())
		self.forward(40)
		self.list = list
		self.st()
   	
	# move the bullet
	def move(self):
		self.forward(15)
		if self.ycor()>300 or self.ycor()< -300:
			self.delete()
			
	# delete the bullet
	def delete(self):
		self.ht()
		self.list.remove(self)

class Defense(Turtle):
	def __init__(self,x,y, list):
		super().__init__()
		self.speed(0)
		self.ht()
		self.pu() 
		self.goto(x,y)
		self.hits = 0
		self.shape("large.gif")
		self.st()
		self.wall = list

	def strike(self):
		self.hits+=1
		if self.hits==6:
			self.delete()
		elif self.hits > 3:
			self.shape("medium.gif")

	def delete(self):
		self.ht()
		self.wall.remove(self)


class ScoreBoard(Turtle):
	def __init__(self):
		super().__init__()
		self.speed(0)
		self.ht()
		self.penup()
		self.color("white")
		self.goto(-300,-200)

	def display(self, text):
		self.clear()
		self.write("Score: "+str(text), align = "center", font=("Times New Roman",20))

	def game_over(self,text):
		self.clear()
		self.home()
		self.color("red")
		self.write("GAME OVER!\nYour Score: "+str(text), align = "center", font=("Times New Roman",40))

def update(counter):
	if len(enemies)>0 and player.alive: 
		score.display(player.score)
		# move each of the enemies
		for alien in enemies:
			alien.move()
			if alien.ycor() < - 200 or alien.distance(player)<30:
				player.delete()

		# randomly select an enemy to fire a bullet.
		if counter % 5 == 0:
			index = random.randint(0,len(enemies)-1)
			bullets.append(Bullet(enemies[index],bullets))

		# move each bullet fired by the enemies
		for bullet in bullets[:]:
			bullet.move()
			# check for collision with player
			if bullet.distance(player)<20:
				player.delete()
			# check for collision with a wall
			for wall in walls[:]:
				if bullet.distance(wall)<20:
					try:
						bullet.delete()
						wall.strike()
					except:
						pass
			  			
						
				
		# move bullets fired by the player
		for bullet in player.rounds:
			bullet.move()
			# check for collision with an enemy
			for alien in enemies:
				if bullet.distance(alien)<20:
					player.score += 1
					bullet.delete()
					alien.delete(enemies)
			for wall in walls:
				if bullet.distance(wall)< 20:
					wall.ht()
					walls.remove(wall)
		counter += 1
		screen.ontimer(lambda:update(counter),40)
	else: 
		score.game_over(player.score)

"""
SCREEN
"""
screen = Screen()
screen.bgpic("night_sky.png")
screen.register_shape("player.gif")
screen.register_shape("space_invader1.gif")
screen.register_shape("small.gif")
screen.register_shape("medium.gif")
screen.register_shape("large.gif")
screen.tracer(2)
screen.listen()

"""
TURTLE AND OBJECT INSTANTIATION
"""
enemies = []
walls = []
bullets = []
score = ScoreBoard()
for x in range(-300,300,175):
	for xx in range(x,x+90,30):
		walls.append(Defense(xx,-125,walls))
for x in range(-330,260, 60):
	for y in range(220,140,-40):
		enemies.append(Alien(x,y))

player = Player(screen)


"""
GAME LOOP
"""
counter = 0
update(counter)
screen.mainloop()