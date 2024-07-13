from os import listdir
from subprocess import run
from bs4 import BeautifulSoup
from csv import DictWriter


def get_text(element):
    return element.p.span.get_text()


if __name__ == '__main__':

    for file in listdir('.'):

        if len(file.split('.')) < 2:
            continue

        if file.split('.')[1] == 'webarchive':
            run(['textutil', '-convert', 'html', file])

            with open(f'{file.split(".")[0]}.html', 'r') as htmlFile:
                html_doc = htmlFile.read()
                soup = BeautifulSoup(html_doc, 'html.parser')
                table = soup.table.tbody
                with open('output.csv', 'w') as csvFile:
                    fieldnames = [
                        '#',
                        'ID loueur',
                        'Compte',
                        'Nom du loueur',
                        'Nombre de dossiers',
                        'Solde CRM (A)',
                        'Solde compta (B)',	
                        'Facture achat / avoir (C)',
                        'Différence (A-B-C)',
                        'Statut compte',
                        'Commentaires',
                        'Référence',
                        'Client',
                        'Date de réservation',
                        'Date de départ',
                        'Tags',
                        'Reste à payer',
                        'Statut dossier',
                    ]
                    writer = DictWriter(csvFile, fieldnames=fieldnames)
                    writer.writeheader()
                    lines = table.find_all('tr')
                    for i in range(len(lines)):
                        rowDict = {}
                        tds = lines[i].find_all('td')
                        if get_text(tds[0]) == '#':
                            tds = lines[i + 1].find_all('td')
                            lessorData = {
                                key: value
                                for key, value
                                in zip(
                                    fieldnames[0:11],
                                    [get_text(td) for td in tds],
                                )
                            }
                            k = 3
                            while True:
                                if i + k >= len(lines):
                                    break
                                tds = lines[i + k].find_all('td')
                                if get_text(tds[0]) == '#':
                                    k += 1
                                    break
                                k += 1
                                rowDict = {
                                    key: get_text(value)
                                    for key, value
                                    in zip(fieldnames[11:], tds[1:])
                                }
                                rowDict.update(lessorData)
                                writer.writerow(rowDict)
                            i += k
