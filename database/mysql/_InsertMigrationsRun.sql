CREATE PROCEDURE _Insert_MigrationsRun 
(
    IN  migration_name      TEXT
)


/*  ****************************************************************************

Inserts the filenames of successfully executed migration scripts into the 
_MigrationsRun table.


Args
----

    migration_name      TEXT 
                        Filename of the migration script to be inserted into the 
                        _MigrationsRun table. 


***************************************************************************** */


BEGIN   


    INSERT INTO _MigrationsRun 
    (
        Migration 
        ,DateRun 
    )
    VALUES 
    (
        migration_name 
        ,UTC_TIMESTAMP()
    );
    

END; 