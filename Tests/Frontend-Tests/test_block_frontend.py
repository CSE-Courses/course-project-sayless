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

class TestBlock():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_block(self):
    # Test name: block
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
    # 8 | click | linkText=Block Users | 
    self.driver.find_element(By.LINK_TEXT, "Block Users").click()
    # 9 | verifyEditable | id=autocomplete-3 | 
    element = self.driver.find_element(By.ID, "autocomplete-3")
    assert element.is_enabled() is True
    # 10 | click | css=.btn |
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".btn")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    # 11 | click | id=yes | 
    time.sleep(1)
    self.driver.find_element(By.ID, "yes").click()
    # 12 | click | css=.fa-sign-out-alt |
    WebDriverWait(self.driver, 30000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".fa-sign-out-alt")))
    time.sleep(2)
    self.driver.find_element(By.CSS_SELECTOR, ".fa-sign-out-alt").click()
    # 13 | close |  | 
    self.driver.close()
  
