import pkg_resources 
import pytest

from psycopg2 import OperationalError 

from migrator.database.PostgreSQLDatabase import PostgreSQLDatabase 
from migrator.server.PostgreSQLServer import PostgreSQLServer
from tests.helper import run_script


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


@pytest.mark.skipif(not _connected(), reason="Not connected to PostgreSQL database server")
@pytest.fixture(scope="module")
def testing_database(testing_server: PostgreSQLServer) -> PostgreSQLDatabase:
    return testing_server.get_database()


@pytest.mark.skipif(not _connected(), reason="Not connected to PostgreSQL database server")
def test_database_type(testing_database):
    assert isinstance(testing_database, PostgreSQLDatabase)


@pytest.mark.skipif(not _connected(), reason="Not connected to PostgreSQL database server")
@pytest.mark.parametrize(
    "script_path, expected_result",
    [
        ("postgresql/test_migrations_run.sql", "_migrationsrun"),
        ("postgresql/test_insert_migrations_run.sql", "_insert_migrations_run"),
        ("postgresql/test_check_migration.sql", "check_migration")
    ]
)
def test_migrations(testing_server: PostgreSQLServer, script_path: str, expected_result: str):
    path = pkg_resources.resource_filename(__name__, script_path)
    result = run_script(path=path, server=testing_server)

    assert result == expected_result
