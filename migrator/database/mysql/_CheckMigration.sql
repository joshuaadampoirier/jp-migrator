CREATE FUNCTION _Check_Migration
(
    migration_name INT
)
RETURNS INT DETERMINISTIC 

BEGIN  


    DECLARE     migration_exists    BIT DEFAULT 0;


    SELECT      CASE 
                    WHEN    COUNT(1) > 0
                    THEN    1
                    ELSE    0
                    END
    INTO        migration_exists    
    FROM        _MigrationsRun 
    WHERE       Migration = migration_name;


    RETURN migration_exists;


END;