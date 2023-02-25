import csv

with open('rough_contacts.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    header = next(reader)
    contacts_after_removal = [row for row in reader if all([
        all([row[x] != '' for x in (4, 5, 6, 9)]),
        not row[1].lower().startswith('accounts'),
        not row[1].startswith('AP'),
        row[12] == 'ACTIVE',
        row[3] != 'Electro Meters Company Limited'
    ])]

contacts_without_duplicate_emails = []
for count, row in enumerate(contacts_after_removal):
    if count == 0:
        last_email = row[4]
    else:
        if row[4] != last_email:
            contacts_without_duplicate_emails.append(row)
        last_email = row[4]

with open('cleaned_contacts.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for row in contacts_without_duplicate_emails:
        writer.writerow(row)