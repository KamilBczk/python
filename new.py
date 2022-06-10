import sys
import time
import urllib.parse
from bs4 import BeautifulSoup
import requests
import math 
import os
import numpy as np

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ORANGE = '\033[33m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

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
    return(site.replace("?utm_source=fcrmedia&utm_medium=internet&utm_campaign=goudengidspagesdor", ""))

def mailRecup(soup):
    mail_first = soup.find('a', class_ = 'hover:no-underline text-blue-200 underline t-c', href=True)
    if mail_first is not None:
        mail = mail_first['href']
    else:
        mail_second = soup.find('a', class_ = 'outline-btn t-c', href=True)
        if mail_second is not None:
            mail = mail_second['href']
        else:
            mail = "None"
    finalmail = mail.replace("mailto:", "")
    return(finalmail.replace("?subject=Demande d’information via pagesdor.be", ""))

print("\r")

def print_slow(str, logo = False):
    if (logo == True):
        sleep_time = 0.00005;
        print(f"{bcolors.ORANGE}")
    else:
        sleep_time = 0.05;
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(sleep_time)
    if (logo == True):
        print(f"{bcolors.RESET}")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 35, fill = f'{bcolors.RESET}█{bcolors.RESET}'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + f'{bcolors.RESET}-{bcolors.RESET}' * (length - filledLength)
    print('\r\t  %s➤%s\t%s%% | %s/%s %s %s %s' % (bcolors.WARNING, bcolors.RESET, percent, iteration, total, prefix, bar, suffix), end = '\r')
    if iteration == total:
        print('\r\t  %s➤%s\t%s%% | %s/%s %s %s' % (bcolors.OKGREEN, bcolors.RESET, percent, iteration, total, prefix, bar), end = '\r')
        print()

def string_format(str):
    for i in range(150):
        if (len(str) <= i):
            str += " "
    return (str)

def print_console(status, message="No message", slow_typing = False):
    if (slow_typing == True):
        print_slow(f"\n\t  {bcolors.OKGREEN}✓{bcolors.RESET} \t{message}\n\n")
    elif (status == 1):
        print(f"\t  {bcolors.FAIL}!{bcolors.RESET}    {string_format(message)}")
    elif (status == 2):
        print(f"\t[ {bcolors.FAIL}?{bcolors.RESET} ]\t{message}")
    elif (status == 3):
        print(f"\t[ {bcolors.WARNING}?{bcolors.RESET} ]\t{message}")
    elif (status == 4):
        print(f"\t{bcolors.UNDERLINE}{message}{bcolors.RESET}\n")
    elif (status == 5):
        print(f"\t[ {bcolors.OKGREEN}✉{bcolors.RESET} ]\t{message}")
    elif (status == 6):
        print(f"\t[ {bcolors.WARNING}?{bcolors.RESET} ]\t", end="")
        return input()
    elif (status == 7):
        print(f"\t  {bcolors.OKGREEN}➤{bcolors.RESET} \t{message}")
        
def get_proxy():
    print_console(3, "Recherche de proxy...")
    proxy_request = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
    proxy_text = proxy_request.content.decode("utf-8")
    proxy_to_test = ""
    found_proxy = False

    for letter in proxy_text:
        if not (letter == "\r" or letter == "\n"):
            proxy_to_test += letter
        if (letter == "\n"):
            proxies = {"https":f"https://{proxy_to_test}"}
            try:
                response = requests.get("https://pagesdor.be", proxies=proxies, timeout=5)
                print_console(4, f"Proxy trouvé : {proxies}")
                found_proxy = True
                break
            except:
                proxy_to_test = "";
    if (found_proxy == False):
        get_proxy()
    return proxies

def change_vpn():
    print_console(1, "Veuillez changer de VPN (Appuyer sur entré)")
    input()
    try:
        requests.get("https://www.pagesdor.be", timeout=5)
    except:
        print_console(1, "Votre VPN n'as toujours pas été accepté")
        change_vpn()

def get_categories():
    categories = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T"]
    # categories = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","R","S","T","U","V","Y","Z"]
    all = 0
    file = open("categories.txt", "w")
    for alphabet in categories:
        time.sleep(1.0 + np.random.uniform(0,60))
        url = f"https://www.pagesdor.be/les-categories/{alphabet}/1/"
        try:
            response = requests.get(url, timeout=5)
        except:
            change_vpn()
            response = requests.get(url, timeout=5)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.find("ul", class_ = "gap-x-4 grid grid-cols-1 mb20 md:grid-cols-2")
        li = ul.findAll("a", class_ = "text-blue-200 underline hover:no-underline", href=True)
        print_console(7, f"Catégorie {alphabet} : {len(li)} catégories trouvés")
        all += len(li)
        for elem in li:
            tofile = f"https://pagesdor.be{elem['href']}\n"
            file.write(tofile)
    return all

