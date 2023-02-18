import os
import csv
os.chdir("C:\\Users\\zanow\\OneDrive\\Desktop\\Scripts\\Q360")
from work_module import format_raw_customer_file
from work_module import make_file_from_list
from work_module import partial_search
from work_module import get_list_from_txt
from work_module import filter_customers
from work_module import alpha_sort_list
from work_module import combine_lists
from work_module import format_raw_bookings_file

os.chdir("C:\\Users\\zanow\\OneDrive\\Desktop\\Scripts\\Q360\\2022")

# Cleans up the outside customers file from Q360 and makes a new file.
format_raw_customer_file('raw-all-outside-customers', 'all-outside-customers')

# Cleans up the bookings file from Q360 and makes a new file.
format_raw_bookings_file('raw-all-bookings', 'all-bookings')

# Combines the bookings data into the outside customers file. Separates out customers with no sales data, as well as customers with a 5Y Average sales of zero.
with open('work-data/all-outside-customers.csv', 'r', newline='') as outside_customers_file:
    outside_reader = csv.reader(outside_customers_file)
    header = next(outside_reader)
    new_header = header + ['5Y Average']
    customers_with_no_matches = [new_header]
    customers_with_matches = [new_header]
    customers_with_zero_sales = [new_header]
    customers_with_sales = [new_header]
    for row in outside_reader:
        with open('work-data/all-bookings.csv', 'r', newline='') as bookings_file:
            sales = []
            bookings_reader = csv.reader(bookings_file)
            for row2 in bookings_reader:
                if (partial_search(row[1], row2[0], 80)):
                    sales.append(row2[1])
            if (sales == []):
                customers_with_no_matches.append(row + ['no match'])
            else:
                max_sales = max(sales)
                customers_with_matches.append(row + [max_sales])
                if max_sales == '0':
                    customers_with_zero_sales.append(row + [max_sales])
                else:
                    customers_with_sales.append(row + [max_sales])

# Uses the list of exceptional names to split off customers from the ones heading toward removal.
names_to_find = get_list_from_txt('keep-regardless-of-sales')
no_matching_sales_name_to_keep = filter_customers(customers_with_no_matches, 'Company', names_to_find)
no_matching_sales_name_to_lose = filter_customers(customers_with_no_matches, 'Company', names_to_find, matching=False)
zero_sales_to_keep = filter_customers(customers_with_zero_sales, 'Company', names_to_find)
zero_sales_to_lose = filter_customers(customers_with_zero_sales, 'Company', names_to_find, matching=False)

#Recombine those heading toward keeping and removal.
keepers_rough = combine_lists(customers_with_sales, no_matching_sales_name_to_keep, zero_sales_to_keep)
loosers = combine_lists(no_matching_sales_name_to_lose, zero_sales_to_lose)
make_file_from_list('loosers', loosers)
keepers_sorted = alpha_sort_list(keepers_rough, 'Company',)
make_file_from_list('keepers', keepers_sorted)

# Uses the list of customers with multiple locations
names_to_find = get_list_from_txt('multi-location-customers')
keepers_without_multi_location_customers = filter_customers(keepers_sorted, 'Company', names_to_find, matching=False)
multi_location_customers = filter_customers(keepers_sorted, 'Company', names_to_find, matching=True)
make_file_from_list('multi-locations', multi_location_customers)

