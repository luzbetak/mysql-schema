SELECT 
  CONCAT(
    'CREATE TABLE ', tables.table_schema, '.', tables.table_name, ' (\n', 
    GROUP_CONCAT(
      CONCAT('  ', columns.column_name, ' ', columns.column_type, 
             IF(columns.IS_NULLABLE = 'NO', ' NOT NULL', ''), 
             IF(columns.column_default IS NOT NULL, CONCAT(' DEFAULT ', columns.column_default), ''), 
             IF(columns.extra <> '', CONCAT(' ', columns.extra), '')
      ), 
      '\n'
    ),
    IF(
      (SELECT COUNT(*) 
       FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS usage2
       WHERE usage2.table_schema = tables.table_schema 
         AND usage2.table_name = tables.table_name 
         AND usage2.REFERENCED_COLUMN_NAME IS NOT NULL
      ) > 0, 
      CONCAT(
        ',\n  ', 
        GROUP_CONCAT(
          DISTINCT CONCAT(
            'CONSTRAINT ', usage.constraint_name, ' FOREIGN KEY (', usage.column_name, ') REFERENCES ', usage.referenced_table_name, ' (', usage.referenced_column_name, ')'
          ) 
          SEPARATOR ',\n  '
        )
      ), 
      ''
    ),
    '\n) ENGINE=', tables.engine, ' CHARSET=', tables.table_collation, ';\n'
  ) AS CreateTable
FROM 
  INFORMATION_SCHEMA.TABLES AS tables
  JOIN INFORMATION_SCHEMA.COLUMNS AS columns
    ON tables.table_schema = columns.table_schema 
       AND tables.table_name = columns.table_name
  JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS `usage`
    ON usage.table_schema = tables.table_schema 
       AND usage.table_name = tables.table_name
WHERE 
  tables.table_schema = 'your_database_name'
GROUP BY 
  tables.table_schema, 
  tables.table_name, 
  tables.engine, 
  tables.table_collation;

