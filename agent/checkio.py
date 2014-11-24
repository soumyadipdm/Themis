'''This module checks and scores for
IO bottlenecks'''

from score import Score
from myexception import MyExcept

class CheckIO:
	
	inst = False
	def __init__(self):
		if CheckIO.inst:
			raise MyExcept("CheckIO already has an instance")	
		else:
			inst = True

		self.user = 0
		self.nice = 0
		self.system = 0
		self.idle = 0
		self.iowait = 0
		self.uptime = 0
		self.score_deducted = 0

		with open('/proc/stat') as stat_f:
			(self.user, self.nice, self.system, self.idle, self.iowait)= tuple(int(i) for i in stat_f.readline().split()[1:6])
			

		with open('/proc/uptime') as uptime_f:
			self.uptime = float(uptime_f.readline().split()[0])

		if self.uptime == 0 or self.user == 0:
			raise MyExcept("Could not initialize CheckIO")
	

	def __repr__(self):
		return "User: %d\nNice: %d\nSystem: %d\nIdle: %d\nIowait: %d\nUptime %f\nSystemScore: %d\nDeducted: %d\n" % (self.user, self.nice, self.system, self.idle, self.iowait, self.uptime, Score.get_score(), self.score_deducted)
	

	def score_me(self, iowait_threshold=20):
		old_score = Score.get_score()
		iowait_pct = self.iowait/(self.uptime+0.0) * 100
		idle_pct = self.idle/(self.uptime+0.0) * 100
		busy_pct = (self.user+self.nice+self.system)/(self.uptime+0.0) * 100

		if iowait_pct >= busy_pct:
			Score.update_score(20)

		elif busy_pct >= idle_pct:
			Score.update_score(10)

		if iowait_pct >= (iowait_threshold/100.0) * self.uptime:
			Score.update_score(10)

		self.score_deducted = old_score - Score.get_score()

	




def main():
	var = CheckIO()
	var.score_me()
	print var	


if __name__ == '__main__':
	main()
