from pathlib import Path
from time import sleep
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# Set the default timeout
capabilities = DesiredCapabilities.CHROME
capabilities["pageLoadStrategy"] = "normal"
capabilities["timeouts"] = {"implicit": 30000, "pageLoad": 30000, "script": 30000}

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)
"""

def ocr(image: Path):
  return
  driver.get("https://web.baimiaoapp.com/")
  sleep(6)
  def sel(css_selector: str):
    return driver.find_element(by=By.CSS_SELECTOR, value=css_selector)
  not_login = sel(".not-login")
  login_btn = sel(".login-btn")
  login_btn.click()
  sleep(1)
  email = "overflowcat@gmail.com"
  password = "sll99080000"
  email_input = sel(".login-username")
  email_input.clear
  password_input = sel(".login-password")
  password_input.clear()
  email_input.send_keys(email)
  password_input.send_keys(password)

  sel('.btn-do-login').click()

  sleep(6)

  file_input = sel('div.board > div > div > input[type="file"]')
  image_path = str(Path(image_path).resolve())
  file_input.send_keys(image_path)
  submit_btn = sel('.btn-submit.active')
  submit_btn.click()

  sleep(6)

  view_results_btn = sel('.btn-submit.active')
  view_results_btn.click()

  sleep(1.5)

  editor_content = driver.execute_script("""
      const editor = document.querySelector('.ql-editor');
      return editor.innerText;
  """)

  # try:
  #   sel(".icon-arrow-vip").click()
  #   sleep(1.2)
  #   sel(".detail-logout").click()
  #   sleep(1)
  #   driver.quit()
  # except Exception:
  #     pass
  # try:
  #     driver.quit()
  # except Exception:
  #     pass
  return editor_content
