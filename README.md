# jp-migrator
Tool enabling managing database schema changes through source control.

## Installation 
To install **jp-migrator**, clone the repo and install using pip as described 
below.

> $ git clone https://github.com/joshuaadampoirier/jp-migrator  
> $ cd jp-migrator  
> $ pip install .

## Deployments 
To run deploy a database using the **jp-migrator**, from the terminal navigate 
to the directory containing the database project you wish to deploy. This 
directory requires the *migrate.yaml* file providing deployment instructions to 
the **jp-migrator**.

> $ python  
> \>\>\>   from migrator.migrate import main  
> \>\>\>   main()

## Testing 
**jp-migrator** leverages Python's `unittest` library to perform unit tests. You
can run the tests by running the following command from the terminal within the 
**jp-migrator** directory.

> $ python -m unittest discover 

## Getting Started 

### SQLite3 
SQLite3 has no external dependencies you need to install. 

We have implemented w3Resources' Model database as an SQLite3 example 
for how to get started using the **jp-migrator** with SQLite3 databases. You can 
find the SQLite3 repo [here](https://github.com/joshuaadampoirier/w3resourceModel). Feel 
free to clone/deploy/modify the database! Further information about this 
database can be found [here](https://www.w3resource.com/sql/sql-table.php).

### PostgreSQL 
Getting started with PostgreSQL, we followed [this](https://www.codementor.io/@engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb) tutorial for getting up 
and running on MacOS. 

We have transcribed MySQL's sample database into a PostgreSQL database which can 
be deployed using the **jp-migrator**. You can find the PostgreSQL repo 
[here](https://github.com/joshuaadampoirier/ClassicModels), feel free to 
clone/deploy/modify this database! Further information about this database can 
be found [here](https://www.mysqltutorial.org/mysql-sample-database.aspx).

### SQL Server 
Getting started with SQL Server, we followed [this](https://adamwilbert.com/blog/2018/3/26/get-started-with-sql-server-on-macos-complete-with-a-native-gui) tutorial for 
getting up and running on MacOS using Docker.