# Author: Vincent.chan
# Blog: http://blog.alys114.com

import os
import json
import hashlib
from socketserver import (TCPServer as TCP,StreamRequestHandler as SRH,ThreadingTCPServer as TCPThead)
import common
import constConfig
import subprocess



# 全局变量
HOST='127.0.0.1'
PORT=21567
BUFSIZ=8192
ADDR=(HOST,PORT)
CODING='utf-8'
VIR_PATH_PRE = constConfig.BASE_DIR + os.sep

# 类定义
class MyRequestHandler(SRH):
	def handle(self):
		while True:
			try:
				print('...connected from:',self.client_address)
				self.data  = self.request.recv(BUFSIZ).strip()
				self.data = self.data.decode('utf-8')
				# print(self.data)
				if self.data is None:
					break
				self.data = json.loads(self.data)
				action = self.data['action']
				if hasattr(self,action):
					func = getattr(self,action)
					func(self.data)

			except ConnectionAbortedError as e:
				print('Exception:', e)
				break

	def put(self, *args):
		'''
		接收上传的文件
		:return:
		'''
		cmd = args[0]
		file_name = cmd['file_name']
		file_size = cmd['file_size']
		# 返回状态码
		self.request.send('200-ok'.encode(CODING))
		server_path = VIR_PATH_PRE + file_name
		if os.path.isfile(server_path):
			f = open(server_path + '.new','wb')
		else:
			f = open(server_path, 'wb')

		receive_size = 0
		m = hashlib.md5()
		while receive_size < file_size:
			# 解决粘包问题：获取文件大小的数据，作为边界
			cur_buf_size = file_size - receive_size
			if cur_buf_size > BUFSIZ:
				cur_buf_size = BUFSIZ
			data = self.request.recv(cur_buf_size)
			receive_size += len(data)  # 注意:一定不能+cur_buf_size,要以实际收到的数据为准
			f.write(data)
			# print(receive_size,file_size)
			m.update(data)
		else:

			local_md5 = m.hexdigest()
			client_md5 = self.request.recv(BUFSIZ)
			if local_md5 == client_md5:
				print('201-file recv done.')
		f.close()

	def auth(self, *args):
		'''
		权限验证
		:param args:
		:return:
		'''
		# 获取参数
		cmd = args[0]
		user_name = cmd['user_name']
		password = cmd['password']
		# 获取用户信息
		user_info = common.jsonLoad(constConfig.USER_DB)
		auth_result = {'user_name':user_name,'result':False,'msg':'',
					   'user_home':'',
					   'limit_size':0,
					   'used_size':0
					   }
		# print(user_info)
		if user_info.keys().__contains__(user_name):
			if user_info[user_name][0] == password:
				self.user_name = user_name
				self.user_home_dir_server = 'data'+os.sep+user_name+os.sep
				auth_result['result'] = True
				auth_result['user_home'] = self.user_home_dir_server
				auth_result['limit_size'] = self.mb_covert(user_info[user_name][1])
				auth_result['used_size'] = self.getdirsize(VIR_PATH_PRE+self.user_home_dir_server)
			else:
				auth_result['msg'] = '501-校验失败：密码错误..'
		else:
			auth_result['msg'] = '502-校验失败：不存在该用户..'

		auth_result_json = json.dumps(auth_result)
		self.request.send(auth_result_json.encode(CODING))

	def get(self, *args):
		'''
		下载文件
		:param args:
		:return:
		'''
		cmd = args[0]
		file_name = cmd['file_name']
		server_path = VIR_PATH_PRE + file_name
		if os.path.isfile(server_path):
			file_size = os.stat(server_path).st_size
			# 发送文件大小到Client
			print(file_size)
			self.request.send(str(file_size).encode(CODING))
			# 等待Client确认
			info_confirm = self.request.recv(BUFSIZ)

			m = hashlib.md5()
			# 获取文件
			f = open(server_path, 'rb')
			for line in f:
				m.update(line)
				self.request.send(line)
			f.close()
			server_md5 = m.hexdigest()
			print('204-send done')
			self.request.send(server_md5.encode())

	def ls(self, *args):
		'''
		获取当前目录的信息
		:param args:
		:return:
		'''
		cmd = args[0]
		print(cmd)
		client_user_path = cmd['user_cur_dir']
		server_user_path = VIR_PATH_PRE + client_user_path
		print('server_user_path:',server_user_path)
		cmd_str = 'ls ' + server_user_path
		# print('cmd_str:',cmd_str)
		res = os.popen(cmd_str).read()
		print(res)
		run_info_length = len(res.encode())
		self.request.send(str(run_info_length).encode(CODING))
		client_reply = self.request.recv(BUFSIZ)
		print(client_reply)
		self.request.sendall(res.encode(CODING))


	def cd(self,*args):
		'''
		目录切换（服务器不动）
		:param args:
		:return:
		'''
		# 获取参数
		cmd = args[0]
		user_name = cmd['user_name']
		new_path = cmd['user_new_dir']
		auth_result = {'user_name': user_name, 'result': False, 'msg': ''}
		server_path  = VIR_PATH_PRE + new_path
		print(server_path)
		if os.path.isdir(server_path):
			auth_result['result'] = True
		else:
			auth_result['msg'] = '503-切换失败：目录不存在..'
		auth_result_json = json.dumps(auth_result)
		self.request.send(auth_result_json.encode(CODING))

	def mb_covert(self,limit_size):
		size = limit_size.upper().replace('MB', '')
		size = int(size)
		size = 1024 * 1024 * size
		return size

	def getdirsize(self,dir):
		file_size = 0
		for root, dirs, files in os.walk(dir):
			print(root, dirs, files)
			file_size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
		return file_size

# 函数
def main():
	# tcpServ = TCP(ADDR,MyRequestHandler) #单线程
	tcpServ = TCPThead(ADDR, MyRequestHandler)  #多线程
	tcpServ.allow_reuse_address = True #重用地址，即使客户端还没断开
	print('waiting for connection...')

	tcpServ.serve_forever()
	tcpServ.server_close()

# 主程序
if __name__ == '__main__':
	main()