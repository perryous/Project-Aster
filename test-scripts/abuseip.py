#!/usr/bin/env python
# _0853RV3R
import urllib2, sys, subprocess, argparse, os, webbrowser, time, traceback
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description = \
"AbuseIPDB Checker v1.2\n\
\n\
Checks AbuseIPDB.com for reports on an IP address.\n\
\n\
anti-hacker toolkit\n\
_0853RV3R",
formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('ipaddr', action="store", help="target IP address")
parser.add_argument('-n', '--nmap', action="store_true", dest="nmap", help="run nmap scan in addition to AbuseIPDB check")
parser.add_argument('-o', '--output', action="store", dest="outputfile", help="output file location")
parser.add_argument('-x', '--overwrite', action="store_true", dest="overwrite", help="overwrite existing file")
parser.add_argument('-w', '--webview', action="store_true", dest="webview", help="open AbuseIPDB results in web browser")

if len(sys.argv[1:])==0:
    parser.print_help()        
    parser.exit()

argument = parser.parse_args()

ipaddr = argument.ipaddr
nmap = argument.nmap
outputfile = argument.outputfile
overwrite = argument.overwrite
webview = argument.webview

report = ""

if outputfile is not None:
    file_exists = os.path.isfile(outputfile)
    if file_exists and not overwrite:
        userinput = raw_input("File already exists. Overwrite file? y/n ")
        if "y" in userinput.lower():
            overwrite = True

    file = open(outputfile, 'w')
    out = True
else:
    out = False



def nmapscan():
    try:
        nmap_start = subprocess.Popen(["nmap", "-T4", "-A", "-Pn", ipaddr], stdout=subprocess.PIPE)
        nmap_result = nmap_start.stdout.read()
    except:
        errorlog = traceback.format_exc()
        errorfmt = errorlog.splitlines()[-1]
        print(errorfmt)
        nmap_result = "Nmap scan failed.\n"

    return nmap_result + "\n"

def AbuseIPDB():
    quote_page = "https://www.abuseipdb.com/check/" + ipaddr

    if webview:
        webbrowser.open(quote_page,new=1)

    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

        page = urllib2.Request(quote_page, headers=hdr)
        data = urllib2.urlopen(page)

        page = data.read()


        soup1 = BeautifulSoup(page, 'html.parser')
        name_box1 = soup1.find('div', attrs={'class': 'well'})
        info = name_box1.text.strip()

        trim1 = info.replace("\t", "")
        trim1 = os.linesep.join([s for s in trim1.splitlines() if "Report" not in s])
        trim1 = os.linesep.join([s for s in trim1.splitlines() if "Whois" not in s])
        trim1 = os.linesep.join([s for s in trim1.splitlines() if s])
        trim1 = trim1.replace("ISP\n", "\nISP: ")
        trim1 = trim1.replace("Usage Type\n", "Usage Type: ")
        trim1 = trim1.replace("Domain Name\n", "Domain Name: ")
        trim1 = trim1.replace("Country\n", "Country: ")
        trim1 = trim1.replace("City\n", "City: ")
        info = trim1

    except:
        info = "AbuseIPDB lookup failed.\n"
        errorlog = traceback.format_exc()
        errorfmt = errorlog.splitlines()[-1]
        print(errorfmt)

    try:
        soup2 = BeautifulSoup(page, 'html.parser')
        name_box2 = soup2.find('table', attrs={'class': 'table table-striped responsive-table'})
        comments = name_box2.text.strip()

        trim2 = comments.replace("Reporter \n Date \n Comment \n Categories \n\n", "")
        trim2 = trim2.replace("\t", "")
        trim2 = trim2.replace("\n\n", "\n")
        trim2 = trim2.replace("             \n", "\n")
        trim2 = trim2.replace("\n\n", "\n")
        trim2 = trim2.replace("\n ", "\n")

        trim2 = trim2.replace("show less", "")
        lines = trim2.splitlines()
        part = ""
        for line in lines:
            if "... show more" in line:
                head, _sep, tail = line.rpartition("... show more")
                line = tail
            part += line + "\n"
        trim2 = part
        

        header = "\n\n\nReport Comments:"
        header += "\n================================================="
        header += "\n" + time.strftime("%d %b %Y %H:%M:%S")
        footer = "\n================================================="
        comments = header + trim2 + footer
    except:
        comments = ""

    return info, comments


if nmap:
    scan = nmapscan()

else:
    scan = ""


info, comments = AbuseIPDB()

report = scan + info + comments
report = report.encode('ascii', 'replace')

print(report)

if out or overwrite:
    print("Writing report to output file: " + outputfile)
    file.write(report)
    file.close()


