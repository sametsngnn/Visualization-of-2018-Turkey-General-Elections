from flask import Flask, render_template
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import os
import time
from selenium.webdriver.common.action_chains import ActionChains

app = Flask(__name__)

def create_folder(path):
    try:
        os.makedirs(path)
        print(f"Folder Created: {path}")
    except FileExistsError:
        print(f"Folder Already Exist: {path}")

def check_json(json_path):
    if os.path.exists(json_path) or os.path.exists(os.path.join(os.path.expanduser("~"), "Downloads", "SecimSonucIl.json")):
        return True

def JsonIlce(il_id):
    original_path = os.path.join(os.path.expanduser("~"), "Downloads", "SecimSonucIlce.json")
    json_path = os.getcwd()+ "/datavisproject/JSON/IlceSonuc/"
    os.rename(original_path,json_path+f"{il_id}.json")

browser = None
def fetch(json_path):
    global browser
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--disable-cache")
    options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36")
    if browser is None:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
    link = "https://acikveri.ysk.gov.tr/anasayfa"
    browser.get(link)
    button = browser.find_element(By.ID, "myModalClose")
    button.click()
    link_element = browser.find_element(By.ID, "navbarDropdown")
    link_element.click()
    link_element = browser.find_element(By.ID, "heading6")
    link_element.click()
    link_element = browser.find_element(By.XPATH,"/html/body/ngb-modal-window/div/div/div[2]/div/div[7]/div[4]")
    link_element.click()
    female_male_numbers = []
    link_element = browser.find_element(By.CSS_SELECTOR,"#accordionSidebar > li:nth-child(9) > a")
    link_element.click()
    female = browser.find_element(By.CSS_SELECTOR,"#content > div > div.row.mt-3 > div:nth-child(2) > div > div > div > div.col.mr-2 > div.row.no-gutters.align-items-center > div.col-auto > div").text
    male = browser.find_element(By.CSS_SELECTOR,"#content > div > div.row.mt-3 > div:nth-child(3) > div > div > div > div.col.mr-2 > div.row.no-gutters.align-items-center > div.col-auto > div").text
    female_male_numbers.append(female)
    female_male_numbers.append(male)
    new_folder_path = os.getcwd()+"/JSON/"
    create_folder(new_folder_path)
    female_male_numbers_df = pd.DataFrame({'Female':[female_male_numbers[0]],'Male':[female_male_numbers[1]]})
    create_folder(json_path+"FemaleMaleJSON/")
    female_male_numbers_df.to_json(json_path+"FemaleMaleJSON/femaleMale.json")

    create_folder(json_path+"IlSonuc/")
    link_element = browser.find_element(By.CSS_SELECTOR, "#accordionSidebar > li:nth-child(22) > a > svg")
    link_element.click()
    json_indir = browser.find_element(By.CSS_SELECTOR,"#kadinErkekOraniBar > div.card-body > div > button:nth-child(2)")
    json_indir.click()
    time.sleep(2)
    original_path = os.path.join(os.path.expanduser("~"), "Downloads", "SecimSonucIl.json")
    os.rename(original_path, json_path+"IlSonuc/SecimSonucIl.json")
    time.sleep(5)
    browser.quit()
    

@app.route("/")
def main():
    print(os.getcwd())
    json_path = os.getcwd()+"/JSON/"
    fetch(json_path)
    return render_template("json.html")

if __name__ == "__main__":
    app.run(debug=True)