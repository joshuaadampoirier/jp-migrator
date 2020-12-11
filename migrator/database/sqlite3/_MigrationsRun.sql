/*  Assumes >= SQLite3 3.3. Earlier versions do not support IF EXISTS.
***************************************************************************** */
CREATE TABLE IF NOT EXISTS _MigrationsRun 
(
    Id              INTEGER         NOT NULL 
                    PRIMARY KEY     AUTOINCREMENT 
    ,Migration      TEXT            NOT NULL 
    ,DateRun        TEXT            NOT NULL 
)