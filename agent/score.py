import time

class Score:
	'''This is the main class which keeps
score of each node'''
	my_score = 100
	score_time = time.time()

	def __init__(self):
		pass

	@classmethod
	def update_score(cls, value):
		cls.my_score -= value
		cls.score_time = time.time()


	@classmethod
	def get_score(cls):
		return cls.my_score

	@classmethod
	def get_time(cls):
		return cls.score_time
