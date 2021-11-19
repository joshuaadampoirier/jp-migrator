import argparse
import logging
import os
from pathlib import Path
import yaml

from migrator.server.BaseServer import BaseServer
from migrator.server.SQLite3Server import SQLite3Server
from migrator.server.PostgreSQLServer import PostgreSQLServer

logging.basicConfig(
    filename='Migrate.log',
    level=logging.INFO,
    format='|'
    '%(asctime)-18s|'
    '%(levelname)-4s|'
    '%(module)-18s|'
    '%(filename)-18s:%(lineno)-4s|'
    '%(funcName)-18s|'
    '%(message)-32s|',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def _parse_args() -> argparse.Namespace:
    """Parses and validates command-line arguments. Generates help and usage
    messages.

    Parameters
    ----------
    None

    Returns
    -------
    args : argparse.Namespace
        Populated with values
    """
    parser = argparse.ArgumentParser(description='Parameters for jp-migrator')

    parser.add_argument(
        '--deployment-repo',
        type=str,
        help='Location of the git repo to be deployed'
    )

    parser.add_argument(
        '--deployment-branch',
        type=str,
        help='Branch of the git repo to be deployed'
    )

    # optional host argument
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Name or address of host server'
    )

    parser.add_argument(
        '--port',
        type=int,
        default=5432,
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


def _read_instructions() -> dict:
    """Read the database migration instructions. These are contained in the
    migrate.yaml file of the database project.

    Parameters
    ----------
    None

    Returns
    -------
    migrate : dict
        Database metadata and migration instructions

    Notes
    -----
    This function assumes that the current working directory is the root
    directory of the database project. If no migrate.yaml file is found, we
    throw an error.
    """
    try:
        stream = open('/deployment/migrate.yaml', 'r')
        migrate = yaml.safe_load(stream)
    except FileNotFoundError:
        logging.error('Database project must have migrate.yaml to be deployed.')
        raise FileNotFoundError

    return migrate


def _get_files(migrate: dict, folder: str) -> list:
    """Retrieve the list of migration files to execute.

    Parameters
    ----------
    migrate : dict
        Database migration instructions.

    folder : str
        Folder of migration scripts to execute.

    Returns
    -------
    files : list
        Migration files to be executed.
    """
    # initialize list of files
    files = []

    # recursively locate migration scripts
    if migrate['migrations'][folder]['recursive']:
        logging.info('Recursively locating {fo} migrations.'.format(fo=folder))

        pathlist = Path('/deployment/' + folder).glob('**/*.sql')
        for path in pathlist:
            files.append(str(path))

    # locate migration scripts
    else:
        logging.info('Locating {fo} migrations'.format(fo=folder))

        for f in os.listdir('/deployment/' + folder):
            filename = os.fsdecode(f)

            if filename.endswith('.sql'):
                files.append('/deployment/' + folder + '/' + filename)

    return files


def _order_files(migrate: dict, folder: str, files: list):
    """Re-order the migration files to ensure those listed by the migration
    instructions are executed first.

    Parameters
    ----------
    migrate : dict
        Database migration instructions.

    folder : str
        Folder of migration scripts to execute.

    files : List
        List of migration scripts, unordered.

    Returns
    -------
    None
    """
    logging.info('Reorder {fo} migrations per instructions.'.format(fo=folder))

    # reverse the list, such that we process the first item last
    migrate['migrations'][folder]['order'].reverse()

    # loop through the files to be ordered
    for f in migrate['migrations'][folder]['order']:
        if '/deployment/' + folder + '/' + f in files:
            files.insert(0, files.pop(files.index('/deployment/' + folder + '/' + f)))


def _remove_previously_run(server: BaseServer, migrate: dict, files: list) -> list:
    """
    Remove migration scripts which have been previously executed.

    Parameters
    ----------
    server : BaseServer
        Database server object.

    migrate : dict
        Database migration instructions.

    files : list
        List of migration scripts, ordered.

    Returns
    -------
    new_files : list
        List of migration scripts which need to be executed.
    """
    remove = []

    # loop through migration scripts
    for f in files:
        # if migration script already ran, remove from list
        if server.get_database().check_migration(f):
            remove.append(f)

    # only include new migration scripts
    new_files = [f for f in files if f not in remove]

    return new_files


def _run_migrations(server: BaseServer, files: list):
    """Execute the provided migration scripts.

    Parameters
    ----------
    server : BaseServer
        Database server object.

    files : list
        List of migration scripts to be executed.

    Returns
    -------
    None
    """
    database = server.get_database()

    # loop through migrations
    for migration in files:
        database.run_migration(migration)


def _get_server(args: argparse.Namespace, migrate: dict) -> BaseServer:
    """Connect to the server provided by the migration instructions.

    Parameters
    ----------
    args : argparse.Namespace
        argparse namespace containing command-line arguments

    migrate : dict
        Database migration instructions.

    Returns
    -------
    server : Database Server object.
    """
    if migrate['engine'] == 'SQLite3':
        server = SQLite3Server(migrate['dbname'])
    elif migrate['engine'] == 'PostgreSQL':
        server = PostgreSQLServer(
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port,
            dbname=migrate['dbname']
        )

    return server


def main():
    """
    Primary orchestration of database migration.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    args = _parse_args()

    # clone given database repository to deploy
    os.system('rm -rf /deployment')
    os.system(f'git clone -b {args.deployment_branch} --single-branch {args.deployment_repo} /deployment')

    # read database migration instructions
    migrate = _read_instructions()

    # connect to database server
    server = _get_server(args, migrate)

    # loop through the migration folders
    for folder in migrate['migrations']:

        # retrieve migration scripts
        files = _get_files(migrate, folder)

        # remove files which have already executed (unless to always be run)
        if not migrate['migrations'][folder]['always']:
            files = _remove_previously_run(server, migrate, files)

        # re-order migration scripts as necessary
        if files and 'order' in migrate['migrations'][folder].keys():
            _order_files(migrate, folder, files)

        # run the migration scripts
        if files:
            _run_migrations(server, files)
            logging.info('{fo} successfully migrated.'.format(fo=folder))
        else:
            logging.info('{fo} up to date.'.format(fo=folder))

    logging.info('Database migrated successfully.')


if __name__ == '__main__':
    main()
