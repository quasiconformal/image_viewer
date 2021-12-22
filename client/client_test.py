from __future__ import print_function

import logging

import cv2
import numpy as np

import grpc

import my_if_pb2
import my_if_pb2_grpc

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    addr = 'localhost:50051'
    with grpc.insecure_channel(addr, options=[
        ('grpc.max_send_message_length', 50 * 1024 * 1024),
        ('grpc.max_receive_message_length', 50 * 1024 * 1024)
        ]) as channel:
        stub = my_if_pb2_grpc.GrpcViewerStub(channel)
        response = stub.SayHello(my_if_pb2.GrpcViewerHelloRequest(name='you'))
        print("Greeter client received: " + response.message)

        img = cv2.imread("leaf.jpg")
        print(img.shape)
        w = img.shape[1]
        h = img.shape[0]
        ch = 3
        type = 0
        action = "check"
        data = img.tobytes()
        req = my_if_pb2.GrpcViewerActionRequest(action = action, 
            width = w, height = h, ch = ch, type = type, data = data)
        resp = stub.DoAction(req)
        data = resp.data
        img = np.frombuffer(data, dtype="uint8")
        img = np.reshape(img, (h, w, ch))
        cv2.imwrite("resp.png",img)




if __name__ == '__main__':
    logging.basicConfig()
    run()