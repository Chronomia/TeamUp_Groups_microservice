import os

from google.cloud.sql.connector import Connector, IPTypes
import pymysql

import sqlalchemy


def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.
    Uses the Cloud SQL Python Connector package.
    """
    
    instance_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME') # e.g. 'project:region:instance'
    db_user = os.environ.get('CLOUD_SQL_USERNAME')  # e.g. 'my-db-user'
    db_pass = os.environ.get('CLOUD_SQL_PASSWORD')  # e.g. 'my-db-password'
    db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')  # e.g. 'my-database'


    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    connector = Connector(ip_type)

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # ...
    )
    return pool
