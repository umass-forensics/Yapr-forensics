__author__ = 'Saksham'

import sqlite3
import argparse
import os
import zipfile


def main():

    parser = argparse.ArgumentParser(
        description="Recursively scans the directory structure for .zip files, extracts them, then looks for contact "
                    "databases, queries some of its tables and writes results to different files")

    parser.add_argument("-bp", help="The base directory for all images", type=str, dest="base_dir")
    parser.add_argument("-p", help="The path where the query results would be stored", type=str, dest="res_path")

    args = parser.parse_args()

    # extract zips
    for cur, dirs, files in os.walk(args.base_dir):
        for each_file in files:
            root, ext = os.path.splitext(each_file)
            if ext == ".zip":
                absolute_path = os.path.join(cur, each_file)
                Extract_zip_archive(absolute_path)
                print "Extracted filesystem dump: %s" % absolute_path

    # query contacts tables
    ctr = 1
    for cur, dirs, files in os.walk(args.base_dir):
        for each_file in files:
            root, ext = os.path.splitext(each_file)
            if each_file.startswith("contacts") and ext == ".db":
                absolute_path = os.path.join(cur, each_file)
                result = Query_database(absolute_path)
                result_file_path = os.path.join(args.res_path, str(ctr))
                Write_result_to_file(result_file_path, result)
                print "Written results from %s" % result_file_path
                ctr += 1


def Write_result_to_file(out_path, result):

    with open(out_path + ".txt", 'w') as writer:
        writer.write(result.encode('utf-8'))
    return

def Query_database(db_path):

    #db_path = 'H:\work_images\contacts2_id0633_v000_in_p008_htc_wildfire_a333.db'
    os.chmod(db_path, 444)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('select * from sqlite_master where type=\'table\';')

        all_tables = list(c.fetchall())

        table_names = set()
        for table in all_tables:
            table_names.add(table[1])

        rows_data = []
        rows_contacts = []
        rows_accounts = []
        rows_calls = []

        if table_names.__contains__('data'):
            c.execute('select * from data;')
            rows_data = list(c.fetchall())

        if table_names.__contains__('contacts'):
            c.execute('select * from contacts;')
            rows_contacts = list(c.fetchall())

        if table_names.__contains__('accounts'):
            c.execute('select * from accounts;')
            rows_accounts = list(c.fetchall())

        if table_names.__contains__('calls'):
            c.execute('select * from calls;')
            rows_calls = list(c.fetchall())

        all_results = db_path
        all_results += "\n\n" + Get_results_string(rows_data, rows_contacts, rows_accounts, rows_calls)

        return all_results

    except:
        return ""



def Get_results_string(data, contacts, accounts, calls):

    result = ""

    result += "DATA TABLE ROWS\n"
    result = Get_table_string(result, data) + "\n\n"

    result += "CONTACTS TABLE ROWS\n"
    result = Get_table_string(result, contacts) + "\n\n"

    result += "ACCOUNTS TABLE ROWS\n"
    result = Get_table_string(result, accounts) + "\n\n"

    result += "CALLS TABLE ROWS\n"
    result = Get_table_string(result, calls) + "\n\n"

    return result


def Get_table_string(running_str, all_rows):
    for row in all_rows:
        row_str = ""
        for col in row:
            if isinstance(col, int) or isinstance(col, float) or isinstance(col, str):
                row_str += str(col) + "\t"
            elif isinstance(col, unicode):
                row_str += unicode(col) + "\t"
        running_str += "\n" + row_str

    return running_str


def Extract_zip_archive(zip_path):

    dir = os.path.dirname(zip_path)

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            for name in z.namelist():
                try:
                    z.extract(name, dir)
                except:
                    pass
    except:
        pass

    return


if __name__ == '__main__':
    main()