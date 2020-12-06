# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestProfile():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_profile(self):
    # Test name: profile
    # Step # | name | target | value
    # 1 | open | /login | 
    self.driver.get("http://sayless.azurewebsites.net/login")
    # 2 | setWindowSize | 1552x840 | 
    self.driver.set_window_size(1552, 840)
    # 3 | click | id=emailInput | 
    self.driver.find_element(By.ID, "emailInput").click()
    # 4 | type | id=emailInput | jshrishty18@gmail.com
    self.driver.find_element(By.ID, "emailInput").send_keys("jshrishty18@gmail.com")
    # 5 | type | id=passwordInput | Password123
    self.driver.find_element(By.ID, "passwordInput").send_keys("Password123")
    # 6 | click | css=.submit | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".submit")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".submit").click()
    # 7 | click | css=.fa-cog | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fa-cog")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fa-cog").click()
    # 8 | verifyEditable | id=fn | 
    element = self.driver.find_element(By.ID, "fn")
    assert element.is_enabled() is True
    # 9 | verifyEditable | id=ln | 
    element = self.driver.find_element(By.ID, "ln")
    assert element.is_enabled() is True
    # 10 | verifyEditable | id=username | 
    element = self.driver.find_element(By.ID, "username")
    assert element.is_enabled() is True
    # 11 | click | id=new-pw | 
    self.driver.find_element(By.ID, "new-pw").click()
    # 12 | verifyEditable | id=new-pw | 
    element = self.driver.find_element(By.ID, "new-pw")
    assert element.is_enabled() is True
    # 13 | click | css=.right | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".right")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".right").click()
    # 14 | verifyElementPresent | linkText=Block Users | 
    elements = self.driver.find_elements(By.LINK_TEXT, "Block Users")
    assert len(elements) > 0
    # 15 | verifyElementPresent | linkText=Delete Account | 
    elements = self.driver.find_elements(By.LINK_TEXT, "Delete Account")
    assert len(elements) > 0
    # 16 | verifyElementPresent | linkText=Edit | 
    elements = self.driver.find_elements(By.LINK_TEXT, "Edit")
    assert len(elements) > 0
    # 17 | click | linkText=Block Users | 
    self.driver.find_element(By.LINK_TEXT, "Block Users").click()
    # 18 | click | css=.fa-cog | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fa-cog")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fa-cog").click()
    # 19 | click | linkText=Delete Account | 
    self.driver.find_element(By.LINK_TEXT, "Delete Account").click()
    # 20 | click | css=.fa-cog | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fa-cog")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fa-cog").click()
    # 21 | click | linkText=Edit | 
    self.driver.find_element(By.LINK_TEXT, "Edit").click()
    # 22 | click | css=.fas | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fas")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fas").click()
    # 23 | click | id=fn | 
    self.driver.find_element(By.ID, "fn").click()
    # 24 | type | id=fn | Shrishtyy
    self.driver.find_element(By.ID, "fn").send_keys("Shrishtyy")
    # 25 | click | id=ln | 
    self.driver.find_element(By.ID, "ln").click()
    # 26 | type | id=ln | J
    self.driver.find_element(By.ID, "ln").send_keys("J")
    # 27 | click | id=username | 
    self.driver.find_element(By.ID, "username").click()
    # 28 | type | id=username | shrishty
    self.driver.find_element(By.ID, "username").send_keys("shrishty")
    # 29 | click | css=.right | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".right")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".right").click()
    # 30 | click | id=bio | 
    self.driver.find_element(By.ID, "bio").click()
    # 31 | click | id=bio | 
    self.driver.find_element(By.ID, "bio").click()
    # 32 | type | id=bio | UB 2021, go bulls!
    self.driver.find_element(By.ID, "bio").send_keys("UB 2021, go bulls!")
    # 33 | click | id=update | 
    self.driver.find_element(By.ID, "update").click()
    # 34 | click | css=.fas | 
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fas")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fas").click()
    # 35 | close |  | 
    self.driver.close()
  