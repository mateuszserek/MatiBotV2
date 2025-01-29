class Song:
    def __init__(self, query, duration, requested_by, title, url):
        self.title = title
        self.query = query 
        self.duration = duration
        self.requested_by = requested_by 
        self.url = url