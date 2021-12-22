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
    
    def make_resp(self, img, action, w, h, ch, t):
        data = img.tobytes()

        resp = my_if_pb2.GrpcViewerActionResponse()
        resp.action = action
        resp.width = w
        resp.height = h
        resp.ch = ch
        resp.type = t
        resp.data = data
        return resp

    def do_check(self, img, action, w, h, ch, t):
        img2 = img.copy()
        
        img2 = img - 100
        return img2

    def DoAction(self, request, context):

        action = request.action
        w = request.width
        h = request.height
        ch = request.ch
        t = request.type
        data = request.data

        print("request message = ", action)

        img = np.frombuffer(data, dtype="uint8") ##TODO:
        img = np.reshape(img, (h, w, ch))
        cv2.imwrite("request.png",img)
        

        img_resp = self.do_check(img, action, w, h, ch, t)
        print(img_resp.shape)
        cv2.imwrite("response.png",img_resp)
        return self.make_resp(img_resp, action, w, h, ch, t)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    my_if_pb2_grpc.add_GrpcViewerServicer_to_server(GrpcViewerServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()