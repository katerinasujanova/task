# import requests                  nelze pouzit
import re
# from bs4 import BeautifulSoup    nakonec nepouzito

from lxml import html
from unicodedata import normalize


def get_data(description):

    html_file = open("data.html", "r") 
    data = html_file.read()

    '''
    scrapovat obsah primo se mi nepodarilo a nechtela jsem tim ztracet moc casu
    data jsem tak ziskala z chrome dev tools (<div class="browsingitemcontainer" id="boxes">)
    prepokladam ze jste to trochu tusili, pokud bych mela scrapovat data pro
    vsechny kategorie, tak by to uz tak jednoduche nebylo
    problem: strankovani (pokud by se dalo scrapovat, nebyl by to problem a dalo
    by se to vyresit for cyklem a formatovanim stringu pri zadavani adresy
    v requestu)
    '''

    tree = html.fromstring(data)

    phones = []

    phone_ids = tree.xpath('//a[@class="name browsinglink"]/@href')
    names = tree.xpath('//a[@class="name browsinglink"]/text()')
    prices_w_vat = tree.xpath('//span[@class="c2"]/text()')
    prices_wo_vat = tree.xpath('//span[@class="c1"]/b/text()')
    descriptions = tree.xpath('//div[@class="Description"]/text()')
    d = []
    for i, j in enumerate(descriptions):
        if i % 2 == 0:
            d.append(j)
    # tady jsem zjistila ze se mi do descriptions nacita nejaka dalsi hodnota,
    # ktera je prazdna, neni to uplne dobre reseni ale popisky jsem se rozhodla
    # pridat az skoro na konci

    for i, j in enumerate(phone_ids):
        if description == False:
            phone = {
                "phone_id": re.findall("\d{7}", j)[0],
                "name": names[i].strip("\n "),
                "price_w_vat": float(
                    (prices_w_vat[i].strip("\n ").replace("\xa0", "").replace(",-", ""))
                ),
                "price_wo_vat": float(
                    (prices_wo_vat[i].strip("\n ").replace("\xa0", "").replace(",-", ""))
                )
            }
        else:
            phone = {
                "phone_id": re.findall("\d{7}", j)[0],
                "name": names[i].strip("\n "),
                "price_w_vat": float(
                    (prices_w_vat[i].strip("\n ").replace("\xa0", "").replace(",-", ""))
                ),
                "price_wo_vat": float(
                    (prices_wo_vat[i].strip("\n ").replace("\xa0", "").replace(",-", ""))
                ),
                "description": d[i].strip("\n ")
            }
            # problém znaku \xa0 je spíš v kódování a dalo by se to vyřešit funkcí 
            # normalize("NFD", str), ale později při json dumpu se to znova rozhodí
        
        phone.update({
            "vat": round((phone["price_w_vat"]/phone["price_wo_vat"] - 1), 2)
        })
        phones.append(phone)
    # celkově to asi není nejlepší způsob jak roztřídit jednotlivé položky do 
    # dictu, zvlášť když data neznám a nijak zvlášť neověřuju, asi by měly být 
    # přiřazovány jinak než podle pozice v jednotlivých listech ale zvlášť pro 
    # každou položku na eshopu

    return phones

def get_phone_data(phone_id):
    data = get_data(description=True)

    for i in data:
        if phone_id == i["phone_id"]:
            #print(i)
            return i

if __name__ == '__main__':
    phones = get_data(description=False)
    #print(phones)


