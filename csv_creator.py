import re
import os
import csv
import tarfile


def get_common_data (filename):
    with open(filename, encoding = "ISO-8859-1") as file:
        data = file.read()
        row = []
        ddts = filename.replace(".html", "")

        match = re.search(r'(<META NAME=\"Project\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            project = match.group(2).strip()
        else:
            project = ""

        match = re.search(r'(<META NAME=\"Product\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            product = match.group(2).strip()
        else:
            product = ""

        match = re.search(r'(<META NAME=\"Component\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            component = match.group(2).strip()
        else:
            component = ""

        match = re.search(r'(<META NAME=\"Found\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            found = match.group(2).strip()
        else:
            found= ""

        match = re.search(r'(<META NAME=\"Severity\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            severity = match.group(2).strip()
        else:
            severity = ""

        match = re.search(r'(<META NAME=\"isss\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            if match.group(2) == "false":
                isss = "0"
            else:
                isss = "1"
        else:
            isss = ""

        match = re.search(r'(<META NAME=\"isoib\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            if match.group(2) == "false":
                isoib = "0"
            else:
                isoib = "1"
        else:
            isoib = ""

        match = re.search(r'(<META NAME=\"Headline\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match:
            title = match.group(2).strip()
        else:
            title = ""

        match = re.search(r'(::Release-note\n<!--googleoff: all-->)(.*?)(<!--googleon: all-->)', data, re.M | re.S)
        if match:
            rne = match.group(2).replace("&quot", " ").replace("\n", " ").replace("&lt;/B&gt;", "") \
                .replace("&lt;B&gt;", "").replace("&lt;/b&gt;", "").replace("&lt;b&gt;", "").replace("&gt;", "") \
                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")
        else:
            rne = ""


        row.append(project)
        row.append(product)
        row.append(component)
        row.append(found)
        row.append(severity)
        row.append(isss)
        row.append(isoib)
        row.append(ddts)
        row.append(title)
        row.append(rne)
    return row

# tar = tarfile.open("b.tar")
# tar.extractall()
# tar.close()

path = 'b1517'
os.chdir(path)

with open('result_non_psirt.csv', 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Project', 'Product', 'Component', 'Found', 'Severity', 'ISSS',\
                         'ISOIB', 'DDTS', 'Title', 'RNE', 'Description'])

filelist_psirt = []
filelist_psirt_big = []
filelist_psirt_descr = []

filelist_non_psirt_big = []
filelist_non_psirt_descr = []


for filename in os.listdir(os.getcwd()):
    if filename.find(".html") != -1:
        with open(filename, encoding = "ISO-8859-1") as file:
            bug_data = []
            data = file.read()
            ddts = filename.replace(".html", "")

            match = re.search(r'(<META NAME=\"bughaslinkedpsirt\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
            if match:
                if match.group(2) == "1":
                    filelist_psirt.append(filename)
                    continue

            match = re.search(r'(<META NAME=\"description\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
            if match and match.group(2):
                content = match.group(2)
                match = re.search(r'.*?BigDescription.*?', content, re.M | re.S)
                if match:
                    filelist_non_psirt_big.append(filename)
                    continue
                match = re.search(r'.*?Attachment:.*?Description.*?', content, re.M | re.S)
                if match:
                    filelist_non_psirt_descr.append(filename)
                    continue
                description = content.replace("&quot", "").replace("\n", "").replace("&gt;", "") \
                        .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")


            common_data  = get_common_data (filename)
            for item in common_data:
                bug_data.append(item)

            bug_data.append(description)

            with open('result_non_psirt.csv', 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',')
                filewriter.writerow(bug_data)

for filename in filelist_non_psirt_big:
    with open(filename, encoding = "ISO-8859-1") as file:
        bug_data = []
        data = file.read()
        ddts = filename.replace(".html", "")

        match = re.search(r'(<pre>.*?::BigDescription)(.*?)(</pre>)', data, re.M | re.S)
        if match:
            description = match.group(2).replace("\n", "").replace("&lt;/B&gt;", "")\
                .replace("&lt;B&gt;", "").replace("&lt;/b&gt;", "").replace("&lt;b&gt;", "").replace("&gt;", "")\
                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")

        common_data = get_common_data(filename)
        for item in common_data:
            bug_data.append(item)

        bug_data.append(description)

        with open('result_non_psirt.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(bug_data)

for filename in filelist_non_psirt_descr:
    with open(filename, encoding = "ISO-8859-1") as file:
        bug_data = []
        data = file.read()
        ddts = filename.replace(".html", "")

        match = re.search(r'(<pre>.*?::Description)(.*?)(</pre>)', data, re.M | re.S)
        if match:
            description = match.group(2).replace("\n", "").replace("&lt;/B&gt;", "")\
                .replace("&lt;B&gt;", "").replace("&lt;/b&gt;", "").replace("&lt;b&gt;", "").replace("&gt;", "")\
                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")

        common_data = get_common_data(filename)
        for item in common_data:
            bug_data.append(item)

        bug_data.append(description)

        with open('result_non_psirt.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(bug_data)


with open('result_psirt.csv', 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['Project', 'Product', 'Component', 'Found', 'Severity', 'ISSS',\
                         'ISOIB', 'DDTS', 'Title', 'RNE', 'Description', 'PSIRT'])

for filename in filelist_psirt:
    with open(filename, encoding="ISO-8859-1") as file:
        bug_data = []
        data = file.read()
        ddts = filename.replace(".html", "")

        match = re.search(r'(<META NAME=\"description\" CONTENT=\")(.*?)(\">)', data, re.M | re.S)
        if match and match.group(2):
            content = match.group(2)
            match = re.search(r'.*?BigDescription.*?', content, re.M | re.S)
            if match:
                filelist_psirt_big.append(filename)
                continue
            match = re.search(r'.*?Attachment:.*?Description.*?', content, re.M | re.S)
            if match:
                filelist_psirt_descr.append(filename)
                continue
            description = content.replace("&quot", "").replace("\n", "").replace("&gt;", "") \
                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")

        match = re.search(r'(<pre>.*?::PSIRT-evaluation)(.*?)(</pre>)', data, re.M | re.S)
        if match:
            psirt = match.group(2).replace("\n", " ")

        common_data = get_common_data(filename)
        for item in common_data:
            bug_data.append(item)

        bug_data.append(description)
        bug_data.append(psirt)

        with open('result_psirt.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(bug_data)

for filename in filelist_psirt_big:
    with open(filename, encoding = "ISO-8859-1") as file:
        bug_data = []
        data = file.read()
        ddts = filename.replace(".html", "")

        match = re.search(r'(<pre>.*?::BigDescription)(.*?)(</pre>)', data, re.M | re.S)
        if match:
            description = match.group(2).replace("\n", "").replace("&lt;/B&gt;", "")\
                .replace("&lt;B&gt;", "").replace("&lt;/b&gt;", "").replace("&lt;b&gt;", "").replace("&gt;", "")\
                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")

        match = re.search(r'(<pre>.*?::PSIRT-evaluation)(.*?)(</pre>)', data, re.M | re.S)
        if match:
            psirt = match.group(2).replace("\n", " ")

        common_data = get_common_data(filename)
        for item in common_data:
            bug_data.append(item)

        bug_data.append(description)
        bug_data.append(psirt)

        with open('result_psirt.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(bug_data)

for filename in filelist_psirt_descr:
    with open(filename, encoding = "ISO-8859-1") as file:
        bug_data = []
        data = file.read()
        ddts = filename.replace(".html", "")

        match = re.search(r'(<pre>.*?::Description)(.*?)(</pre>)', data, re.M | re.S)
        if match:
            description = match.group(2).replace("\n", "").replace("&lt;/B&gt;", "")\
                .replace("&lt;B&gt;", "").replace("&lt;/b&gt;", "").replace("&lt;b&gt;", "").replace("&gt;", "")\
                .replace("&lt;", "").replace("CmdBold", "").replace("noCmdBold", "")

        match = re.search(r'(<pre>.*?::PSIRT-evaluation)(.*?)(</pre>)', data, re.M | re.S)
        if match:
            psirt = match.group(2).replace("\n", " ")

        common_data = get_common_data(filename)
        for item in common_data:
            bug_data.append(item)

        bug_data.append(description)
        bug_data.append(psirt)

        with open('result_psirt.csv', 'a') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(bug_data)
