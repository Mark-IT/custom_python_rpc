# -*- coding: utf-8 -*-

import json
import time
import struct
import socket


def rpc(sock, in_, params):
    request = json.dumps({'in': in_, 'params': params})  # 请求消息体
    length_prefix = struct.pack('I', len(request))  # 将一个整数(请求消息体的长度)编码成 4 个字节的字符串
    sock.sendall(length_prefix)  # 先发送请求体长度
    sock.sendall(request.encode('utf-8'))  # 再发送实际请求消息
    length_prefix = sock.recv(4)  # 接收响应内容的长度
    length = struct.unpack('I', length_prefix)[0]  # 将一个 4 字节的字符串解码成一个整数,获取实际消息长度
    body = sock.recv(length).decode('utf-8')  # 根据消息长度接收响应内容
    print('body', body)
    response = json.loads(body)
    return (response['out'], response['result'])


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8080))
    for i in range(10):
        out, result = rpc(s, in_='ping', params='ireader %d' % i)
        print(out, result)
        time.sleep(1)  # 休眠 1s，便于观察
    s.close()  # 关闭连接
