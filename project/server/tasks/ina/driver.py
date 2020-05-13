# project/server/tasks/ina/driver.py

# === Import(s) ===
# => Local <=
from . import utils
from . import config
from . import models

# => System <=
import re
import json

# => External <=
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# === Object Definition ===
class Driver(object):
    """Define a Driver Object
    
    A Selenium WebDriver Instance
    """

    def __init__(self, uid:str):
        self.uid = uid
        self.log = utils.get_logger(f"INA.Driver.{self.uid}")
        self.driver = self.geckodriver()

    def __del__(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
    
    def __str__(self):
        return f"INA.Driver(uid={self.uid})"

    # === Getter(s) ===
    def geckodriver(self)->webdriver:
        """Get a Selenium WebDriver instance: geckodriver

        Returns
        -------
        webdriver
        """

        options = webdriver.FirefoxOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Firefox(executable_path=config.WEBDRIVER_EXEPATH, options=options)
        driver.maximize_window()
        return driver

    def taskkey(self)->models.Key:
        """Get task key

        Returns
        -------
        models.Key
        """

        if hasattr(self, "task"): return self.task.key 
        else: return None

    # === Setter(s) ===
    def assign(self, task:models.Task):
        """Assign the Task object to this driver

        """

        self.reset()
        self.task = task
        self.log.debug(f"assigned: {self.task}")

    def reset(self):
        """Reset state information

        """

        self.lut = {}
        self.results = {}
    
    # === Functional ===
    def exec(self, lut:dict=None)->dict:
        """Execute (i.e. run) the Task object
        
        Parameters
        ----------
        lut: dict, optional
            An external look-up table

        Returns
        -------
        dict: An internal look-up table
        """

        self.lut = lut
        for cmd in self.task.cmds: getattr(self, cmd.label.lower())(target=cmd.target, argv=cmd.argv)
        return self.results
    
    # === Utility Function(s) ===
    def argv_key(self)->str:
        """Get next available key for argv
        
        Returns
        -------
        str
        """

        argv_key = "${0}"
        while self.results.get(argv_key):
            pattern = re.findall(config.RE_NUMERAL, argv_key)[0]
            argv_key = argv_key.replace(pattern, str(int(pattern)+1))
        return argv_key

    def find_element_by_xpath(self, target:str, wait:bool=True):
        """Find first element by XPATH

        Parameters
        ----------
        target: str
            An XPATH value

        Returns
        -------
        WebElement
        """

        if wait and self.wait(target, ("UNTIL", "PRESENCE_OF_ELEMENT_LOCATED")):
            elem = self.driver.find_element_by_xpath(target)
        else:
            elem = None
            try: elem = self.driver.find_element_by_xpath(target)
            except exceptions.NoSuchElementException:
                self.log.error(f"find_element_by_xpath: No Such Element Exception - {self.task}")
            
        return elem

    def find_elements_by_xpath(self, target:str, wait:bool=True)->list:
        """Find all elements by XPATH

        Parameters
        ----------
        target: str
            An XPATH value

        Returns
        -------
        list: A list of Selenium WebElement(s)
        """

        if wait and self.wait(target, ("UNTIL", "PRESENCE_OF_ELEMENT_LOCATED")):
            elems = self.driver.find_elements_by_xpath(target)
        else:
            elems = []
            try: elems = self.driver.find_elements_by_xpath(target)
            except exceptions.NoSuchElementException:
                self.log.error(f"find_elements_by_xpath: No Such Element Exception - {self.task}")

        return elems

    def find(self, target:str)->str:
        """Find first element by XPATH & get its text value

        Parameters
        ----------
        target: str
            An XPATH value
        
        Returns
        -------
        str
        """
        
        res = "N/F"
        elem = self.find_element_by_xpath(target)
        if elem: res = elem.text
        
        return res

    def find_all(self, target:str)->str:
        """Find all elements by XPATH & get their text values

        Parameters
        ----------
        target: str
            An XPATH value
        
        Returns
        -------
        str: A semicolon separated string of WebElement.text
        """

        lst = []
        elems = self.find_elements_by_xpath(target)
        for elem in elems:
            if elem: lst.append(elem.text)
        
        if lst: return "; ".join(lst)
        else: return "N/F"

    def enqueue_key_action(self, ac, logic:str, keys:str, target=None):
        """Enqueue key action, however do not perform

        Parameters
        ----------
        ac: ActionChains
            A Selenium ActionChains object
        logic: str
            The key logic
        keys: str
            The key character(s)
        target: WebElement, optional
            A Selenium WebElement
        """

        if logic == config.KEY_DOWN: ac.key_down(keys, element=target)
        elif logic == config.KEY_UP: ac.key_up(keys, element=target)
        else:
            if target: ac.send_keys_to_element(target, keys)
            else: ac.send_keys(keys)
    
    def enact_keyboard_actions(self, target, argv:list):
        """Perform a series of keyboard actions

        Parameters
        ----------
        target: WebElement, optional
            A Selenium WebElement
        argv: list
            A list of key actions
        """

        ac = ActionChains(self.driver)
        for arg in argv:
            if isinstance(arg, list) or isinstance(arg, tuple):
                try:
                    logic = arg[0]
                    keys = self.raw2keys(arg[1])
                except IndexError: raise IndexError(f"INA.Driver.enact_keyboard_actions: IndexError '{argv}'=>{arg}")
            else:
                logic = "SEND"
                keys = self.raw2keys(str(arg))
            
            if logic == "SEND": 
                self.enqueue_key_action(ac, logic, keys, target)
            else: 
                for key in keys: self.enqueue_key_action(ac, logic, key, target)
        ac.perform()

    def raw2ec(self, target:str, arg:str):
        """Parse raw strings into an expected condition

        Parameters
        ----------
        target: str
            Either an Integer, an XPATH or a URL
        arg: str
            Either 'INTEGER', 'LOCATOR' or 'ELEMENT'
        
        Returns
        -------
        expected_condition
        """

        if arg == "INTEGER": result = int(target)
        elif arg == "LOCATOR": result = (By.XPATH, target)
        elif arg == "ELEMENT": result = self.find_element_by_xpath(target)
        else: result = target

        return result

    def raw2keys(self, target:str)->str:
        """Parse raw string into key characters
        
        Special values are replace w/ their corresponding special characters
        
        Parameters
        ----------
        target: str
            The raw string
        
        Returns
        -------
        str
        """

        for replacement in re.findall(config.RE_POSITIONAL, target):
            target = target.replace(replacement, config.KEYS[replacement])
        return target

    def peek(self, target:str)->str:
        """Peek the external look-up table.
        If not found, peek the web page (assumption: XPATH)

        Parameters
        ----------
        target: str
            A dict key value or XPATH value
        
        Returns
        -------
        str
        """

        if self.lut.get(target): 
            res = self.lut[target]
            if isinstance(res, str): return res
            elif isinstance(res, list): return ", ".join(res)
            elif isinstance(res, dict): return json.dumps(res)
            else: 
                try: return str(res)
                except Exception: return f"ERROR: Cannot STRINGIFY Type({type(res)})"
        else: return self.find(target)
    
    def scan(self, target:str)->str:
        """Parse raw string into formatted string

        Parameters
        ----------
        target: str
            The string format
            
        Returns
        -------
        str
        """
        
        for placeholder in re.findall(config.RE_POSITIONAL, target):
            value = placeholder[2:-1]
            if value == config.LUTV: 
                span = []
                for i, j in self.lut.items(): span.append(f"{i}: {j}")
                target = target.replace(placeholder, ", ".join(span))
            elif value == config.ARGV: target = target.replace(placeholder, ", ".join(self.results.values()))
            elif value.isdigit(): target = target.replace(placeholder, self.results.get(placeholder, "N/A"))
            elif value[0] == config.FINDV: target = target.replace(placeholder, self.find_all(value[1:]))
            else: target = target.replace(placeholder, self.peek(value))
        
        return target
    
    # === Command Function(s) ===
    def get(self, target:str, argv:list=None):
        """Get URL page

        Parameters
        ----------
        target: str
            A URL string
        """

        try: 
            self.driver.get(target)
            self.pause(config.DEFAULT_WAIT)
        
        except exceptions.InvalidArgumentException:
            self.log.error(f"get: Invalid Argument Exception - Malformed URL - '{target}' is not a valid URL - {self.task}")

        except exceptions.WebDriverException:
            self.log.error(f"get: WebDriver Exception - Reached Error Page - {self.task}")

    def refresh(self, target:str=None, argv:list=None):
        """Refresh current page

        """

        self.driver.refresh()
    
    def click(self, target:str=None, argv:list=None):
        """Click a Selenium WebElement

        Parameters
        ----------
        target: str, optional
            An XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).click(on_element=elem).perform()
        else: ActionChains(self.driver).click().perform()

    def click_and_hold(self, target:str=None, argv:list=None):
        """Click and hold a Selenium WebElement

        Parameters
        ----------
        target: str, optional
            An XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).click_and_hold(on_element=elem).perform()
        else: ActionChains(self.driver).click_and_hold().perform()
    
    def release(self, target:str=None, argv:list=None):
        """Release mouse click

        Parameters
        ----------
        target: str, optional
            An XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).release(on_element=elem).perform()
        else: ActionChains(self.driver).release().perform()

    def context_click(self, target:str=None, argv:list=None):
        """Context click (i.e. right-click) a Selenium WebElement

        Parameters
        ----------
        target: str, optional
            An XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).context_click(on_element=elem).perform()
        else: ActionChains(self.driver).context_click().perform()
    
    def double_click(self, target:str=None, argv:list=None):
        """Double click a Selenium WebElement

        Parameters
        ----------
        target: str, optional
            An XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).double_click(on_element=elem).perform()
        else: ActionChains(self.driver).double_click().perform()
    
    def drag_and_drop(self, target:str, argv:list):
        """Drag and drop from source to destination

        Parameters
        ----------
        target: str
            An XPATH value, the source Selenium WebElement
        argv: [str]
            An XPATH value, the destination Selenium WebElement
        """

        try:
            src = self.find_element_by_xpath(target)
            dest = self.find_element_by_xpath(argv[0])
            if src and dest: ActionChains(self.driver).drag_and_drop(source=src, target=dest).perform()
            
        except IndexError:
            self.log.error(f"drag_and_drop: Index Error - {self.task}")
            raise IndexError(f"INA.Driver.drag_and_drop: Index Error - {argv} - {self.task}")

    def drag_and_drop_by_offset(self, target:str, argv:list):
        """Drag and drop from source to (xoffset, yoffset)

        Parameters
        ----------
        target: str
            An XPATH value
        argv: [str]
            The x & y offsets
        """

        try:
            src = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if src: ActionChains(self.driver).drag_and_drop_by_offset(source=src, xoffset=xoffset, yoffset=yoffset).perform()
            
        except IndexError:
            self.log.error(f"drag_and_drop_by_offset: Index Error - {self.task}")
            raise IndexError(f"INA.Driver.drag_and_drop_by_offset: Index Error - {argv} - {self.task}")
    
    def move_to_element(self, target:str, argv:list=None):
        """Move mouse cursor to a Selenium WebElement

        Parameters
        ----------
        target: str
            An XPATH value
        """

        elem = self.find_element_by_xpath(target)
        if elem: ActionChains(self.driver).move_to_element(to_element=elem).perform()
        
    def move_to_element_with_offset(self, target:str, argv:list):
        """Move mouse cursor to a Selenium WebElement plus offset

        Parameters
        ----------
        target: str
            An XPATH value
        argv: [str]
            The x & y offsets
        """

        try:
            elem = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if elem: ActionChains(self.driver).move_to_element_with_offset(to_element=elem, xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error(f"move_to_element_with_offset: Index Error - {self.task}")
            raise IndexError(f"INA.Driver.move_to_element_with_offset: Index Error - {argv} - {self.task}")
    
    def move_by_offset(self, target:str, argv:list):
        """Move mouse cursor to offset

        Parameters
        ----------
        argv: [str]
            The x & y offsets
        """

        try:
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            ActionChains(self.driver).move_by_offset(xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error(f"move_by_offset: Index Error - {self.task}")
            raise IndexError(f"INA.Driver.move_by_offset: Index Error - {argv} - {self.task}")
    
    def send_keys(self, target:str, argv:list):
        """Send keys
        NOTE. Support sending special characters including ${ENTER}, ${ALT}, ${SHIFT}, etc.
        
        Parameters
        ----------
        target: str, optional
            An XPATH value
        argv: [tuple2]
            A list of string tuple2 values
            e.g. [("KEY_DOWN", "${SHIFT}"), "uppercase", ("KEY_UP", "${SHIFT}")]
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: self.enact_keyboard_actions(elem, argv)
        else: self.enact_keyboard_actions(None, argv)
    
    def pause(self, target:str, argv:list=None):
        """Pause WebDriver instance

        Parameters
        ----------
        target: str
            A float, the number of seconds to pause
        """
        
        try:
            seconds = float(target)
            ActionChains(self.driver).pause(seconds).perform()

        except ValueError:
            self.log.error(f"pause: Value Error - {self.task}")
            raise ValueError(f"INA.Driver.pause: Value Error - {target} - {self.task}")
    
    def wait(self, target:str, argv:list)->bool:
        """Wait for expected condition

        Parameters
        ----------
        target: str
            Either an Integer, an XPATH or a URL
        argv: [str]
            A string tuple2 containing the operation and expected condition
        """

        try:
            operation = argv[0]
            expected_condition = config.EXPECTED_CONDITIONS.get(argv[1])

            if expected_condition:
                res = self.raw2ec(target, expected_condition[1])
                if operation == "UNTIL_NOT": WebDriverWait(self.driver, timeout=config.DEFAULT_TIMEOUT).until_not(expected_condition[0](res))
                else: WebDriverWait(self.driver, timeout=config.DEFAULT_TIMEOUT).until(expected_condition[0](res))
                
                return True
            else:
                self.log.error(f"wait: Value Error - {self.task}")
                raise ValueError(f"INA.Driver.wait: Value Error - {argv[1]} - {self.task}")

        except IndexError:
            self.log.error(f"wait: Index Error - {self.task}")
            raise IndexError(f"INA.Driver.wait: Index Error - {argv} - {self.task}")
        
        except exceptions.TimeoutException:
            self.log.error("wait: Timeout Exception")
            return False
    
    # => Dynamic Command Function(s) <=
    # i.e. Command Functions w/ Look-Up Support
    def dget(self, target:str, argv:list=None):
        """Dynamic get
        Support dictionary & web element look-up

        Parameters
        ----------
        target: str
            The string format
        """

        self.get(self.scan(target))

    def dclick(self, target:str, argv:list=None):
        """Dynamic click
        Support dictionary & web element look-up

        Parameters
        ----------
        target: str
            The string format
        """

        self.click(self.scan(target))

    def dsend_keys(self, target:str, argv:list):
        """Dynamic send keys
        NOTE. Support dictionary & web element look-ups. 
        However, do not support key logic & special character parsing.        

        Parameters
        ----------
        target: str, optional
            An XPATH value
        argv: [str]
            A list of string formats
        """

        values = map(lambda arg: self.scan(arg), filter(lambda arg: isinstance(arg, str), argv))
        if target:
            elem = self.find_element_by_xpath(target)
            if elem: self.enact_keyboard_actions(elem, values)
        else: self.enact_keyboard_actions(None, values)
    
    def printf(self, target:str, argv:list=None):
        """Print formatted

        Find & replace all special sequences to generate a formatted string

        Parameters
        ----------
        target: str
            The string format
        """
        
        key = self.argv_key()
        self.results[key] = ""
        
        if target: self.results[key] = self.scan(target)
    