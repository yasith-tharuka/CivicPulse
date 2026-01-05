#!/usr/bin/env python3
"""
Helper script to run SQL commands on civicpulse.db
Usage: python db_helper.py "SELECT * FROM users;"
"""

import sys
import sqlite3

if len(sys.argv) < 2:
    print("Usage: python db_helper.py \"SQL_COMMAND\"")
    sys.exit(1)

conn = sqlite3.connect("civicpulse.db")
conn.row_factory = sqlite3.Row  # This allows column access by name
cursor = conn.cursor()

try:
    cursor.execute(sys.argv[1])
    
    # Check if it's a SELECT query (returns rows)
    if cursor.description:
        rows = cursor.fetchall()
        if rows:
            # Print column names
            columns = [description[0] for description in cursor.description]
            print(" | ".join(columns))
            print("-" * 50)
            # Print rows
            for row in rows:
                print(" | ".join(str(value) for value in row))
        else:
            print("No rows returned")
    else:
        # For INSERT, UPDATE, DELETE, etc.
        conn.commit()
        print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
    
except Exception as e:
    conn.rollback()
    print(f"Error: {e}")
finally:
    conn.close()

