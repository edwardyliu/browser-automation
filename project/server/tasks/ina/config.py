# project/server/tasks/ina/config.py

# === Import(s) ===
# => System <=
import os
import re
import logging
from pathlib import Path

# => External <=
from selenium.webdriver.support import expected_conditions as EC

# === Configuration(s) ===
# => Logging <=
LOG_LEVEL=logging.ERROR

# => Path & Directories <=
CACHE_DIRPATH=os.path.join(Path(__file__).parents[0], "resources/cache/")
WEBDRIVER_EXEPATH=os.path.join(Path(__file__).parents[0], "resources/geckodriver")

# => Pattern(s) & Regex(s) <=
RE_NUMERAL=re.compile(r"([0-9]+)")
RE_POSITIONAL=re.compile(r"(\$\{.*?\})")

# => Default(s) <=
ARGV="@"
LUTV="@#"
FINDV="@"
LAST="-1"

DEFAULT_WAIT=1.5
DEFAULT_TIMEOUT=7.5

DEFAULT_FORMAT=(
    "${usrId}," +       # user ID
    "${0}," +           # env, name
    "${" + LAST + "}"   # order ID, [Optionally] memos
)

DEFAULT_SMTP_SERVER="127.0.0.1"
DEFAULT_SMTP_PORT=25
DEFAULT_SENDER_EMAIL="support@nauto.com"

# => Expected Condition(s) <=
EXPECTED_CONDITIONS={
    "ELEMENT_LOCATED_SELECTION_STATE_TO_BE": (EC.element_located_selection_state_to_be, "LOCATOR"),
    "ELEMENT_LOCATED_TO_BE_SELECTED": (EC.element_located_to_be_selected, "LOCATOR"),
    "ELEMENT_TO_BE_CLICKABLE": (EC.element_to_be_clickable, "LOCATOR"),
    "ELEMENT_TO_BE_SELECTED": (EC.element_to_be_selected, "ELEMENT"),
    "FRAME_TO_BE_AVAILABLE_AND_SWITCH_TO_IT": (EC.frame_to_be_available_and_switch_to_it, "LOCATOR"),
    "INVISIBILITY_OF_ELEMENT": (EC.invisibility_of_element, "LOCATOR"),
    "INVISIBILITY_OF_ELEMENT_LOCATED": (EC.invisibility_of_element_located, "LOCATOR"),
    "NEW_WINDOW_IS_OPENED": (EC.new_window_is_opened, "INTEGER"),
    "NUMBER_OF_WINDOWS_TO_BE": (EC.number_of_windows_to_be, "INTEGER"),
    "PRESENCE_OF_ALL_ELEMENTS_LOCATED": (EC.presence_of_all_elements_located, "LOCATOR"),
    "PRESENCE_OF_ELEMENT_LOCATED": (EC.presence_of_element_located, "LOCATOR"),
    "STALENESS_OF": (EC.staleness_of, "ELEMENT"),
    "TEXT_TO_BE_PRESENT_IN_ELEMENT": (EC.text_to_be_present_in_element, "LOCATOR"),
    "TEXT_TO_BE_PRESENT_IN_ELEMENT_VALUE": (EC.text_to_be_present_in_element_value, "LOCATOR"),
    "TITLE_CONTAINS": (EC.title_contains, "STRING"),
    "TITLE_IS": (EC.title_is, "STRING"),
    "URL_CHANGES": (EC.url_changes, "STRING"),
    "URL_CONTAINS": (EC.url_contains, "STRING"),
    "URL_MATCHES": (EC.url_matches, "STRING"),
    "URL_TO_BE": (EC.url_to_be, "STRING"),
    "VISIBILITY_OF": (EC.visibility_of, "ELEMENT"),
    "VISIBILITY_OF_ALL_ELEMENTS_LOCATED": (EC.visibility_of_all_elements_located, "LOCATOR"),
    "VISIBILITY_OF_ANY_ELEMENTS_LOCATED": (EC.visibility_of_any_elements_located, "LOCATOR"),
    "VISIBILITY_OF_ELEMENT_LOCATED": (EC.visibility_of_element_located, "LOCATOR")
}

# => Special Key Character(s) <=
KEY_UP="KEY_UP"
KEY_DOWN="KEY_DOWN"
KEYS={
    "${ADD}": u'\ue025',
    "${ALT}": u'\ue00a',
    "${ARROW_DOWN}": u'\ue015',
    "${ARROW_LEFT}": u'\ue012',
    "${ARROW_RIGHT}": u'\ue014',
    "${ARROW_UP}": u'\ue013',
    "${BACKSPACE}": u'\ue003',
    "${BACK_SPACE}": u'\ue003',
    "${CANCEL}": u'\ue001',
    "${CLEAR}": u'\ue005',
    "${COMMAND}": u'\ue03d',
    "${CONTROL}": u'\ue009',
    "${DECIMAL}": u'\ue028',
    "${DELETE}": u'\ue017',
    "${DIVIDE}": u'\ue029',
    "${DOWN}": u'\ue015',
    "${END}": u'\ue010',
    "${ENTER}": u'\ue007',
    "${EQUALS}": u'\ue019',
    "${ESCAPE}": u'\ue00c',
    "${F1}": u'\ue031',
    "${F10}": u'\ue03a',
    "${F11}": u'\ue03b',
    "${F12}": u'\ue03c',
    "${F2}": u'\ue032',
    "${F3}": u'\ue033',
    "${F4}": u'\ue034',
    "${F5}": u'\ue035',
    "${F6}": u'\ue036',
    "${F7}": u'\ue037',
    "${F8}": u'\ue038',
    "${F9}": u'\ue039',
    "${HELP}": u'\ue002',
    "${HOME}": u'\ue011',
    "${INSERT}": u'\ue016',
    "${LEFT}": u'\ue012',
    "${LEFT_ALT}": u'\ue00a',
    "${LEFT_CONTROL}": u'\ue009',
    "${LEFT_SHIFT}": u'\ue008',
    "${META}": u'\ue03d',
    "${MULTIPLY}": u'\ue024',
    "${NULL}": u'\ue000',
    "${NUMPAD0}": u'\ue01a',
    "${NUMPAD1}": u'\ue01b',
    "${NUMPAD2}": u'\ue01c',
    "${NUMPAD3}": u'\ue01d',
    "${NUMPAD4}": u'\ue01e',
    "${NUMPAD5}": u'\ue01f',
    "${NUMPAD6}": u'\ue020',
    "${NUMPAD7}": u'\ue021',
    "${NUMPAD8}": u'\ue022',
    "${NUMPAD9}": u'\ue023',
    "${PAGE_DOWN}": u'\ue00f',
    "${PAGE_UP}": u'\ue00e',
    "${PAUSE}": u'\ue00b',
    "${RETURN}": u'\ue006',
    "${RIGHT}": u'\ue014',
    "${SEMICOLON}": u'\ue018',
    "${SEPARATOR}": u'\ue026',
    "${SHIFT}": u'\ue008',
    "${SPACE}": u'\ue00d',
    "${SUBTRACT}": u'\ue027',
    "${TAB}": u'\ue004',
    "${UP}": u'\ue013'
}
