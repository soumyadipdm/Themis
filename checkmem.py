''' This module checks the memory usage
and if it is high enough (tunable i.e as to how much high)
it deducts scores from the overall system score and points
out the culprit processes'''

import re

from score import Score
from myexception import MyExcept


class CheckMem(Score):
	inst = False
	def __init__(self):

		if CheckMem.inst:
			raise MyExcept("already one instance is running")
		else:
			CheckMem.inst = True


		self.MemTotal = 0
		self.MemUsed = 0
		self.BufferCached = 0		
		self.SwapTotal = 0
		self.SwapUsed = 0

		self.score_deducted = 0

		with open('/proc/meminfo', 'r') as meminfo_f:
			str = meminfo_f.read()		
			regex_str = r'MemTotal:\s+(\d+).+?MemFree:\s+(\d+).+?Buffers:\s+(\d+).+?Cached:\s+(\d+).+?SwapTotal:\s+(\d+).+?SwapFree:\s+(\d+).+?'
			extract_re = re.compile(regex_str, re.S)		
			match = extract_re.search(str)
			if match:
				self.MemTotal = int(match.group(1))
				self.BufferCached = int(match.group(3)) + int(match.group(4))
				self.MemUsed = self.MemTotal - int(match.group(2)) - self.BufferCached	
				self.SwapTotal = int(match.group(5))
				self.SwapUsed = self.SwapTotal - int(match.group(6))
			
			else:
				raise MyExcept("Could not initialize memory info values")


	def __repr__(self):
		return "MemTotal: %d\nMemUsed: %d\nBufferCached: %d\nSwapTotal: %d\nSwapUsed: %d\nSystemScore: %d\nDeducted: %d" % (self.MemTotal, self.MemUsed, self.BufferCached, self.SwapTotal, self.SwapUsed, Score.my_score, self.score_deducted)

	def score_me(self, mem_threshold=70.0, swap_threshold=20.0):

		old_score = Score.my_score
		
		mem_pct = self.MemUsed/(self.MemTotal+0.0) * 100
		if 90 > mem_pct >= mem_threshold:
			Score.my_score -= 10
		elif mem_pct >= 90:
			Score.my_score -= 15
		else:
			Score.my_score -= 5

		swap_pct = self.SwapUsed/(self.SwapTotal+0.0) * 100

		if 50 > swap_pct >= swap_threshold:
			Score.my_score -= 10
		elif swap_pct >= 50:
			Score.my_score -= 15
		elif 0 < swap_pct <= 10:
			Score.my_score -= 5	
		

		self.score_deducted = old_score - Score.my_score



def main():
	var = CheckMem()
	var.score_me()
	print var

if __name__ == '__main__':
	main()
				
