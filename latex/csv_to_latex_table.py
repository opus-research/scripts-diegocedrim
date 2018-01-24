import csv
import sys


class TableData:
    def __init__(self, rows, headers):
        self.rows = rows
        self.headers = headers
        self.widths = self.compute_widths()

    def compute_widths(self):
        widths = {}
        for row in self.rows:
            for header in self.headers:
                widths[header] = max(widths.get(header, 0), len(row[header]), len(header))
        return widths


def read_rows(file_name):
    rows = []
    with open(file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append(row)
        headers = reader.fieldnames

    return TableData(rows, headers)


def print_row(row, table_data, print_keys=False):
    markdown = [""]
    for key in table_data.headers:
        value = row[key] if not print_keys else key
        width = table_data.widths[key]
        markdown.append(("%-" + str(width+1) + "s& ") % value)
    print "".join(markdown).strip("& ") + " \\\\"



def print_markdown(table_data):
    print_row(table_data.headers, table_data, True)
    for row in table_data.rows:
        print_row(row, table_data)


table_data = read_rows("/Users/diego/Downloads/export (44).csv")
# table_data = read_rows(sys.argv[1])
print_markdown(table_data)
