import re
import os
import csv

with open('cleaned_psirt.csv', 'a') as csvfile1:
    filewriter = csv.writer(csvfile1, delimiter=',')
    filewriter.writerow(['Project', 'Product', 'Component', 'Found', 'Severity', 'ISSS',\
                         'ISOIB', 'DDTS', 'Title', 'RNE', 'Description', 'PSIRT'])

with open('cleaned_non_psirt.csv', 'a') as csvfile2:
    filewriter = csv.writer(csvfile2, delimiter=',')
    filewriter.writerow(['Project', 'Product', 'Component', 'Found', 'Severity', 'ISSS',\
                         'ISOIB', 'DDTS', 'Title', 'RNE', 'Description', 'PSIRT'])


with open('result_psirt.csv', mode='r') as csv_input:
    csv_reader = csv.DictReader(csv_input)
    for row in csv_reader:
        match1 = re.search(r'.*?CVE|CVSS|\$\$IGNORE-PSIRT.*', row["RNE"], re.M | re.I)
        match2 = re.search(r'.*?does not meet the criteria.*', row["PSIRT"], re.M | re.I)
        if match1 and not match2:
            row_data = []
            for value in row.values():
                row_data.append(value)
            with open('cleaned_psirt.csv', 'a') as csvfile_psirt:
                filewriter = csv.writer(csvfile_psirt, delimiter=',')
                filewriter.writerow(row_data)
        else:
            row_data = []
            for value in row.values():
                row_data.append(value)
            with open('cleaned_non_psirt.csv', 'a') as csvfile_non_psirt:
                filewriter = csv.writer(csvfile_non_psirt, delimiter=',')
                filewriter.writerow(row_data)