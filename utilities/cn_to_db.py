import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utilities.models_db import db, CNumber
from flask import session


from flask import current_app

def cn_to_db(csv_file):
    # read the csv file
    with open(csv_file, 'r') as f:
        reader = csv.reader(f, delimiter=';') # f is the file object
        next(reader)  # skip the header
        data = list(reader)

    # insert the data into the cnumbers table
    with current_app.app_context():  # This line is necessary to avoid the error: "RuntimeError: No application found. Either work inside a view function or push an application context."
        for row in data:
            # Convert numeric strings to integers
            if len(row) == 7:
                for i in range(len(row)):
                    if row[i].isdigit():  # Check if the string represents a number
                        row[i] = int(row[i])  # Convert to integer
            print(f'row:----------> {row}')
            print(f'row length:----------> {len(row)}')

            cnumber = CNumber(l_type=row[0], treatment=row[1], h_condition=row[2], hsg_a=row[3], hsg_b=row[4], hsg_c=row[5], hsg_d=row[6])  # Update with the correct column names
            db.session.add(cnumber)

        db.session.commit()