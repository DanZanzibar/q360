import os
os.chdir("C:\\Users\\zanow\\OneDrive\\Desktop\\Scripts\\Q360")
import work_module as wm

os.chdir("C:\\Users\\zanow\\OneDrive\\Desktop\\Scripts\\Q360\\2023")

wm.format_raw_customer_file('raw-outside-customers', 'outside-customers-no-bookings')
wm.format_raw_bookings_file('raw-bookings', 'bookings')
wm.add_bookings_data('outside-customers-no-bookings', 'bookings', 'outside-customers')