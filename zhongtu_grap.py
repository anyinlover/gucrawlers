import requests
import csv

def get_callno(isbn):
    url = f"http://opac.nlc.cn/F/H6Q7419A6FB26XV63H264PXMVPB1DC38795R7ERJXTC2CKQXIB-48942?find_code=ISB&request={isbn}&local_base=NLC01&func=find-b"
    body = requests.get(url).text
    pos = body.find("CALL-NO:")
    if pos < 0:
        print(f'{isbn}: Failed to find CallNo, quit')
        return ""
    end = body.find("\n", pos)
    callno = body[pos+8 : end].strip()
    return callno

def main():
    with open("test.csv", newline='') as infile:
        with open("out.csv", "w", newline='') as outfile:
            reader = csv.reader(infile, delimiter=',')
            writer = csv.writer(outfile, delimiter=',')
            for row in reader:
                isbn = row[0]
                out = [isbn, get_callno(isbn)]
                writer.writerow(out)

main()