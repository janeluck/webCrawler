from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome('/Users/jane/software/chromeDriver/chromedriver')
driver.get("http://v.youku.com/v_show/id_XMTY2NTk5ODAwMA==.html?from=y1.3-idx-beta-1519-23042.223465.3-3")
WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.CLASS_NAME, "con")))