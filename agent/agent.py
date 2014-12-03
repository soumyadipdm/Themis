#!/bin/env python

import sys, os, socket, time
import json
#from qpid.messaging import *
import checkmem, checkio, score


def timer_d(func):
	def wrapper(*args, **kwargs):
		start_time = time.time()	
		func(*args, **kwargs)
		end_time = time.time()
		tot_time = end_time - start_time
		return func
	return wrapper 

#@timer_d
def score_now(mem_context=True, io_context=True):
	mem_deducted, io_deducted = 0, 0
	if mem_context:
		mem = checkmem.CheckMem()
		mem.score_me()
		mem_deducted = mem.score_deducted

	if io_context:
		io = checkio.CheckIO()
		io.score_me()
		io_deducted = io.score_deducted

	return (score.Score.get_score(), score.Score.get_time(), mem_deducted, io_deducted)

def send_msg(msg, broker='localhost:5672', topic='amq.topic'):
	
	connection = Connection(broker)	

	try:
		connection.open()
		session = connection.session()
		sender = session.sender(topic)
		receiver = session.receiver(topic)

		sender.send(Message(msg))
		message = receiver.fetch()
		print message.content
		session.acknowledge()
	except MessagingError, m:
		print m
	finally:	
		connection.close()

def main():
	fqdn = socket.getfqdn(socket.gethostname())
	
	data = dict(zip(['final_score', 'age', 'mem_deducted', 'io_deducted'], list(score_now())))

	data['node'] = fqdn
	json_str = json.dumps(data)
	#send_msg(json_str)
	print json_str

if __name__ == '__main__':
	main()
