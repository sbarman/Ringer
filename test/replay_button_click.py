import threading
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rootedserver import RootedHTTPServer, RootedHTTPRequestHandler

# Open server at port 8080 to load test pages
port = 8080
server = RootedHTTPServer('test/pages', ('', port), RootedHTTPRequestHandler)
thread = threading.Thread(target=server.serve_forever)
thread.daemon = True
try:
    thread.start()
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)

# Load extension into Chrome
options = webdriver.ChromeOptions()
options.add_argument('load-extension=src')

driver = webdriver.Chrome(chrome_options=options)  # Optional argument, if not specified will search path.
driver.get('http://localhost:8080/button.html');

# Identify the current tabs
windows = driver.window_handles
assert len(windows) == 2

current_window = driver.current_window_handle
current_window_idx = windows.index(current_window)

if driver.current_url.endswith('mainpanel.html'):
    extension_window = current_window
    test_window = windows[1 - current_window_idx]
else:
    extension_window = windows[1 - current_window_idx]
    test_window = current_window

driver.switch_to.window(extension_window)
start_button = driver.find_element_by_id('start')
start_button.click()

driver.switch_to.window(test_window)
button1 = driver.find_element_by_id('button1')
button1.click()

driver.switch_to.window(extension_window)
stop_button = driver.find_element_by_id('stop')
stop_button.click()

replay_header = driver.find_element_by_id('ui-accordion-accordion-header-1')
replay_header.click()

replay_button = driver.find_element_by_id('replay')
WebDriverWait(driver, 10).until(EC.visibility_of(replay_button))

# Start the replay
replay_button.click()
messages = driver.find_element_by_id('messages')
WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, "//*[@id='messages']/*[1]"), 'stopped'))

windows = driver.window_handles
assert len(windows) == 3
windows.remove(extension_window)
windows.remove(test_window)
assert len(windows) == 1
replay_window = windows[0]

driver.switch_to.window(replay_window)
text_div = driver.find_element_by_id('text1')
assert text_div.get_attribute('textContent') == 'Button clicked'

driver.quit()

