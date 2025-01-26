class Server:
    def __init__(self, id: int):
        self.id = id
        self.music_queue = []

    def get_serv_info(self):
        print(f"id: {self.id}, queue: {self.music_queue}")