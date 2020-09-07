import asyncio

metrics_dict = dict()

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        # print(data.decode())
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def process_data(self,data):
        # print(data)
        info = data.strip("\n").split()
        try:
            action = info[0]
        except IndexError:
            action = ""
        if action == "put" and len(info) == 4:
            try:
                key, timestamp, value = info[1], int(info[3]), float(info[2])
                if key not in metrics_dict:
                    metrics_dict[key] = [(timestamp,value)]
                else:
                    for i in metrics_dict[key]:
                        if i[0] == timestamp:
                            metrics_dict[key].remove(i)
                            metrics_dict[key].append((timestamp,value))
                            metrics_dict[key].sort()
                            return "ok\n\n"
                    metrics_dict[key].append((timestamp,value))
                return "ok\n\n"
            except Exception:
                return "error\nwrong command\n\n"

        elif action == "get" and len(info) == 2:
            key = info[1]
            to_send = "ok\n"
            if key == "*":
                for key, item_list in metrics_dict.items():
                    item_list.sort()
                    for item_tuple in item_list:
                        try:
                            to_send += f'{key} {item_tuple[1]} {item_tuple[0]}\n'
                        except IndexError:
                            return "Index error"
                return to_send + '\n'
            else:
                metrics_list = metrics_dict.get(key)
                if metrics_list is None:
                    return "ok\n\n"
                try:
                    metrics_list.sort()
                    for metric in metrics_list:
                        to_send += f'{key} {metric[1]} {metric[0]}\n'
                    return to_send + '\n'
                except IndexError:
                    return "Index error"

        else:
            return "error\nwrong command\n\n"

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

# run_server('127.0.0.1', 8888)