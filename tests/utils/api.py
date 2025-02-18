import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

def singleton(class_):
  instances = {}

  def getinstance(*args, **kwargs):
    if class_ not in instances:
      instances[class_] = class_(*args, **kwargs)
    return instances[class_]

  return getinstance

@singleton
class BrowserAPI:
  def __init__(self):
    self.web_driver = webdriver.Chrome()
    self.timeout = 30
    self.wait = WebDriverWait(self.web_driver, self.timeout)

  def find_visible_by_text(self, input_str):
    locator = By.XPATH, f"//*[text()=\"{input_str}\"]"

    return self.find_visible_element(locator)

  def find_visible_element(self, locator: tuple):
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    wait = WebDriverWait(self.web_driver, self.timeout, ignored_exceptions=ignored_exceptions)

    return wait.until(expected_conditions.visibility_of_element_located(locator), f'Failed to find web element {locator}')

  def switch_to_frame(self, frame: WebElement):
    self.web_driver.switch_to.frame(frame)

  def switch_to_default_content(self):
    self.web_driver.switch_to.default_content()

  def get_attribute(self, element_or_visible_locator, attribute):
    element = element_or_visible_locator if isinstance(element_or_visible_locator, WebElement) else self.find_visible_element(element_or_visible_locator)

    return element.get_attribute(attribute)

  def set_attribute(self, element_or_visible_locator, attribute, value):
    element = element_or_visible_locator if isinstance(element_or_visible_locator, WebElement) else self.find_visible_element(element_or_visible_locator)
                                                                                                              
    self.web_driver.execute_script(f"""
      element = arguments[0];
      element.setAttribute('{attribute}', '{value}');
    """, element)

  def highlight_element(self, element_or_visible_locator):
    element = element_or_visible_locator if isinstance(element_or_visible_locator, WebElement) else self.find_visible_element(element_or_visible_locator)
    color = 'purple'

    original_style = element.get_attribute('style')
    new_style = 'background-color: yellow; border: 1px solid ' + color + original_style

    self.web_driver.execute_script(f"""
      element = arguments[0];
      setTimeout(() => {'{'}
        element.setAttribute('style', '{new_style}');
      {'}'}, 0);
    """, element)
    self.web_driver.execute_script(f"""
      element = arguments[0];
      setTimeout(() => {'{'}
        element.setAttribute('style', '{original_style}');
      {'}'}, 400);
    """, element)

  def assert_is_displayed(self, visible_locator: tuple):
    assert self.find_visible_element(visible_locator).is_displayed(), f'Failed to find web element {visible_locator}'

  def get_current_url(self):
    return self.web_driver.current_url

  def wait_for_page(self, page_url):
    self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
    assert self.wait.until(lambda _: page_url in self.get_current_url())

  def click(self, element_or_visible_locator: tuple):
    element = element_or_visible_locator if isinstance(element_or_visible_locator, WebElement) else self.find_visible_element(element_or_visible_locator)
    time.sleep(1)
    element.click()
