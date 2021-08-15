from bs4 import BeautifulSoup
from fpdf import FPDF
from collections import OrderedDict
import requests
import os
import fpdf


fpdf.set_global("SYSTEM_TTFONTS", os.path.join(os.path.dirname(__file__),'fonts'))

urls = []
pdf=FPDF()
pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)

# Change range to the number of pages to scrape ( 167 MAX on the day of this edit)
for i in range(1, 15):
    page = "https://www.thehindu.com/opinion/editorial/?page={}".format(i)
    reqs = requests.get(page)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    for link in soup.find_all('a'):
        ln = str(link.get('href'))
        if "www.thehindu.com/opinion/editorial" in ln and ".ece" in ln:
            urls.append(ln)

print(len(urls))
urls = list(OrderedDict.fromkeys(urls))
print(len(urls))

for link in urls:
    reqs = requests.get(link)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    title = soup.find("h1", class_="title")
    body = soup.find_all('p')
    date = soup.find('none')

    if title:
       
        title = title.getText()
    else:
        title = soup.find("h2", class_="special-article-heading")
        if title:
            title = title.getText()
        else:
            title = "<TitleNotFound>"

    if date:
        date = date.getText()
    else:
        date = "<DateNotFound>"

    pdf.add_page()
    count += 1;
    pdf.set_font("NotoSans", size = 20)

    pdf.multi_cell(0, 8, txt = str(title), align = 'L')
    pdf.set_font("NotoSans", size = 10)

    pdf.multi_cell(0, 8, txt = str(date), align = 'L')
    pdf.set_font("NotoSans", size = 13)
    for i in body[:-4]:
        text = i.getText()
        pdf.multi_cell(0, 7, txt = text , align = 'L')
        pdf.cell(0,4, ln=1, align='C')
    
    print(count)


pdf.output("Editorials.pdf")   
