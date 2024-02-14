import logging
import os

from psycopg_pool import AsyncConnectionPool


class PGConnectionPoolFactory:
    __min_connections: int
    __max_connections: int

    def __init__(self):
        self.__min_connections = 1
        self.__max_connections = 300
        self.__db_host = os.environ['POSTGRES_HOST']
        self.__db_username = os.environ['POSTGRES_USERNAME']
        self.__db_password = os.environ['POSTGRES_PASSWORD']
        self.__db_port = os.environ['POSTGRES_PORT']
        self.__db_name = os.environ['POSTGRES_DB_NAME']

    def create(self):
        return AsyncConnectionPool(
            min_size=self.__min_connections,
            max_size=self.__max_connections,
            conninfo=" ".join((
                f"host={self.__db_host}",
                f"port={self.__db_port}",
                f"dbname={self.__db_name}",
                f"user={self.__db_username}",
                f"password={self.__db_password}",
            ))
        )
