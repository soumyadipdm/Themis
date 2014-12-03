import multiprocessing

if __name__ == '__main__':	
	class test:
		def __init__(self):
			self.arr = [x for x in range(1, 51)]	
	
		def cube(self):
			self.arr = [i**3 for i in self.arr]
	
	
	t = test()
	
	def func(x):
		print x**3
	
	pool = multiprocessing.Pool(processes=4)
	pool.map(func, (3,45, 12))
	pool.close()
	pool.join()
	
