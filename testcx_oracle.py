# myscript.py

from __future__ import print_function

import cx_Oracle

# Connect as user "hr" with password "welcome" to the "orclpdb1" service running on this computer.
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XE")
connection = cx_Oracle.connect("hr", "hr", dsn, encoding="UTF-8")
# connection = cx_Oracle.connect("hr", "hr", "localhost/xe")

cursor = connection.cursor()
cursor.execute("""
    SELECT first_name, last_name
    FROM employees
    WHERE department_id = :did AND employee_id > :eid""",
    did = 50,
    eid = 190)
for fname, lname in cursor:
    print("Values:", fname, lname)