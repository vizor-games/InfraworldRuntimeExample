import grpc
from concurrent import futures
import time
from time import strftime
from time import gmtime
import vizor_demonstration_pb2
import vizor_demonstration_pb2_grpc


class VizorDemoServer(vizor_demonstration_pb2_grpc.HelloServiceServicer):
    def Hello(self, request: vizor_demonstration_pb2.HelloRequest, context):
        t = strftime("%H:%M:%S", gmtime())
        print(f'Hello request received from {request.name} {t}!')
        return vizor_demonstration_pb2.HelloResponse(message=f'Vizor Demo Server Greetings you, {request.name}!')

    def ServerTime(self, request, context):
        hours = strftime("%H", gmtime())
        minutes = strftime("%M", gmtime())
        seconds = strftime("%S", gmtime())
        timezone = strftime("%z", gmtime())
        location = 'Europe/Moscow'
        return vizor_demonstration_pb2.ServerTimeResponse(hours=hours, minutes=minutes,
                                                          seconds=seconds, timezone=timezone, location=location)


def start_server():
    print('Server Started!')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    vizor_demonstration_pb2_grpc.add_HelloServiceServicer_to_server(VizorDemoServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    start_server()
