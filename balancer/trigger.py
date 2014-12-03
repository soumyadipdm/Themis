'''This module sends a trigger message to the nodes
that have not sent their scores in the defined time
duration. Nodes will receive the trigger message and
send the scores to the balancer
ZeroMQ PAIR type socket is being used due to its flexibility
over traditional sockets
'''

import zmq

class PairClient:
	''' The ZMQ Pair Client'''
	def __init__(self, IP='127.0.0.1', PORT='5556'):
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.PAIR)	
		self.socket.connect("tcp://"+IP+":"+PORT)

	def __del___(self):
		self.socket.close()

	def send_msg(self, topic=None, msg="SCORE"):
		self.socket.send(topic+":"+msg)	

	def recv_msg(self):
		return self.socket.recv()
		



def main():
	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.bind("tcp://127.0.0.1:5556")

	pc = PairClient()
	for i in range(10):
		pc.send_msg("%d" % i)
		msg = socket.recv()
		print "message received: %s" % msg


if __name__ == '__main__':
	main()
		
