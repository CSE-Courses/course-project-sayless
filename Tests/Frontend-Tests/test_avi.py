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

class TestAvi():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_avi(self):
    # Test name: avi
    # Step # | name | target | value
    # 1 | open | /login | 
    self.driver.get("http://sayless.azurewebsites.net/login")
    # 2 | setWindowSize | 1552x840 | 
    self.driver.set_window_size(1552, 840)
    # 3 | click | id=emailInput | 
    self.driver.find_element(By.ID, "emailInput").click()
    # 4 | type | id=emailInput | jshrishty18@gmail.com
    self.driver.find_element(By.ID, "emailInput").send_keys("jshrishty18@gmail.com")
    # 5 | type | id=passwordInput | Newpassword1234
    self.driver.find_element(By.ID, "passwordInput").send_keys("Newpassword1234")
    # 6 | click | css=.submit | 
    self.driver.find_element(By.CSS_SELECTOR, ".submit").click()
    # 7 | click | css=.fa-cog |
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fa-cog")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fa-cog").click()
    # 8 | click | linkText=Edit | 
    self.driver.find_element(By.LINK_TEXT, "Edit").click()
    # 9 | click | id=myFile | 
    self.driver.find_element(By.ID, "myFile").click()
    # 10 | click | css=h2 |
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "h2")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, "h2").click()
    # 11 | verifyTitle | Update AVI | 
    assert self.driver.title == "Update AVI"
    # 12 | click | id=submit | 
    self.driver.find_element(By.ID, "submit").click()
    # 13 | click | css=.fas |
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fas")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fas").click()
    # 14 | click | css=.fas |
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fas")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fas").click()
    # 15 | click | css=.fa-sign-out-alt |
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fa-sign-out-alt")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fa-sign-out-alt").click()
  

  
