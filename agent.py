#!/bin/env python

import sys, os
import checkmem, checkio, score

def main():
	mem = checkmem.CheckMem()
	mem.score_me()
	io = checkio.CheckIO()
	io.score_me()	

	print mem, '\n'
	print io
	print "Overall Score:", score.Score.my_score


if __name__ == '__main__':
	main()
