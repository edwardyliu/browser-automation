# Instructed Navigator Auto
A Selenium-Driven Finite State Machine For Automating Web-Tasks.

## models.py
```python
class Command:
    """Define a Command Object
    
    For executing a particular command
    """

class Task:
    """Define a Task Object
    
    Is a sequence of Command objects executed linearly
    """

class Key:
    """Define a Key Object
    
    Is the unique ID of a Task object
    """
```

#### Available Command(s):
```python
1. CLICK
    Left Mouse Click
    { "target": optional <XPATH> }

2. CLICK_AND_HOLD
    Left Mouse Click & Hold, Do Not Release
    { "target": optional <XPATH> }

3. CONTEXT_CLICK
    Right Mouse Click
    { "target": optional <XPATH> }

4. DOUBLE_CLICK
    Double Left Mouse Click
    { "target": optional <XPATH> }

5. DRAG_AND_DROP
    Mouse Drag & Drop From <SRC> To <DEST>
    { 
        "target": <XPATH>
        "argv": <XPATH>
    }

6. DRAG_AND_DROP_BY_OFFSET
    Mouse Drag & Drop From <SRC> To [<XOFFSET>, <YOFFSET>]
    { 
        "target": <XPATH>
        "argv": [<XOFFSET>, <YOFFSET>]
    }

7. GET:
    HTTP Request GET <URL>
    { "target": <URL> }

8. DGET
    Dynamic GET
    *Supports Dictionary & Web Element Finds
    { "target": <FORMAT> }

9. MOVE_TO_ELEMENT
    FireFox: Move Mouse Cursor to WebElement
    Others: Maneuver to WebElement (i.e. Scroll & Cursor)
    { "target": optional <XPATH> }

10. MOVE_TO_ELEMENT_WITH_OFFSET
    FireFox: Move Mouse Cursor to WebElement Plus [<XOFFSET>, <YOFFSET>]
    Others: Maneuver to WebElement Plus [<XOFFSET>, <YOFFSET>] (i.e. Scroll & Cursor)
    { 
        "target": <XPATH>
        "argv": [<XOFFSET>, <YOFFSET>]
    }

11. MOVE_BY_OFFSET
    FireFox: Move Mouse Cursor to [<XOFFSET>, <YOFFSET>]
    Others: Maneuver to [<XOFFSET>, <YOFFSET>] (i.e. Scroll)
    { "argv": [<XOFFSET>, <YOFFSET>] }

12. PAUSE
    Pause The Browser Instance
    { "target": <SECONDS> }

13. PRINTF
    Print Formatted String
    { "target": <FORMAT> }

14. REFRESH
    Refresh Current Instance
    { None }

15. RELEASE
    Release Mouse Click
    { "target": optional <XPATH> }

16. SEND_KEYS
    Send Keyboard Actions To The Browser Instance
    *Supports Key Logic
    *Supports Special Key Characters
    { 
        "target": optional <XPATH>
        "argv": [ [<KEY_LOGIC>, <KEY>] OR <KEY>, ... ]
    }

17. DSEND_KEYS
    Dynamic Send Keys
    *Supports Dictionary & Web Element Finds
    *Removed Key Logic Support
    *Removed Special Key Character Support
    { 
        "target": optional <XPATH>
        "argv": [ <KEY>, ... ]
    }

18. WAIT
    Wait For An Expected Condition OR Timeout
    {
        "target": An INTEGER, An XPATH Value Or A URL String
        "argv": [<OPERATION>, <EXPECTED_CONDITION>]
    }
```

#### Available Key Logic & Special Key Character(s):
* Key Logic
    ```bash
    <KEY_LOGIC>

        'KEY_DOWN'
        'KEY_UP'
        'SEND'
    ```

* Special Key Characters
    ```bash
    ${ADD}
    ${ALT}
    ${ARROW_DOWN}
    ${ARROW_LEFT}
    ${ARROW_RIGHT}
    ${ARROW_UP}
    ${BACKSPACE}
    ${BACK_SPACE}
    ${CANCEL}
    ${CLEAR}
    ${COMMAND}
    ${CONTROL}
    ${DECIMAL}
    ${DELETE}
    ${DIVIDE}
    ${DOWN}
    ${END}
    ${ENTER}
    ${EQUALS}
    ${ESCAPE}
    ${F1}
    ${F10}
    ${F11}
    ${F12}
    ${F2}
    ${F3}
    ${F4}
    ${F5}
    ${F6}
    ${F7}
    ${F8}
    ${F9}
    ${HELP}
    ${HOME}
    ${INSERT}
    ${LEFT}
    ${LEFT_ALT}
    ${LEFT_CONTROL}
    ${LEFT_SHIFT}
    ${META}
    ${MULTIPLY}
    ${NULL}
    ${NUMPAD0}
    ${NUMPAD1}
    ${NUMPAD2}
    ${NUMPAD3}
    ${NUMPAD4}
    ${NUMPAD5}
    ${NUMPAD6}
    ${NUMPAD7}
    ${NUMPAD8}
    ${NUMPAD9}
    ${PAGE_DOWN}
    ${PAGE_UP}
    ${PAUSE}
    ${RETURN}
    ${RIGHT}
    ${SEMICOLON}
    ${SEPARATOR}
    ${SHIFT}
    ${SPACE}
    ${SUBTRACT}
    ${TAB}
    ${UP}
    ```

#### Available Operation & Expected Condition(s):
* Operation
    ```bash
    <OPERATION>
        
        'UNTIL'
        'UNTIL_NOT'
    ```

* Expected Conditions
    ```bash
    "ELEMENT_LOCATED_SELECTION_STATE_TO_BE"
    "ELEMENT_LOCATED_TO_BE_SELECTED"
    "ELEMENT_TO_BE_CLICKABLE"
    "ELEMENT_TO_BE_SELECTED"
    "FRAME_TO_BE_AVAILABLE_AND_SWITCH_TO_IT"
    "INVISIBILITY_OF_ELEMENT"
    "INVISIBILITY_OF_ELEMENT_LOCATED"
    "NEW_WINDOW_IS_OPENED"
    "NUMBER_OF_WINDOWS_TO_BE"
    "PRESENCE_OF_ALL_ELEMENTS_LOCATED"
    "PRESENCE_OF_ELEMENT_LOCATED"
    "STALENESS_OF"
    "TEXT_TO_BE_PRESENT_IN_ELEMENT"
    "TEXT_TO_BE_PRESENT_IN_ELEMENT_VALUE"
    "TITLE_CONTAINS"
    "TITLE_IS"
    "URL_CHANGES"
    "URL_CONTAINS"
    "URL_MATCHES"
    "URL_TO_BE"
    "VISIBILITY_OF"
    "VISIBILITY_OF_ALL_ELEMENTS_LOCATED"
    "VISIBILITY_OF_ANY_ELEMENTS_LOCATED"
    "VISIBILITY_OF_ELEMENT_LOCATED"
    ```

## driver.py
```python
class Driver:
    """Define a Driver Object
    
    A Selenium-Driven WebDriver Instance
    The Task Executor
    """
```

## job.py
```python
class Job:
    """ Define a Job Object

    A List of Task Objects Executed Linearly
    Assigned to a Worker Node
    """
```

## template.py
```python
Multiple lambda Functions - Used to Construct an E-mail Template
```