def get_page(nb_categories):
    
    all = 0
    cache = open("cache.txt", "w")
    file = open("categories.txt", "r")
    lines = file.readlines()
    i = 0
    for line in lines:
        time.sleep(1.0 + np.random.uniform(0,60))
        i += 1
        url = line.strip()
        try:
            response = requests.get(url, timeout=5)
        except:
            change_vpn()
            response = requests.get(url, timeout=5)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        nb = int(soup.find("span", class_ = "font-medium count").text.replace(" ", ""))
        name = soup.find("span", class_ = "font-medium what").text
        pages = math.ceil(nb/20)
        all += pages
        printProgressBar(i, nb_categories, suffix=string_format(f"Catégorie \"{name}\": {bcolors.BOLD}{nb}{bcolors.RESET} entreprises trouvées ({pages} pages)."))
        while pages != 0:
            if(pages==1):
                cache.write(f"{url}\n")
            else:
                cache.write(f"{url.replace('/entreprises/', '/trouvez/')}{pages}\n")
            pages -= 1
    file.close()
    os.remove("categories.txt")
    return all

def scrap_links(nb_pages):
    all = 0
    file_r = open("cache.txt", "r")
    file_w = open("links.txt", "w")
    lines = file_r.readlines()
    i = 0
    for line in lines:
        time.sleep(1.0 + np.random.uniform(0,60))
        i += 1
        url = line.strip()
        try:
            response = requests.get(url, timeout=5)
        except:
            change_vpn()
            response = requests.get(url, timeout=5)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        list = soup.findAll('li', class_ = 'result-item')
        elems = 0
        for li in list :
            elems += 1
            all += 1
            link = li.find('a', class_ = 'absolute', href=True)
            file_w.write(f"https://pagesdor.be{link['href']}\n")
        printProgressBar(i, nb_pages, suffix=string_format(f"Page n°{bcolors.BOLD}{i}{bcolors.RESET}: {elems} entreprises trouvées."))
    file_r.close()
    os.remove("cache.txt")
    return all

def scrap_link(nb_links):
    all = 0
    file_r = open("links.txt")
    lines = file_r.readlines()
    i = 0
    for line in lines:
        time.sleep(1.0 + np.random.uniform(0,60))
        i += 1
        url = line.strip()
        try:
            response = requests.get(url, timeout=5)
        except:
            change_vpn()
            response = requests.get(url, timeout=5)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        # to_send = f"http://api.kamilbiczyk.be/webscrapping/?ref={urllib.parse.quote(line.strip())}&nom={urllib.parse.quote(nameRecup(soup))}&num={urllib.parse.quote(phoneRecup(soup))}&site={urllib.parse.quote(siteRecup(soup))}&mail={urllib.parse.quote(mailRecup(soup))}";
        # requests.get(to_send, timeout=5)
        printProgressBar(i, nb_links, suffix=string_format(f"Analyse de l'entreprise {bcolors.BOLD}{nameRecup(soup)}{bcolors.RESET}"))


# Print logo
logo = "\n\t\t       d8888         888                                   8888888b.\n\t\t      d88888         888                                   888  \"Y88b\n\t\t     d88P888         888                                   888    888\n\t\t    d88P 888 888d888 888888 .d88b.  88888b.   8888b.       888    888  .d88b.  888  888\n\t\t   d88P  888 888P\"   888   d8P  Y8b 888 \"88b     \"88b      888    888 d8P  Y8b 888  888\n\t\t  d88P   888 888     888   88888888 888  888 .d888888      888    888 88888888 Y88  88P\n\t\t d8888888888 888     Y88b. Y8b.     888  888 888  888      888  .d88P Y8b.      Y8bd8P\n\t\td88P     888 888      \"Y888 \"Y8888  888  888 \"Y888888      8888888P\"   \"Y8888    Y88P  88888888\n"
print_slow(logo, logo=True)

# Get categories
print_console(4, "Étape ➀ sur ➃ : Récupération de toutes les catégories")
nb_categories = get_categories()
print_console(4, f"{bcolors.BOLD}{nb_categories}{bcolors.RESET} catégories ont été trouvées", slow_typing=True)

# Analyse des catégories pour obtenir les liens directs
print_console(4, "Étape ➁ sur ➃ : Analyse des catégories pour obtenir les différentes pages")
nb_pages = get_page(nb_categories)
print_console(4, f"{bcolors.BOLD}{nb_pages}{bcolors.RESET} Pages trouvées ce qui fait une moyenne de {bcolors.BOLD}{nb_pages*18}{bcolors.RESET} entreprises à analyser", slow_typing=True)

print_console(4, "Étape ➂ sur ➃ : Analyse des pages pour obtenir les liens directs")
nb_links = scrap_links(nb_pages)
print_console(4, f"{bcolors.BOLD}{nb_links}{bcolors.RESET} entreprises trouvées.", slow_typing=True)

print_console(4, "Étape ➃ sur ➃ : Scrapping des liens pour obtenir les informations")
nb_link = scrap_link(nb_links)

