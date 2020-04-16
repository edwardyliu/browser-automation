# == Import(s) ==
# => Local
from . import parser
from . import machine

# => External
from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)
dcgs = parser.get_dcgs()

instance = machine.model.Machine("test", driver, dcgs[0].actions)
for instance.next():
    print("next: ")