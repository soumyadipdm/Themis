'''If score of a node has reached TTL, send a trigger message
to the node. We will not wait for the node's response, instead
we will delete the node from the queue. Node will publish
its score anyway'''

import trigger
import myexception
import Queue
import multiprocessing
import heapq
import operator
import time


class MyPrioQ:
	def __init__(self):
		self._queue = []
		self._index = 0

	def put(self, item, prio):
		heapq.heappush(self._queue, (-prio, self._index, item))
		self._index += 1

	def get(self):
		return heapq.heappop(self._queue)[-1]

class Balancer:
	instances = 0
	
	@classmethod
	def get_inst(cls):
		return cls.instances

	@classmethod
	def incr_inst(cls):
		cls.instances += 1
	
	def __init__(self, IP='*', PORT='5557', age_threshold=300):
		if self.get_inst() > 1:
			raise myexception.MyExcept('Balancer instance cannot be more than one')	
		self.incr_inst()
		self.tr = None
		self.queue = Queue.PriorityQueue()
		self.sched_data = {}
		self.node_hash = {}
		self.score_q = MyPrioQ()
		self.lock = multiprocessing.Lock()
		self.age_threshold = age_threshold # default 5 minutes

	def __repr__(self):
		return "%s" % self.score_q

	def send_trigger(self, node, port='5556'):
		self.tr = trigger.PairClient(node)
		self.tr.send_msg()

	def get_q(self):
		return self.queue.get(timeout=0.5)		

	def put_q(self, score=100):
		self.queue.put(score, timeout=0.5)
	
	def put_data(self, data):

		def wrapper(self, data):
			self.lock.acquire()
			if data['final_score'] not in self.sched_data:
				self.sched_data[data['final_score']] = []

			self.sched_data[data['final_score']].append(data)
			self.node_hash[data['node']] = data['age']
			self.score_q.put(data['node'], data['final_score'])
			self.lock.release()
		
		multiprocessing.Process(target=wrapper, args=(self, data)).start()

	def get_node(self):
		
		def wrapper(self):
			self.lock.acquire()
			node = self.score_q.get()
			p_node = node
			now = time.time()	
			if (now - self.node_hash[node]) >= self.age_threshold: 	
				self.send_trigger(node)
				node = self.score_q.get()

			del self.node_hash[node]
			self.lock.release()	
			self.send_trigger(node)




def main():
	import string
	import random
	bal = Balancer()
	for i in range(100):
		data = {}
		data['node'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
		data['age'] = 0
		data['final_score'] = random.randint(1, 100)

		bal.put_data(data)


	print bal
	bal.get_node()


if __name__ == '__main__':
	main()
