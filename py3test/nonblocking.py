#!/usr/bin/env python3
# encoding: utf-8

import socket
import time

# http://python.jobbole.com/88291/


def noblocking_way():
    sock = socket.socket()
    # socket上阻塞调用都改为非阻塞的方式
    sock.setblocking(False)

    try:
        sock.connect(('baidu.com', 80))
    except BlockingIOError:
        # 非阻塞连接过程中也会抛出异常
        pass
    request = 'GET / HTTP/1.0\r\nHost: baidu.com\r\n\r\n'
    data = request.encode('ascii')

    # 不知道socket何时就绪，所以不断尝试发送
    while True:
        try:
            sock.send(data)
            # 直到send不抛异常，则发送完成
            break
        except OSError:
            pass

    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            break
        except OSError:
            pass
    return response


def sync_way():
    res = []
    for i in range(10):
        res.append(noblocking_way())
    return len(res)


def main():
    start = time.time()
    print(start)
    print(sync_way())
    print(time.time() - start)


if __name__ == '__main__':
    main()
