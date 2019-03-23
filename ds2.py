import re
import os
import csv

path = 'b1517'
os.chdir(path)

with open('result_psirt.csv', 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Project', 'Product', 'Component', 'Found', 'Severity', 'ISSS',\
                         'ISOIB', 'DDTS', 'Title', 'Description', 'RNE'])

filelist = []

for filename in os.listdir(os.getcwd()):
    with open(filename, encoding = "ISO-8859-1") as file:
        row = []
        data = file.read()

        match = re.search(r'(<META NAME=\"bughaslinkedpsirt\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            if match.group(2) == "1":
                filelist.append(filename)


for filename in filelist:
    with open(filename, encoding = "ISO-8859-1") as file:
        row = []
        data = file.read()

        match = re.search(r'(<META NAME=\"description\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            description = match.group(2).replace("&quot", "").replace("\n", "").replace("&gt;", "") \
                                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")

        match = re.search(r'(<META NAME=\"Project\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            project = match.group(2).strip()

        match = re.search(r'(<META NAME=\"Product\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            product = match.group(2).strip()

        match = re.search(r'(<META NAME=\"Component\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            component = match.group(2).strip()

        match = re.search(r'(<META NAME=\"Found\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            found = match.group(2).strip()

        match = re.search(r'(<META NAME=\"Severity\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            severity = match.group(2).strip()

        match = re.search(r'(<META NAME=\"isss\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            if match.group(2) == "false":
                isss = "0"
            else:
                isss = "1"

        match = re.search(r'(<META NAME=\"isoib\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            if match.group(2) == "false":
                isoib = "0"
            else:
                isoib = "1"


        match = re.search(r'(<META NAME=\"Identifier\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            ddts = match.group(2).strip()

        match = re.search(r'(<META NAME=\"Headline\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            title = match.group(2).strip()

        match = re.search(r'(::Release-note\n<!--googleoff: all-->)(.*?)(<!--googleon: all-->)', data, re.M | re.S)
        if match:
            rne = match.group(2).replace("&quot", " ").replace("\n", " ").replace("&lt;/B&gt;", "")\
                .replace("&lt;B&gt;", "").replace("&lt;/b&gt;", "").replace("&lt;b&gt;", "").replace("&gt;", "")\
                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")


        row.append(project)
        row.append(product)
        row.append(component)
        row.append(found)
        row.append(severity)
        row.append(isss)
        row.append(isoib)
        row.append(ddts)
        row.append(title)
        row.append(description)
        row.append(rne)

        with open('result_psirt.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(row)
