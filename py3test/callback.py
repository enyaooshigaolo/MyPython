#!/usr/bin/env python3
# encoding: utf-8

#http://python.jobbole.com/88291/

import socket
from selectors import DefaultSelector,EVENT_WRITE,EVENT_READ

selector = DefaultSelector()
stopped = False
urls_todo = {'/','/0','/1','/2','/3', '/4', '/5', '/6', '/7', '/8', '/9'}

class Crawler:
    def __init__(self,url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('baidu.com',80))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(),EVENT_WRITE,self.connected)
    
    def connected(self,key,mask):
        selector.unregister(key.fd)
        get = 'GET {0} HTTP/1.0\r\nHost: baidu.com\r\n\r\n'.format(self.url)
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd,EVENT_READ,self.read_response)
    
    def read_response(self,key,mask):
        global stopped
        # 如果响应大于4KB，下一次循环会继续读
        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True

def loop():
    while not stopped:
       # 阻塞, 直到一个事件发生
       events = selector.select()
       for event_key,event_mask in events:
           callback = event_key.data
           callback(event_key,event_mask)

if __name__ == '__main__':
    import time
    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)
        crawler.fetch()
    loop()

    print(time.time() -  start)

'''
代码异步执行的过程：
1、创建Crawler 实例；
2、调用fetch方法，会创建socket连接和在selector上注册可写事件；
3、fetch内并无阻塞操作，该方法立即返回；
4、重复上述3个步骤，将10个不同的下载任务都加入事件循环；
5、启动事件循环，进入第1轮循环，阻塞在事件监听上；
6、当某个下载任务EVENT_WRITE被触发，回调其connected方法，第一轮事件循环结束；
7、进入第2轮事件循环，当某个下载任务有事件触发，执行其回调函数；此时已经不能推测是哪个事件发生，
	因为有可能是上次connected里的EVENT_READ先被触发，也可能是其他某个任务的EVENT_WRITE被触发；
	（此时，原来在一个下载任务上会阻塞的那段时间被利用起来执行另一个下载任务了）
8、循环往复，直至所有下载任务被处理完成
9、退出事件循环，结束整个下载程序
'''