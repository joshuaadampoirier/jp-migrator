import pymysql
import pytest

from pymysql.connections import Connection
from pymysql import OperationalError

from migrator.server.MySQLServer import MySQLServer 


def _connected() -> bool:
    try:
        _ = MySQLServer(
            server='localhost',
            port=3306,
            user='root',
            password='badpassword123',
            dbname='TestDatabaseName'
        )
        connected = True
    except OperationalError:
        connected = False
    
    return connected


@pytest.fixture(scope="module")
def testing_server() -> MySQLServer:
    try:
        server = MySQLServer(
            server='localhost',
            port=3306,
            user='root',
            password='badpassword123',
            dbname='TestDatabaseName'
        )
    except OperationalError:
        server = None

    return server


@pytest.mark.skipif(not _connected(), reason="Not connected to MySQL database server")
def test_server_type(testing_server):
    assert isinstance(testing_server, MySQLServer)


@pytest.mark.skipif(not _connected(), reason="Not connected to MySQL database server")
def test_connection_type(testing_server):
    assert isinstance(testing_server.get_connection(), Connection)
