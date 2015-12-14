import sys
import random
	
def playGame(secretNumber):
	guess=-1
	score=0	
	for i in range(10):		
		guess=int(raw_input("Please guess a number between 0 and 100 "))
		if(guess<secretNumber):
			print "Your guess is low"
		elif (guess>secretNumber):
			print "Your guess is high"
		else:
			print "You are right"
			score = 100
			break
		
	return score
	
	

def main():

	secretNumber = random.randint(0,100)
	playerScore=playGame(secretNumber)
	if playerScore==100:
		print "You won"
	else:
		print "You lost"
	

if __name__ == '__main__':
  main()
