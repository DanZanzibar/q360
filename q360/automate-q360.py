from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import csv

os.chdir(r"C:\Users\zanow\OneDrive\Desktop\Scripts\Python")

def get_list_from_csv(file_name):
    with open(f'work-data/{file_name}.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        output_list = []
        for row in reader:
            output_list.append(row)
    return output_list

def wait_for_element(button):
    count = 0
    while count < 20:
        try:
            edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-componentid='main_edit']")))
        except:
            time.sleep(1)
            count += 1

def make_file_from_list(file_name, list):
    with open(f'work-data/{file_name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in list:
            writer.writerow(row)

def change_customer(customer_no):
    wait = WebDriverWait(driver, 20)
    search_field = driver.find_element(By.XPATH, "//input[@data-name='mainsearch-value-main']")
    search_field.send_keys(customer_no)
    time.sleep(1)
    search_field.send_keys(Keys.RETURN)
    time.sleep(1)

    count = 0
    while count < 30:
        try:
            edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-componentid='main_edit']")))
            print('edit ready')
            edit_button.click()
            print('edit clicked')
            break
        except:
            time.sleep(1)
            count += 1
    time.sleep(1)

    count = 0
    while count < 20:
        try:
            save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-componentid='main_save']")))
            print('save ready')
            break
        except:
            time.sleep(1)
            count += 1
    time.sleep(1)

    rep_2 = Select(driver.find_element(By.XPATH, "//select[@data-name='salesrep2']"))
    rep_2.select_by_visible_text('')
    save_button.click()
    time.sleep(1)
    
    count = 0
    while count < 20:
        try:
            edit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-componentid='main_edit']")))
            break
        except:
            time.sleep(1)
            count += 1
    time.sleep(1)

#Initial log-in
driver = webdriver.Chrome()
driver.get("https://q360prod.electro-meters.com/controller.php?action=login")
user_box = driver.find_element(By.ID, 'userid')
user_box.send_keys('zowsley')
pass_box = driver.find_element(By.ID, 'password')
pass_box.send_keys('Kenisthebest')
login_button = driver.find_element(By.CLASS_NAME, 'icon-check-before')
login_button.click()
time.sleep(6)

#Get customer window open and switch to iframe
close_button = driver.find_element(By.XPATH, "//div[@title='Close']")
close_button.click()
cust_button = driver.find_element(By.CLASS_NAME, 'toolBarButton')
cust_button.click()
time.sleep(6)
driver.switch_to.frame(0)

loosers = get_list_from_csv('loosers-not-lost')

for x in range(0, len(loosers)):
    change_customer(loosers[0][0])
    loosers.pop(0)
    make_file_from_list('loosers-not-lost', loosers)
