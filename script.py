from 
from bs4 import BeautifulSoup
from csv import DictWriter


if __name__ == '__main__':

    with open('file.html', 'r') as htmlFile:
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
                if tds[0].p.span.get_text() == '#':
                    tds = lines[i + 1].find_all('td')
                    lessorData = {
                        key: value
                        for key, value
                        in zip(
                            fieldnames[0:11],
                            [td.p.span.get_text() for td in tds],
                        )
                    }
                    k = 3
                    while True:
                        if i + k >= len(lines):
                            break
                        tds = lines[i + k].find_all('td')
                        k += 1
                        rowDict = {}
                        for j, title in enumerate(fieldnames[11:]):
                            try:
                                rowDict[title] = tds[j + 1].p.span.get_text()
                            except IndexError:
                                break
                        rowDict.update(lessorData)
                        if rowDict['Référence'] == 'ID loueur':
                            break
                        writer.writerow(rowDict)
                    i += k
