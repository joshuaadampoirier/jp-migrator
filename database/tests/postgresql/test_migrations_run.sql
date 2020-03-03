/*  If _MigrationsRun table exists, it returns the name of the table. If it does
    not exist, returns nothing.
***************************************************************************** */
SELECT      table_name 
FROM        information_schema.tables
WHERE       table_schema = 'public'
    AND     table_name = '_migrationsrun';