#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Description: CLI - database search utility
-The user calls it from the command line (that is, shell prompt)
-The search term is defined at the time of calling
-If the -t flag is issued, the following term is the table to be used; default is to search all tables
-If the -c flag is issued, the output is formatted by colunm
-If the -f flag is issued, the output is formatted by table
-If the -o flag is issued, the output is written to the given file
Ex.: ./csdb.py -t <table> -c <col> -f -o <output.csv> -q <query>
"""

# =======================================================================================================
# Author: laercio.serra@gmail.com
# Versions:
# 1.0 - 09/04/2013 - Laercio Serra - Coding this first version
# 1.1 - 15/04/2013 - Laercio Serra - Add try/except
# =======================================================================================================

import optparse
import MySQLdb
import sys
import csv

# =======================================================================================================
# Part 1 - Command-Line
# The arguments for sys.argv that would be required are:
# -0 the command itself, naturally
# -1 the flag -t
# -2 the flag -c
# -3 the table name
# -4 the -f flag
# -5 the flag -o
# -6 the output file name
# -7 the search string for the query
# =======================================================================================================
# Create the object
opt = optparse.OptionParser()

# Usage: add arguments
# object.add_option (
# 						"-[short flag option]",
# 						"--[long flag option]",
# 						action="store",
# 						type="string",
# 						dest="[variable name under which to store the option]" )
opt.add_option("-t", "--table", action="store", type="string", dest="table")
opt.add_option("-c", "--col", action="store", type="string", dest="column")
opt.add_option("-f", "--format", action="store_true", dest="frmt")
opt.add_option("-o", "--output", action="store", type="string", dest="outfile")
opt.add_option("-q", "--query", action="store", type="string", dest="term")

# All the options are assigned. The first of the two values, opt , is an
# object containing the values of all the options passed to the program.
# The second value, args , is a list of any remaining arguments.
opt, args = opt.parse_args()

if opt.table is None and opt.column is None and opt.frmt is None \
        and opt.outfile is None and opt.term is None:
    print 'This is a CLI database search utility. Usage:'
    print '>> The user calls it from the command line (that is, shell prompt)'
    print '>> The search term is defined at the time of calling'
    print '>> If the -t flag is issued, the following term is the table to be used; default is to search all tables'
    print '>> If the -c flag is issued, the output is formatted by colunm'
    print '>> If the -f flag is issued, the output is formatted by table'
    print '>> If the -o flag is issued, the output is written to the given file'
    print 'Ex.: ./csdb.py -t <table> -c <col> -f -o <output.csv> -q <query>'
    sys.exit(1)

# Define the parameters of the statement
if opt.table is not None:
    table = opt.table
else:
    print 'Warning: The parameter -t <table> is necessary'
    sys.exit(1)

if opt.column is not None:
    column = opt.column
else:
    print 'Warning: The parameter -c <column> is necessary'
    sys.exit(1)

frmt = opt.frmt

if opt.outfile is not None:
    outfile = opt.outfile
else:
    print 'Warning: The parameter -o <output> is necessary'
    sys.exit(1)

if opt.term is not None:
    term = opt.term
else:
    print 'Warning: The parameter -q <term> is necessary'
    sys.exit(1)
# =======================================================================================================
# Part 2 - MySQL
# =======================================================================================================
# Define the parameters of the connection
HOST = '127.0.0.1'
USER = 'root'
PWD = ''
DB = 'search'

try:
    # Create and open a database connection
    db = MySQLdb.connect(HOST, USER, PWD, DB)

    # Create and open a cursor
    cur = db.cursor()
except MySQLdb.Error as err:
    print 'Connection Error - %s' % err
    sys.exit(1)

try:
    # Build the statement to populate the cursor
    statement = "SELECT * FROM %s WHERE %s LIKE \'%s\'" % (table, column, term)

    # Execute the statement to populate the cursor
    cur.execute(statement)

    # Return the result of the cursor and create a new object
    rst = cur.fetchall()
except MySQLdb.OperationalError as err:
    print 'Operational Error - %s' % err
    sys.exit(1)
except MySQLdb.ProgrammingError as err:
    print 'Programming Error - %s' % err
    sys.exit(1)

# Count and show in the screen the number of records found
print '>> RECORDS FOUND: %i' % len(rst)
print '=' * 50

# Fetch all the columns and data to output
columns_query = """DESCRIBE %s""" % table
columns_command = cur.execute(columns_query)
headers = cur.fetchall()
column_list = []
for record in headers:
    column_list.append(record[0])

cols = ''
for col in column_list:
    cols += col + ','

output = ''
for record in rst:
    fields = record
    for fds in fields:
        output += str(fds) + ','
    output += '\n'

# Show the data found to screen or export to an external file (csv)
if frmt is True:
    print cols
    print output

if outfile:
    with open(outfile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(column_list)
        writer.writerows(rst)
