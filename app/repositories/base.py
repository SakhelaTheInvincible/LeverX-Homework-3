from mysql.connector import MySQLConnection


class BaseRepository:
    def __init__(self, connection: MySQLConnection) -> None:
        self.connection = connection
