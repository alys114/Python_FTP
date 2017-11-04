# Author: Vincent.chan
# Blog: http://blog.alys114.com

'封装了所有公共的内容'

# 1.标准库
import os
import json
import configparser
import pickle
import hashlib
# 2.第三方库
# 3.自定义库

##获取当前根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = BASE_DIR+os.sep+"conf"+os.sep+'setting.cnf'

# print(config_path)
c = configparser.ConfigParser()
c.read(config_path)

def jsonDump(data,filename):
	with open(filename,'w') as file_object:
		json.dump(data,file_object)


def jsonLoad(filename):
	with open(filename,'r') as file_object:
		# print(json.load(file_object))
		return json.load(file_object)


def ReadConfig(section,key):
	return c.get(section,key)


def SetConfig(section,key,value):
	c.set(section,key,value)
	c.write(open(config_path,'w'))

def ReadConfigSEQ(section,key):
	seq = ReadConfig(section,key)
	next_seq = int(seq)+1
	SetConfig(section,key,str(next_seq))
	return seq


def WriteToFile(data,filename):
	with open(filename, 'a') as file_object:
		file_object.write(data)


def pickleLoad(filename):
	with open(filename,'rb') as file_object:
		return pickle.load(file_object)


def pickleDump(data,filename):
	with open(filename,'wb') as file_object:
		pickle.dump(data,file_object)


def md5Encode(mes):
	md = hashlib.md5()
	md.update(mes.encode('utf8'))
	return md.hexdigest()

def errorPrompt(mes):
	print("\033[31m%s \033[0m" %mes)

def menuDisplay(mes):
	print("\033[36m%s \033[0m" % mes)


# print(md5Encode('123456'))