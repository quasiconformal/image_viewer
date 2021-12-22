from concurrent import futures
import logging

import cv2
import numpy as np

import grpc
import my_if_pb2
import my_if_pb2_grpc


class GrpcViewerServer(my_if_pb2_grpc.GrpcViewerServicer):

    def SayHello(self, request, context):
        return my_if_pb2.GrpcViewerHelloReply(message='Hello, %s!' % request.name)
    
    def DoAction(self, request, context):

        action = request.action
        w = request.width
        h = request.height
        t = request.type
        data = request.data

        print("request message = ", action)

        img = np.frombuffer(data, dtype="uint8")
        img = np.reshape(img, (h, w, 3))
        cv2.imwrite("test.png",img)
        img2 = img.copy()
        data2 = img2.tobytes()

        resp = my_if_pb2.GrpcViewerActionResponse()
        resp.action = action
        resp.width = w
        resp.height = h
        resp.type = t
        resp.data = data2
        return resp


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_if_pb2_grpc.add_GrpcViewerServicer_to_server(GrpcViewerServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()