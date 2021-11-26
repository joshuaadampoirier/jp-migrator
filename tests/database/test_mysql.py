import pkg_resources 
import pytest

from pymysql import OperationalError

from migrator.database.MySQLDatabase import MySQLDatabase 
from migrator.server.MySQLServer import MySQLServer
from tests.helper import run_script


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
@pytest.fixture(scope="module")
def testing_database(testing_server: MySQLServer) -> MySQLDatabase:
    return testing_server.get_database()


@pytest.mark.skipif(not _connected(), reason="Not connected to MySQL database server")
def test_database_type(testing_database):
    assert isinstance(testing_database, MySQLDatabase)


@pytest.mark.skipif(not _connected(), reason="Not connected to MySQL database server")
@pytest.mark.parametrize(
    "script_path, expected_result",
    [
        ("mysql/test_migrations_run.sql", "_MigrationsRun"),
        ("mysql/test_insert_migrations_run.sql", "_Insert_MigrationsRun"),
        ("mysql/test_check_migration.sql", "_Check_Migration")
    ]
)
def test_migrations(testing_server: MySQLServer, script_path: str, expected_result: str):
    path = pkg_resources.resource_filename(__name__, script_path)
    result = run_script(path=path, server=testing_server)

    assert result == expected_result
