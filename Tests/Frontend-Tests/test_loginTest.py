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

class TestLoginTest():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_loginTest(self):
    # Test name: Login-Test
    # Step # | name | target | value | comment
    # 1 | open | / |  | 
    self.driver.get("https://loginsayless.netlify.app/")
    # 2 | setWindowSize | 1552x840 |  | 
    self.driver.set_window_size(1552, 840)
    # 3 | assertTitle | SayLess Login |  | 
    assert self.driver.title == "SayLess Login"
    # 4 | verifyText | css=h2 | Login | 
    assert self.driver.find_element(By.CSS_SELECTOR, "h2").text == "Login"
    # 5 | verifyText | css=.btn1 | Login | 
    assert self.driver.find_element(By.CSS_SELECTOR, ".btn1").text == "Login"
    # 6 | verifyText | linkText=Forgot password? | Forgot password? | 
    assert self.driver.find_element(By.LINK_TEXT, "Forgot password?").text == "Forgot password?"
    # 7 | verifyText | css=p:nth-child(7) | New to SayLess? Sign up | 
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7)").text == "New to SayLess? Sign up"
    # 8 | click | id=emailInput |  | 
    self.driver.find_element(By.ID, "emailInput").click()
    # 9 | type | id=emailInput | test@gmail.com | 
    self.driver.find_element(By.ID, "emailInput").send_keys("test@gmail.com")
    # 10 | click | id=passwordInput |  | 
    self.driver.find_element(By.ID, "passwordInput").click()
    # 11 | type | id=passwordInput | hello123 | 
    self.driver.find_element(By.ID, "passwordInput").send_keys("hello123")
    # 12 | close |  |  | 
    self.driver.close()
  