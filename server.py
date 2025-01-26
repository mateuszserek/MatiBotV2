class Server:
    def __init__(self, id: int):
        self.id = id
        self.music_queue = []
        self.is_playing_on_vc = False

    def get_serv_info(self):
        print(f"id: {self.id}, queue: {self.music_queue}, is_playing: {self.is_playing_on_vc}")