from os import listdir
from subprocess import run
from bs4 import BeautifulSoup
from csv import DictWriter


FIELDNAMES = [
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


def get_text(element):
    return element.p.span.get_text()


def dectify_data(fieldnames, tds):
    return {
        key: get_text(td)
        for key, td
        in zip(
            fieldnames[0:11],
            [td for td in tds],
        )
    }


def processHTMLFile(html_document, target_file):
    soup = BeautifulSoup(html_document, 'html.parser')
    table = soup.table.tbody

    with open(target_file, 'w') as csvFile:
        writer = DictWriter(csvFile, fieldnames=FIELDNAMES)
        writer.writeheader()
        lines = table.find_all('tr')
        for i in range(len(lines)):
            row_dict = {}
            tds = lines[i].find_all('td')
            if get_text(tds[0]) == '#':
                tds = lines[i + 1].find_all('td')
                lessor_data = dectify_data(FIELDNAMES[0:11], tds)
                k = 3
                while i + k < len(lines):
                    tds = lines[i + k].find_all('td')
                    if get_text(tds[0]) == '#':
                        k += 1
                        break
                    k += 1
                    row_dict = dectify_data(FIELDNAMES[11:], tds[1:])
                    row_dict.update(lessor_data)
                    writer.writerow(row_dict)
                i += k


if __name__ == '__main__':

    for file in listdir('.'):

        if len(file.split('.')) < 2:
            continue

        if file.split('.')[1] == 'webarchive':
            run(['textutil', '-convert', 'html', file])
            run(['rm', file])

            with open(f'{file.split(".")[0]}.html', 'r') as htmlFile:
                processHTMLFile(htmlFile.read(), f'{file.split(".")[0]}.csv')

            run(['rm', f'{file.split(".")[0]}.html'])
