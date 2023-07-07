import unittest
from appium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.mobileby import MobileBy as AppiumBy

#parameters of the level editor
numberOfTilesInMenu=15
xSize=16
ySize=20
length = 10

class NewLevelFlow (unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps["platformName"] = "Windows"
        desired_caps["app"] = "C:\\KINGTestTask\\LevelEditor.exe"

        self.driver=webdriver.Remote(
            command_executor="http://127.0.0.1:4723",
            desired_capabilities=desired_caps
        )

        self.driver.implicitly_wait(15)
        self.driver.maximize_window()

    @classmethod
    def tearDownClass(self):
            self.driver.close()
            self.driver.quit()

    def test_init(self):
        try:
            #new level
            newLevelButton=self.driver.find_element_by_accessibility_id("New level.<empty>.LevelEditor - 1.0.0")
            newLevelButton.click()
            windows = self.driver.window_handles
            handle1 = self.driver.window_handles[0]

            # describing tiles menu
            tilesMenu = self.driver.find_element_by_xpath(
                "(//Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Custom[starts-with(@AutomationId, '.<empty>.LevelEditor - ')])[last()]")
            bounding_rect = tilesMenu.get_attribute("BoundingRectangle")
            rect_values = bounding_rect.split(' ')
            leftT = int(rect_values[0].split(':')[1])
            topT = int(rect_values[1].split(':')[1])
            widthT = int(rect_values[2].split(':')[1])
            heightT = int(rect_values[3].split(':')[1])
            stepXT=int (widthT/numberOfTilesInMenu)

            # describing level builder frame
            mainField = self.driver.find_element_by_xpath(
                "(//Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Custom[starts-with(@AutomationId, '.<empty>.LevelEditor - ')])[1]")
            bounding_rect = mainField.get_attribute("BoundingRectangle")
            rect_values = bounding_rect.split(' ')
            leftM = int(rect_values[0].split(':')[1])
            topM = int(rect_values[1].split(':')[1])
            widthM = int(rect_values[2].split(':')[1])
            heightM = int(rect_values[3].split(':')[1])
            stepXM = int(widthM / xSize)
            stepYM = int(heightM / ySize)

            action_chains = ActionChains(self.driver)

            for j in range(1, ySize+1):
                if j == numberOfTilesInMenu:
                    currentTileNumber = j
                else:
                    currentTileNumber= j % numberOfTilesInMenu

                action_chains.move_to_element_with_offset(tilesMenu, currentTileNumber * stepXT - stepXT/2,int(heightT / 2)).click()
                for i in range(1, xSize+1):
                #for i in range(1, 2):
                    #Fill current brick
                    action_chains.move_to_element_with_offset(mainField, stepXM * i - stepXM/2, stepYM * j - stepYM/2).click()

            action_chains.perform()

            #assign a name
            levelNameElement = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Edit[starts-with(@AutomationId, '.<empty>.LevelEditor - ')]")
            symbols = string.ascii_lowercase
            assignedName = ''.join(random.choice(symbols) for _ in range(length))
            levelNameElement.send_keys(assignedName)

            #assign background
            backgroundElement = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/ComboBox")
            backgroundElement.click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            backgroundOptions = self.driver.find_elements_by_xpath("/Window[@Name='LevelEditor']/MenuItem[starts-with(@AutomationId,'Background-')]")
            random_back = random.choice(backgroundOptions)
            newBackground = random_back.get_attribute("Name")
            random_back.click()

            self.driver.switch_to.window(handle1)

            # save the changes
            saveLevelButton = self.driver.find_element_by_accessibility_id("Save.<empty>.LevelEditor - 1.0.0")
            saveLevelButton.click()

            windows=self.driver.window_handles
            self.driver.switch_to.window(self.driver.window_handles[0])

            wait = WebDriverWait(self.driver, 10)
            assetsFolder=wait.until(EC.visibility_of_element_located((AppiumBy.NAME, "assets")))
            assetsFolder.click()
            assetsFolder.send_keys(Keys.ENTER)

            levelsFolder = self.driver.find_element_by_name("Levels")
            levelsFolder.click()
            levelsFolder.send_keys(Keys.ENTER)

            elements = wait.until(EC.visibility_of_all_elements_located((AppiumBy.XPATH, "//ListItem[@ClassName='UIItem']")))

            symbols = string.ascii_lowercase
            fileName = ''.join(random.choice(symbols) for _ in range(length))

            fileNameField = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH,
                       "//Window[@Name='Save a level']/Pane[@ClassName='DUIViewWndClassName']/ComboBox/Edit[@ClassName='Edit']")))

            fileNameField.send_keys(fileName)
            fileNameField.send_keys(Keys.ENTER)

            self.driver.switch_to.window(handle1)

            #Open a new level from the assets\Levels folder
            openLevelButton = self.driver.find_element_by_accessibility_id("Open Level.<empty>.LevelEditor - 1.0.0")
            openLevelButton.click()
            windows = self.driver.window_handles
            handle1 = self.driver.window_handles[1]
            self.driver.switch_to.window(self.driver.window_handles[0])
            assetsFolder=wait.until(EC.visibility_of_element_located((AppiumBy.NAME, "assets")))
            assetsFolder.click()
            assetsFolder.send_keys(Keys.ENTER)
            levelsFolder =wait.until(EC.visibility_of_element_located((AppiumBy.NAME, "Levels")))
            levelsFolder.click()
            levelsFolder.send_keys(Keys.ENTER)
            elements =wait.until(EC.visibility_of_all_elements_located((AppiumBy.XPATH, "//ListItem[@ClassName='UIItem']")))
            random_element = random.choice(elements)
            random_element.click()
            random_element.send_keys(Keys.ENTER)
            self.driver.switch_to.window(handle1)

            #Then open your level again.
            openLevelButton = self.driver.find_element_by_accessibility_id("Open Level.<empty>.LevelEditor - 1.0.0")
            openLevelButton.click()
            windows = self.driver.window_handles
            handle1 = self.driver.window_handles[1]
            self.driver.switch_to.window(self.driver.window_handles[0])
            assetsFolder=wait.until(EC.visibility_of_element_located((AppiumBy.NAME, "assets")))
            assetsFolder.click()
            assetsFolder.send_keys(Keys.ENTER)
            levelsFolder =wait.until(EC.visibility_of_element_located((AppiumBy.NAME, "Levels")))
            levelsFolder.click()
            levelsFolder.send_keys(Keys.ENTER)

            elements = wait.until(EC.visibility_of_all_elements_located((AppiumBy.XPATH, "//ListItem[@ClassName='UIItem']")))

            for el in elements:
                if el.get_attribute("Name") == fileName:
                    found_element = el
                    found_element.click()
                    found_element.send_keys(Keys.ENTER)
                    self.driver.switch_to.window(handle1)
                    break

            #The set title and level components should be the same.
            # checking the name of the level
            element = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Edit[starts-with(@AutomationId, '.<empty>.LevelEditor - ')]")
            nameToCheck = element.text
            self.assertEqual(nameToCheck, assignedName,"Level name does not match the expected value. Possible problem with changing level name or saving the changes.")

            # checking the background name
            backgroundElement = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/ComboBox")
            self.assertEqual(backgroundElement.text, newBackground, "Background does not match the expected value. Possible problem with changing background or saving the changes.")
        except Exception as e:
            print(f"An exception occurred: {e}")
            raise e