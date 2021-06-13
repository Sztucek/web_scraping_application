from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
currentYear = 2020
driver.get("https://pl.wikipedia.org/wiki/{year}_w_grach_komputerowych".format(year=currentYear))
file = open("output.csv", "w")
file.write("Tytuł;Platformy\n")
firstTableNumber = 5
for iteration in range(10):
    try:
        pageTables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "wikitable"))
        )
        gamesTables = pageTables[-4:]
        for gamesTable in gamesTables:
            rows = gamesTable.find_elements_by_tag_name('tr')
            iterator = 0
            for row in rows:
                if iterator > 0:
                    cols = row.find_elements_by_tag_name('td')
                    file.write(cols[-3].text + ';' + cols[-2].text + '\n')
                iterator = iterator + 1
        currentYear = currentYear - 1
        categoryChooseBoxes = driver.find_elements_by_class_name("mw-collapsible")
        categoryChooseBox = categoryChooseBoxes[-1]
        showMoreBtn = categoryChooseBox.find_element_by_class_name("mw-collapsible-text")
        showMoreBtn.click()
        nextYearCategories = WebDriverWait(categoryChooseBox, 10).until(
            EC.presence_of_all_elements_located(
                (By.TAG_NAME, "li")
            )
        )
        for nextYearCategory in nextYearCategories:
            linkToNextCategory = nextYearCategory.find_element_by_xpath('//a[text()="{year}"]'.format(year=currentYear))
            linkToNextCategory.click()
    except:
            print("Couldn't locate table")
file.close()
driver.quit()
