# Basics

Login to mysql
```bash
mysql -u root -p
```

Create a database
```sql
CREATE DATABASE <dbname>;
```

Show all databases
```sql
SHOW DATABASES;
```

Select a database
```sql
USE <dbname>;
```

See all the tables in the db
```sql
SHOW TABLES;
```

Get more info about the database fields
```sql
DESCRIBE <table>;
```

Delete a row from a table
```sql
DELETE FROM <table> WHERE name = “reserved”;
```

Delete a column
```sql
ALTER TABLE <table> DROP COLUMN <column name>;
```

Add a column of binary type set to 0
```sql
ALTER TABLE <table> ADD COLUMN <column name> TINYINT(1) DEFAULT 0;
```

Add a column of string type with 20 characters
```sql
ALTER TABLE <table> ADD COLUMN <column name> VARCHAR(20);
```

Changing a column name
```sql
ALTER TABLE <table> CHANGE <old name> <new name> VARCHAR(20);
```

Make a column bigger
```sql
ALTER TABLE <table> MODIFY <column name> VARCHAR(50);
```

# Getting records

Get all information
```sql
SELECT * FROM <table>;
```

Show all records where a field matches a value
```sql
SELECT * FROM <table> WHERE name = “whatever”;
```

Show all records where a field matches two values
```sql
SELECT * FROM <table> WHERE name = “whatever” AND phone_number = '3444444';
```

Show all records where a field matches one and excludes the other
```sql
SELECT * FROM <table> WHERE name = “whatever” AND phone_number != '3444444';
```

Show all records where a field contains a phrase
```sql
SELECT * FROM <table> WHERE name LIKE “bob%”;
```

Show all records where a field does not contains a phrase
```sql
SELECT * FROM <table> WHERE name NOT LIKE “bob%”;
```

Show all records where a field contains a phrase and order by another  field 
```sql
SELECT * FROM <table> WHERE name like “bob%” ORDER BY account_number;
```

Show unique column records
```sql
SELECT DISTINCT <column> FROM <table>;
```

# Backup and Restoring

Load a csv file into a table
```sql
LOAD DATA INFILE '/path/to/file' REPLACE INTO TABLE <table> FIELDS TERMINATED BY ',' LINES TERMINATED BY '\N';
```

Dump all databases for backup
```bash
mysqldump -u root -p –-opt > /tmp/all.sql
```

Dump one database for backup
```bash
mysqldump -u root -p –-databases [db name] >/tmp/db.sql
```

Dump a table from a database for backup
```bash
mysqldump -c -u root -p –-databases [db name] [table name] >/tmp/db.table.sql
```

Restore database from backup
```bash
mysql -u root -p [db name] < /path/to/backup.sql
```

Run a file filled with mysql commands
```bash
mysql -u root -p [db name] < /path/to/file.sql
```

# More advanced queries
Insert a new record
```sql
INSERT INTO Customers (Account_Number, Company_Name, Service_Type) 
values ('1111111', 'UNASSIGNED', 'FIBER');
```

Update records using critera
```sql
UPDATE Customers SET Account_Number = '1111111', Company_Name = 'UNASSGINED' where name = 'deleteme';
```

Write query results to file
```sql
SELECT Radio_MAC FROM Customers
where (Radio_MAC like '%ac:81:1%' OR Radio_MAC like '%20:10:7A%') INTO OUTFILE "/home/tbennett/outfile.csv"
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n';
```
