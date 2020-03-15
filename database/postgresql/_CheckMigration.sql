/*  Checks to see if a given migration script has been previously executed 
    against the database.
***************************************************************************** */
DROP FUNCTION IF EXISTS public._check_migration(TEXT);


CREATE FUNCTION public._check_migration 
(
    migration_name      TEXT 
)
RETURNS     BOOLEAN AS $migration_exists$


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