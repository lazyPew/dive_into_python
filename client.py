import socket
import time

class ClientError(Exception):
    pass

class Client:
    def __init__(self,host,port,timeout = None):
        self.host = host
        self.port = port
        self.connection = socket.create_connection((self.host,self.port),timeout)
        
    def get(self,name):
        try:
            self.connection.sendall(f"get {name}\n".encode("utf8"))
            response = self.connection.recv(1024).decode()
            # if "ok\n" not in response or "\n\n" not in response:
            #     raise ClientError
            metric_dict = {}
            print(response)
            resp = str(response).split('\n')[1:-2]
            if str(response).split('\n',1)[0] != "ok" or not response.endswith("\n\n"):
                raise ClientError
            elif str(response) == "ok\n\n":
                return metric_dict
            print(resp)
            for m in resp:
                metrics = m.split(' ')
                # print(m)
                if len(metrics) == 3:
                    metric_key = metrics[0]
                    metric_value = float(metrics[1])
                    metric_timestamp = int(metrics[2])
                    metric_list = metric_dict.get(metric_key, [])
                    metric_list.append((metric_timestamp, metric_value))
                    metric_dict.update({metric_key: sorted(metric_list)})
                    # print(type(metric_timestamp))
                else:
                    raise ClientError
                # elif metrics not in [["b'ok"], [""], [""]]:
                #     raise ClientError
            print(metric_dict)
            return metric_dict

        except Exception:
            raise ClientError


    def put(self,name,numb,timestamp = None):
        try:
            timestamp = timestamp or int(time.time())
            self.connection.sendall(f"put {name} {numb} {timestamp}\n".encode("utf8"))
            response = self.connection.recv(1024)
            if response != b"ok\n\n":
                raise ClientError
            else:
                print(response.decode())
        except Exception:
            raise ClientError


host = "127.0.0.1"
port = 8888
timeout = 15
client = Client(host,port,timeout)
client.put("test_key", 0.5, timestamp=1150864247)
client.put("palm.cpudfg", 0.4, timestamp=1150864245)
client.put("palm.cpudfg", 0.6, timestamp=1150864242)
client.put("palm.cpu123", 0.3, timestamp=1150864247)
client.get("test_key")
