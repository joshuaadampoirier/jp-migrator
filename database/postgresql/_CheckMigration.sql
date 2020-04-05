DROP FUNCTION IF EXISTS public._check_migration(TEXT);


CREATE FUNCTION public._check_migration 
(
    migration_name      TEXT 
)
RETURNS     BOOLEAN AS $migration_exists$

/* *****************************************************************************

Checks to see if a given migration exists.

Args
----

    @migration_name:    TEXT
                        Name of the migration script to check whether or not it
                        is found in the dbo._MigrationsRun table (i.e. whether 
                        or not the migration has been executed against this 
                        database).

Returns
-------

    @migration_exists:  BOOLEAN
                        TRUE if found (has been executed)
                        FALSE if not found (has not been executed)

***************************************************************************** */


DECLARE     migration_exists    BOOLEAN; 


BEGIN  


    SELECT      CASE 
                    WHEN    COUNT(1) > 0
                    THEN    TRUE 
                    ELSE    FALSE 
                    END     INTO migration_exists 
    FROM        public._migrationsrun 
    WHERE       migration = migration_name; 


    RETURN migration_exists; 


END;
$migration_exists$ LANGUAGE plpgsql;