#!/usr/bin/python3
#
# Script written by Legoktm, 2011
# Released under the MIT License on November, 30, 2011
# Syntax: ./montyhall.py iterations
# Read more about it on my blog: http://crazeness.wordpress.com/2011/11/30/analyzing-the-monty-hall-problem-in-python
# Enjoy!
#

import sys, random

class MontyHall:
	def __init__(self):
		self.x = random.Random()
		self.r = self.x.randint
	def test(self, switch):
		ans = self.r(1,3)
		picked = self.r(1,3)
		possibleopen = self.recompilelist(self.recompilelist([1,2,3], picked), ans)
		if len(possibleopen) == 2:
			open = possibleopen[self.r(0,1)]
		else:
			open = possibleopen[0]
		if switch:
			picked = self.recompilelist(self.recompilelist([1,2,3], picked), open)[0]
			#print picked == ans
		return picked == ans

	def gameshow(self, tries):
		x=0
		switchwork = 0
		y=0
		noswitchwork = 0
		while x < tries/2:
			if self.test(True):
				switchwork += 1
			x += 1
		while y < tries/2:
			if self.test(False):
				noswitchwork += 1
			y += 1
		runs = float(tries/2)
		percentageswitch = float(switchwork)/runs
		percentagenoswitch = float(noswitchwork)/runs
		print('Switch worked ',str(switchwork),'/',str(runs),' times, or ',str(percentageswitch),'%.')
		print('Stay worked ',str(noswitchwork),'/',str(runs),' times, or ',str(percentagenoswitch),'%.')
			
	def recompilelist(self, list, value):
		new = []
		for x in list:
			if x != value:
				new.append(x)
		return new


if __name__ == "__main__":
	m = MontyHall()
	if sys.argv[1:]:
		m.gameshow(int(sys.argv[1]))
	else:
		print('Please use proper syntax: ./montyhall.py #ofIterations')
