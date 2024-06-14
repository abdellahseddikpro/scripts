import grpc
import containerd_services_pb2_grpc as services
import containerd_services_pb2 as messages

class ContainerdClient:
    def __init__(self, socket_path="/run/containerd/containerd.sock"):
        self.channel = grpc.insecure_channel(f"unix://{socket_path}")
        self.client = services.ImagesStub(self.channel)

    def prune_images(self):
        request = messages.PruneRequest()
        response = self.client.Prune(request)
        for msg in response:
            print(msg)
