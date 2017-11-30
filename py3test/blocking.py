#!/usr/bin/env python3
# encoding: utf-8

# http://python.jobbole.com/88291/

import socket
from concurrent import futures


def blocking_way():
    sock = socket.socket()
    # block
    sock.connect(('baidu.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: baidu.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        # blocking
        chunk = sock.recv(4096)
    return response


def thread_way():
    worker = 10
    with futures.ThreadPoolExecutor(worker) as executor:
        futs = {executor.submit(blocking_way) for i in range(10)}
    return len([fut.result() for fut in futs])


def process_way():
    worker = 10
    with futures.ProcessPoolExecutor(worker) as executor:
        futs = {executor.submit(blocking_way) for i in range(10)}
    return len([fut.result() for fut in futs])


def sync_way():
    res = []
    for i in range(10):
        res.append(blocking_way())
    return len(res)


def main():
    start = time.time()
    print(start)
    # print(sync_way())   #0.752
    # print(process_way())    #0.527
    print(thread_way())  # 0.089

    print(time.time() - start)


if __name__ == '__main__':
    import time
    main()
