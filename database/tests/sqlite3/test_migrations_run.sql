/*  If _MigrationsRun table exists, it returns the name of the table. If it does
    not exist, returns nothing.
***************************************************************************** */
SELECT      name 
FROM        sqlite_master 
WHERE       type = 'table'
    AND     name = '_MigrationsRun'