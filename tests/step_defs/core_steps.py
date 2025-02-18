import os
import time
import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from utils.api import BrowserAPI

features_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../features/core'))

if not os.path.exists(features_dir):
    raise FileNotFoundError(f"Directory not found: {features_dir}")

for root, dirs, files in os.walk(features_dir):
  for file in files:
    if file.endswith('.feature'):
      feature_path = os.path.join(root, file)
      scenarios(feature_path)

browser_api = BrowserAPI()

@pytest.fixture(scope='session', autouse=True)
def step_after_all():
    yield None
    browser_api.web_driver.quit()


@given(parsers.parse('User goes to {url} page'))
def _(url):
  browser_api.web_driver.get('https://' + url)


@then(parsers.parse('Wait for {seconds} seconds'))
def _(seconds):
  time.sleep(float(seconds))


@then(parsers.parse('User see text: {text} in body'))
def _(text):
    if "\"" in text:
        locator = By.XPATH, f"//body//*[contains(text(),'{text}')]"
    else:
        locator = By.XPATH, f"//body//*[contains(text(),\"{text}\")]"

    browser_api.assert_is_displayed(locator)


@then(parsers.parse('User is on {url} page'))
def _(url):
   browser_api.wait_for_page(url)


@when(parsers.parse('User clicks {element_text} element'))
@then(parsers.parse('User clicks {element_text} element'))
def _(element_text):
  try:
    browser_api.click(browser_api.find_visible_by_text(element_text))
  except StaleElementReferenceException:
    browser_api.click(browser_api.find_visible_by_text(element_text))

