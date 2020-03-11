import argparse 
import logging 
import yaml

from server.SQLite3Server import SQLite3Server 
from server.PostgreSQLServer import PostgreSQLServer

logging.basicConfig(
    filename='Migrate.log',
    level=logging.INFO,
    format='|' \
    '%(asctime)-18s|' \
    '%(levelname)-4s|' \
    '%(module)-18s|' \
    '%(filename)-18s:%(lineno)-4s|' \
    '%(funcName)-18s|' \
    '%(message)-32s|',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def _parse_args():
    '''
    Parses and validates command-line arguments. Generates help and usage 
    messageds.

    Parameters
    ----------
    None 

    Returns 
    -------
    args:       Namespace
                Populated with values
    '''
    parser = argparse.ArgumentParser(description='Parameters for jp-migrator')

    # optional host argument
    parser.add_argument(
        '--host', 
        type=str, 
        help='Name or address of host server'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        help='Port data is being served through'
    )
    
    parser.add_argument(
        '--user', 
        type=str, 
        help='Server login username'
    )
    
    parser.add_argument(
        '--password', 
        type=str, 
        help='Server login password'
    )

    args = parser.parse_args()
    return args


def _read_instructions():
    '''
    Read the database migration instructions. These are contained in the 
    migrate.yaml file of the database project.

    Parameters
    ----------
    None 

    Returns
    -------
    migrate:        Dictionary 
                    Database metadata and migration instructions

    Notes
    -----
    This function assumes that the current working directory is the root 
    directory of the database project. If no migrate.yaml file is found, we 
    throw an error.
    '''
    try:
        stream = open('migrate.yaml', 'r')
        migrate = yaml.safe_load(stream)
    except FileNotFoundError:
        logging.error('Database project must have migrate.yaml to be deployed.')
        raise FileNotFoundError 

    return migrate 


def _get_server(migrate):
    '''
    Connect to the server provided by the migration instructions.

    Parameters
    ----------
    migrate:        Dictionary
                    Database migration instructions.

    Returns
    -------
    server:         Database Server object.
    '''
    if migrate['engine'] == 'SQLite3':
        server = SQLite3Server(migrate['dbname'])

    return server 


def main():
    '''
    Primary orchestration of database migration.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    args = _parse_args()
    migrate = _read_instructions()

    server = _get_server(migrate)


if __name__ == '__main__':
    main()