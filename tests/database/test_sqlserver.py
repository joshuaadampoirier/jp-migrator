import pkg_resources 
import pytest

from pymssql import OperationalError 

from migrator.database.SQLServerDatabase import SQLServerDatabase 
from migrator.server.SQLServer import SQLServer
from tests.helper import run_script


def _connected() -> bool:
    try:
        _ = SQLServer(
            server='localhost',
            port='1401',
            user='SA',
            password='BadPassword123',
            dbname='TestDatabaseName'
        )
        connected = True
    except OperationalError:
        connected = False

    return connected


@pytest.fixture(scope="module")
def testing_server() -> SQLServer:
    try:
        server = SQLServer(
            server='localhost',
            port='1401',
            user='SA',
            password='BadPassword123',
            dbname='TestDatabaseName'
        )
    except OperationalError:
        server = None

    return server


@pytest.mark.skipif(not _connected(), reason="Not connected to SQL Server database server")
@pytest.fixture(scope="module")
def testing_database(testing_server: SQLServer) -> SQLServerDatabase:
    return testing_server.get_database()


@pytest.mark.skipif(not _connected(), reason="Not connected to SQL Server database server")
def test_database_type(testing_database):
    assert isinstance(testing_database, SQLServerDatabase)


@pytest.mark.skipif(not _connected(), reason="Not connected to SQL Server database server")
@pytest.mark.parametrize(
    "script_path, expected_result",
    [
        ("sqlserver/test_check_migration.sql", "_Check_Migration"),
        ("sqlserver/test_insert_migrations_run.sql", "_Insert_MigrationsRun"),
        ("sqlserver/test_migrations_run.sql", "_MigrationsRun")
    ]
)
def test_migrations(testing_server: SQLServer, script_path: str, expected_result: str):
    path = pkg_resources.resource_filename(__name__, script_path)
    result = run_script(path=path, server=testing_server)

    assert result == expected_result
