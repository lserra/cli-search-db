# csdb
CLI - Database Search Utility

================================================================================================
Pre-requisites:
================================================================================================
- Python version 2.7 or above
- MySQL 5.1 or above
- Package/Library MySQLdb

================================================================================================
How-To:
================================================================================================
Usage:
- The user calls it from the command line (that is, shell prompt)
- The search term is defined at the time of calling
- If the -t flag is issued, the following term is the table to be used; default is to search all tables
- If the -c flag is issued, the output is formatted by colunm
- If the -f flag is issued, the output is formatted by table
- If the -o flag is issued, the output is written to the given file

Part 1: Command-Line, the arguments for optparse that would be required are:
- [0] the command itself, naturally
- [1] the flag -t
- [2] the table name
- [3] the flag -c
- [4] the column name
- [5] the flag -f
- [6] the flag -o
- [7] the output file name
- [8] the search string for the query

Part 2: MySQL Database, are necessary to define the parameters to the connection:
- HOST = ''
- USER = ''
- PWD = ''
- DB = ''

Example:
- $ ./csdb.py -t table_name -c col_name -f -o output_file_name -q filter

So, the results can be show to screen or export to an external file (csv)

================================================================================================
History:
================================================================================================
- Version 1.0 - 09/04/2013 - Coding this first version
- Version 1.1 - 15/04/2013 - Add try/except

================================================================================================
Issues:
================================================================================================
- Unknow

================================================================================================
Next Activities:
================================================================================================
- No activity
