#coding:utf-8
import sys

class iters_logger:
	def __init__(self,step=100):
		self._n=0
		self._step = step

	def step(self):
		if self._n==0:
			sys.stderr.write("start counting...\n")
		elif self._n%self._step==0:
			sys.stderr.write("progress: {:}\n".format(self._n))

		self._n+=1

	def end(self):
		sys.stderr.write("counting done, total count: {:}\n".format(self._n))