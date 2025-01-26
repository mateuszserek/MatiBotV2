from queue import Queue

class Server:
    def __init__(self, id: int):
        self.id = id
        self.music_queue = Queue

    def get_serv_info(self):
        print(self.id + " " + self.music_queue)