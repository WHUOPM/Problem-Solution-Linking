#coding:utf-8
import sys
import re
import datetime


class iters_logger:
	def __init__(self,step=100,tag=None):
		self._n=1
		self._step = step
		self._tag = tag
		self._start= datetime.datetime.now()
		sys.stderr.write("{:}, logger step size: {:}, start logging...\n".format(self._tag,self._step))
	


	def step(self):
		if self._n%self._step==0:
			if self._tag is not None:
				sys.stderr.write(self._tag+", progress: {:}\n".format(self._n))
			else:	
				sys.stderr.write("progress: {:}\n".format(self._n))

		self._n+=1

	def info(self,infos):
		sys.stderr.write("INFO: {:}\n".format(infos))

	def end(self):
		if self._tag is not None:
			sys.stderr.write(self._tag+" counting done, total count: {:}\n".format(self._n))
		else:
			sys.stderr.write("counting done, total count: {:}, takes {:} seconds.\n".format(self._n, (datetime.datetime.now()-self._start).seconds))


def remove_invalid_utf8(data):
    new_data,count = re.subn('[x00-x08x10x0Bx0Cx0E-x19x7F]'
        + '|[x00-x7F][x80-xBF]+'
        + '|([xC0xC1]|[xF0-xFF])[x80-xBF]*'
        + '|[xC2-xDF]((?![x80-xBF])|[x80-xBF]{2,})'
        + '|[xE0-xEF](([x80-xBF](?![x80-xBF]))|(?![x80-xBF]{2})|[x80-xBF]{3,})', '!', data)

    new_data,count = re.subn('xE0[x80-x9F][x80-xBF]'
            + '|xED[xA0-xBF][x80-xBF]', '?', new_data)

    return new_data

