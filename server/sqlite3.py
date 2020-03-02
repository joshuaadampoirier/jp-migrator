import sqlite3 

from server.base import BaseServer 


class SQLite3Server(BaseServer):
    '''
    SQLite3 server object.

    SQLite3 databases are actually serverless and have native python 
    connections, so they are easy to work with.

    Parameters 
    ----------
    dbname:     string 
                Name of the database to connect to. 

    cnxn:       database connection object
                Connection to the SQLite3 database.
    '''
    def __init__(self, dbname):
        self.dbname = dbname 
        self.cnxn = self.__establish_connection()

    def __del__(self):
        self.cnxn.close()

    def __establish_connection(self):
        '''
        Retrieve connection to the SQLite3 database server.

        Parameters 
        ----------
        None

        Returns
        -------
        cnxn:       connection object 
                    Open connection to the SQLite3 database server.
        '''
        cnxn = sqlite3.connect(
            'Database={database}.db'.format(database=self.dbname)
        )

        return cnxn 


def main():
    """
    Build a SQLite3 server object; connected to a SQLite3 database.

    Parameters
    ----------
        None
    Returns
    -------
        0
    """
    server = SQLite3Server('TestServer')
    print(server.dbname)


    return 0


if __name__ == '__main__':
    main()