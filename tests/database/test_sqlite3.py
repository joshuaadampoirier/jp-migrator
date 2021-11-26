import pkg_resources 
import pytest

from migrator.database.SQLite3Database import SQLite3Database 
from migrator.server.SQLite3Server import SQLite3Server
from tests.helper import run_script


@pytest.fixture(scope="module")
def testing_server() -> SQLite3Server:
    server = SQLite3Server("TestServer")
    return server


@pytest.fixture(scope="module")
def testing_database(testing_server: SQLite3Server) -> SQLite3Database:
    return testing_server.get_database()


def test_database_type(testing_database):
    assert isinstance(testing_database, SQLite3Database)


@pytest.mark.parametrize(
    "script_path, expected_result",
    [("sqlite3/test_migrations_run.sql", "_MigrationsRun")]
)
def test_migrations_run(testing_server: SQLite3Server, script_path: str, expected_result: str):
    path = pkg_resources.resource_filename(__name__, script_path)
    result = run_script(path=path, server=testing_server)

    assert result == '_MigrationsRun'
