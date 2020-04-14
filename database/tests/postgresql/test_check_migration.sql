/*  If _Check_Migrations function exists, it returns the name of the function. 
    If it does not exist, returns nothing.
***************************************************************************** */
SELECT      routine_name 
FROM        information_schema.routines
WHERE       routine_schema = 'public'
    AND     routine_name = '_check_migration'
    AND     routine_type = 'FUNCTION';