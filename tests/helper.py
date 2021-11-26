import pytest

from migrator.server.BaseServer import BaseServer


def run_script(path: str, server: BaseServer) -> str:
    # load SQL query
    f = open(path, "r")
    sql = f.read()
    f.close()

    # connect to database and execute query
    cursor = server.get_connection().cursor()
    cursor.execute(sql)
    result = cursor.fetchone()[0]

    return result