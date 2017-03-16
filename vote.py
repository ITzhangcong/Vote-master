# /etc/bin/env python
# coding:utf-8


import sys
import requests
import time
import threading
from Queue import Queue

try:
	import requests.packages.urllib3
	requests.packages.urllib3.disable_warnings()
except:
	pass


class Vote(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global ticket
		while queue_ip.qsize() > 0:
			ip = queue_ip.get()
			for i in xrange(10):
				try:
					proxies = {"http": "http://" + ip}
					r = requests.post('http://star.rayli.com.cn/services/service.php?m=vote&a=do', data=payload, timeout=1, proxies=proxies)
					if r.status_code == 200:
						print 'success'
						ticket += 1
					time.sleep(1)
				except requests.exceptions.ReadTimeout:
					pass
				except requests.exceptions.ConnectionError:
					break
				except:
					pass


if __name__ == '__main__':
	uid = sys.argv[1]
	sid = sys.argv[2]
	queue_ip = Queue(0)
	proxies_list = []
	payload = {'uid': uid, 'sid': sid}
	threads = []
	ticket = 0
	num = 10

	with open("proxy_ip.txt", 'r') as f:
		for i in f.readlines():
			queue_ip.put(i.strip())

	for i in xrange(0, num):
		threads.append(Vote())

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	print '共投%d票' % ticket
