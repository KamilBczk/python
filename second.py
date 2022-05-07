from bs4 import BeautifulSoup
import requests
import csv
import time

print("\n========== Artena Dev_ ==========\n(AD_) Quel est le nom du fichier à analyser?")
filetoread = str(input())
print("(AD_) Combien d'url voulez vous analyser?")
number = int(input())

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 79, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, iteration), end = '\r')
    if iteration == total:
        print()

file = open (filetoread, "r")
lines = file.readlines()

count = 0

def nameRecup(soup):
    name_first = soup.find('h1', class_ = 'font-bold mr-2.5 text-lg')
    if name_first is not None:
        name = name_first.text.strip()
    else:
        name_second = soup.find('h2', class_ = 'font-bold mb-1 md:mb-3 text-lg')
        if name_second is not None:
            name = name_second.text.strip()
        else:
            name = "None"
    return(name)

def phoneRecup(soup):
    phone_first = soup.find('a', class_ = 'filled-yellow-btn')
    if phone_first is not None:
        if phone_first.text.strip() == "Appeler":
            phone = soup.find('a', class_="border-b flex justify-between p-4 t-c").text.strip() + " Autres numéros"
        else:
            phone = phone_first.text.strip()
    else:
        phone_second = soup.find('li', class_ = 'flex justify-center p-2 hover:bg-gray-300 cursor-pointer')
        if phone_second is not None:
            phone = phone_second.text.strip()
        else:
            phone_third = soup.find('a', class_= 'filled-dark-btn hover:bg-black justify-center mt-auto')
            if phone_third is not None:
                phone = phone_third['data-phone-number']
            else:
                phone = "None"
    return(phone)

def siteRecup(soup):
    site_first = soup.find('a', class_ = 't-c hover:no-underline text-blue-200 underline', href=True)
    if site_first is not None:
        site = site_first['href']
    else:
        site = "None"
    return(site)

csvfile = open('results.csv', 'w', newline='', encoding='UTF8')
writer = csv.writer(csvfile)
separation = ["sep=,"]
writer.writerow(separation)

print()

for line in lines:
    count += 1
    
    printProgressBar(count, number)

    html_text = requests.get(line.strip())
    html = html_text.content
    soup = BeautifulSoup(html, 'html.parser')

    final = [line.strip(), nameRecup(soup), phoneRecup(soup), siteRecup(soup)]

    writer.writerow(final)

    time.sleep(5)
    if(number == count):
        break
