import pytest

from psycopg2 import OperationalError 
from psycopg2.extensions import connection 

from migrator.server.PostgreSQLServer import PostgreSQLServer 


def _connected() -> bool:
    try:
        _ = PostgreSQLServer(
            host='localhost',
            port='5432',
            dbname='testserver2'
        )
        connected = True
    except OperationalError:
        connected = False
    
    return connected


@pytest.fixture(scope="module")
def testing_server() -> PostgreSQLServer:
    try:
        server = PostgreSQLServer(
            host='localhost',
            port='5432',
            dbname='testserver2'
        )
    except OperationalError:
        server = None
    
    return server


@pytest.mark.skipif(not _connected(), reason="Not connected to Postgres database server")
def test_server_type(testing_server):
    assert isinstance(testing_server, PostgreSQLServer)


@pytest.mark.skipif(not _connected(), reason="Not connected to Postgres database server")
def test_connection_type(testing_server: PostgreSQLServer):
    assert isinstance(testing_server.get_connection(), connection)
