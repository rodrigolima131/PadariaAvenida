from backend.database.db import Database


class DML:
    def __init__(self):
        self.conn = Database().create_connection()