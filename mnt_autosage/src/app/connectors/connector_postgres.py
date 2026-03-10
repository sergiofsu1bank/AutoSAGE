import os
import psycopg2
from src.app.tools.log_factory import get_dcp_logger


class ConnectorPostgres:

    def __init__(self, trace_id: str):

        self.logger = get_dcp_logger(
            trace_id=trace_id,
            classe="ConnectorPostgres"
        )

        self.host = os.getenv("MNT_DATABASE_HOST")
        self.port = os.getenv("MNT_DATABASE_PORT")
        self.database = os.getenv("MNT_DATABASE_NAME")
        self.user = os.getenv("MNT_DATABASE_USER")
        self.password = os.getenv("MNT_DATABASE_PASSWORD")

    def get_conn(self):

        conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

        return conn
