--db client:sqlcl

-- Change password
password

-- Better output
set sqlformat ansiconsole
set sqlformat fixed

-- Show columns in table
describe table_name

-- Show unique columns in table
select distinct animal from zoo

-- Show unique columns with an occurance count
select http_code, count(*) as num
FROM web_requests
GROUP BY http_code;

-- String Comparison
select name, animal
FROM zoo
WHERE animal = 'zebra';

-- NULL Comparison
select *
FROM web_requests
WHERE http_code is null;

-- ORACLE-specific LIMIT clause
SELECT owner, table_name FROM all_tables FETCH NEXT 2 ROWS ONLY;
