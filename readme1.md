# Tools
WinAppDriver 1.2.1
Appium Python Client 1.3.0
inspect.exe from Windows SDK
WinAppDriverUIRecorder

# Installation instructions
1. Install WinAppDriver 1.2.1 from https://github.com/Microsoft/WinAppDriver/releases
2. Install Appium Python Client python -m pip install Appium-Python-Client==1.3.0
3. Install Selenium 3.141.0
4. Enable Developer Mode in Windows settings
5. Run WinAppDriver.exe from the installation directory 
 
# Task
The objective is to implement a set of test cases:

### Case: New level flow
After opening the editor, create a new level by clicking on the **New level** button.
After that, fill each row with one specific brick type  
Once done, set a name for your level in the **Title** text box, save the level in the **assets\Levels** folder and give it a name.
Open a new level from the **assets\Levels** folder and then open your level again.
The set title and level components should be the same.

### Case: Modify existing level
Open any of the levels provided from **assets\Levels** folder.
Change the title to anything you like.
Change the background to any other background.
Save.

### Case: Open all levels
Go through all provided levels from **assets\Levels** folder and open them one by one.

### Case: Place specific tiles in specific place
Open Level1 from **assets\Levels** folder.
Replace the first gray tile on the left with a red tile.
Replace the first yellow tile on the left with a blue tile.
Place any tile in the 4th column from the right on the first row.
Save.

# Solution description

The given tests were automated using the WinAppDriver + Appium Python Client framework.
UI elements were located using XPath, Name or AccessibilityID locators.
Explicit and implicit waits were used to make sure that elements are displayed on screen.
unittest library was used to run test cases.
Setup and teardown were described for each test as well.


# Screencast link









