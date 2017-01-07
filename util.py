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
		sys.stderr.write("Starting time: {:}\n".format(self._start))


	def step(self):
		if self._n%self._step==0:
			averagetime = float((datetime.datetime.now()-self._start).seconds)/self._n
			if self._tag is not None:
				sys.stderr.write(self._tag+", progress: {:}, average time per step: {:} seconds.\n".format(self._n,averagetime))
			else:	
				sys.stderr.write("progress: {:}\n,average time per step: {:}\n".format(self._n,averagetime))

		self._n+=1

	def info(self,infos):
		sys.stderr.write("INFO: {:}\n".format(infos))

	def error(self,error):
		sys.stderr.write("ERROR: {:}\n".format(error))


	def end(self):
		sys.stderr.write("Ending time: {:}\n".format(datetime.datetime.now()))
		if self._tag is not None:
			sys.stderr.write("{:} counting done, total count: {:}, takes {:} seconds.\n".format(self._tag,self._n,(datetime.datetime.now()-self._start).seconds))
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

