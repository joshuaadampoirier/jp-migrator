/*  ****************************************************************************

Table definition for the _MigrationsRun table, keeping track of which migration 
scripts have been executed against the database.

***************************************************************************** */

CREATE TABLE IF NOT EXISTS _MigrationsRun 
(
    Id              BIGINT          NOT NULL 
                                    AUTO_INCREMENT
    ,Migration      TEXT            NOT NULL 
    ,DateRun        DATETIME        NOT NULL 
    ,PRIMARY KEY    (Id)
);