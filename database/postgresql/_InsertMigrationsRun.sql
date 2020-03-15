/*  Insert migration into the _MigrationsRun table.
***************************************************************************** */
DROP PROCEDURE IF EXISTS public._insert_migrationsrun(TEXT);


CREATE OR REPLACE PROCEDURE public._insert_migrationsrun 
(
    migration_name  TEXT 
)
LANGUAGE plpgsql 
AS $$ 
BEGIN 


    INSERT INTO public._migrationsrun 
    (
        migration 
        ,daterun 
    )
    VALUES 
    (
        migration_name 
        ,NOW()
    );
    

    COMMIT;

END;
$$;