import pytest
from sqlite3 import Connection

from migrator.server.SQLite3Server import SQLite3Server 


@pytest.fixture(scope="module")
def testing_server() -> SQLite3Server:
    server = SQLite3Server("TestServer")
    return server


def test_server_type(testing_server):
    assert isinstance(testing_server, SQLite3Server)


def test_connection_type(testing_server: SQLite3Server):
    assert isinstance(testing_server.get_connection(), Connection)
