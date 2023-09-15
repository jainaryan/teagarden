from datetime import datetime
import openpyxl
from sqlalchemy.sql import text
from sqlapp.dataimport.rainfall_excel_file_reader1 import rainfall_type_1_reader
from sqlapp.dataimport.excel_file_reader2 import type_2_reader
from sqlapp.models import *
from sqlapp.database import db_session, init_db, engine, conn
import os


def read_workbook(workbook):
    first_sheet = True
    workbook = workbook
    for sheet in workbook.worksheets:
        if (first_sheet):
            type = sheet.cell(row = 9, column = 2).value
            if (type == 'rainfall1'):
                rainfall_type_1_reader(workbook)
            elif (type == 2):
                type_2_reader(workbook)
        else:
            break




