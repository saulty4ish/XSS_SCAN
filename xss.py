#-*-coding:utf-8 -*-
from selenium import webdriver
import time
import urlparse
import Queue
import threading
from selenium.webdriver.common.by import By

class xss_scan(object):
	def __init__(self,url,method,cookie={},threadnum=10,data={},filename=""):
		self.url=url
		self.method=method
		self.cookie=cookie
		self.threadnum=threadnum
		self.data=data
		self.param=[]
		self.headers={}
		self.targets=Queue.Queue()
		self.filename=filename
	
	def Analysis_url(self):
		if not "=" in self.url:
			exit()
		parsed_tuple=urlparse.urlparse(self.url)
		for p in parsed_tuple[4].split("&"):
			self.param.append(p.split("=")[0])
		self.url=parsed_tuple[0]+"://"+parsed_tuple[1]
	
	def Init_targets(self):
		with open(self.filename,"r") as f:	
			for payload in f.readlines():
				target=self.url+"?"
				payload=payload.strip()
				for p in self.param:
					target=target+p+"="+payload+"&"
				target=target.rstrip("&")
				self.targets.put(target)
	
	def work(self):
		while not self.targets.empty():
			url=self.targets.get()
			driver = webdriver.Chrome()
			driver.get(url)
			try:
				alert = driver.switch_to_alert()
				time.sleep(1)
				print (alert.text)  #打印警告对话框内容
				print "payload:"+url
				alert.accept()   #alert对话框属于警告对话框，我们这里只能接受弹窗
				driver.quit()
			except:
				driver.quit()
				continue
	def execute(self):
		threads = []
		for i in range(self.threadnum):
			t = threading.Thread(target=self.work)
			threads.append(t)
			t.start()
		for t in threads:
			t.join()
obj=xss_scan("http://p.abiz.com/bulk_buyer/haier?hrCatCode=1&key=111&sort=111","get",filename="xss.txt")
obj.Analysis_url()
obj.Init_targets()
obj.execute()

#POST类型，需要解析dom，难以自动化实现。
'''
表单：
<input class="test" type="button" name="222" value="test"/>
<input type="text" name="111">

解析：
loc=(By.NAME,'111')
loc1=(By.NAME,'222')
loc3 =(By.CLASS_NAME,'test')
loc4 =(By.LINK_TEXT,'用户登录')

driver = webdriver.Chrome()
driver.get('http://127.0.0.1/xss.php')
driver.find_element(*loc).send_keys("1111") //设置值
driver.find_element(*loc1).click()  //点击
time.sleep(1)
driver.quit()
'''

