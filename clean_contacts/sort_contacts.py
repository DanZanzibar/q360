import csv
from datetime import date

with open('activities_zan.csv', 'r', newline='') as file_zan:
    with open('activities_ian.csv', 'r', newline='') as file_ian:
        with open('activities_atiba.csv', 'r', newline='') as file_atiba:
            reader_zan = csv.reader(file_zan)
            header = next(reader_zan)
            reader_ian = csv. reader(file_ian)
            next(reader_ian)
            reader_atiba = csv.reader(file_atiba)
            next(reader_atiba)
            combined_act = [header]
            for reader in (reader_zan, reader_ian, reader_atiba):
                for row in reader:
                    combined_act.append(row)

with open('all_activities.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in combined_act:
        writer.writerow(row)

# Make a dict of contact no's and most recent activity date

mractivity = {}
act_with_custno = []
act_without_custno = []
for count, row in enumerate(combined_act):
    if count > 0:
        contact_no = row[5]
        if contact_no != '':
            act_date = date.fromisoformat(row[2])
            if contact_no in mractivity: 
                current_dict_date = mractivity[contact_no]
                if act_date > current_dict_date: current_dict_date = act_date
            else: mractivity[contact_no] = act_date
            act_with_custno.append(row)
        else: act_without_custno.append(row)

print(f'There are {len(act_with_custno)} activities with customers, {len(act_without_custno)} without.')
print(f'This should match {len(combined_act) - 1} total activities')



with open('rough_contacts.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    header = next(reader)
    contacts_after_removal = [row for row in reader if all([
        all([row[x] != '' for x in (4, 5, 6, 9)]),
        not row[1].lower().startswith('accounts'),
        not row[1].startswith('AP'),
        row[12] == 'ACTIVE',
        row[3] != 'Electro Meters Company Limited',
        row[0] in mractivity
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