from bs4 import BeautifulSoup
import requests

print("\n========== Artena Dev_ ==========\n(AD_) Quelle est l'url à analyser?")
url = str(input())
print("(AD_) Combien y a t-il de pages?")
pages = int(input()) + 1
print ("\n\n\n============================== Récupération des données... ==============================\n")

urls = [url]

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 79, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total:
        print()

for i in range(pages):
    urls.append(url + str(i) + "/")

del urls[0]
del urls[0]

x = 0

tofile = []

for i in urls:
    html_text = requests.get(i)
    html = html_text.content
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.findAll('li', class_ = 'result-item')

    for li in list : 
        x += 1
        link = li.find('a', class_ = 'absolute', href=True)
        tofile.append("https://pagesdor.be" + link['href'] + "\n")
        printProgressBar(x, len(urls)*20)

with open ("urls.txt", "w") as file :
    file.seek(0);
    for y in tofile:
        file.write(y)

print("\nLes données ont été récupérées avec succès!")
input("Appuyer sur entré pour sortir du programme...\n")