import unittest
import random
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

testname="Test"

class ModifyExistingLevel (unittest.TestCase):
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
            #open existing level
            openLevelButton=self.driver.find_element_by_accessibility_id("Open Level.<empty>.LevelEditor - 1.0.0")
            openLevelButton.click()

            #change focus to dialogue window
            windows = self.driver.window_handles
            handle0=self.driver.window_handles[0]
            handle1=self.driver.window_handles[1]

            self.driver.switch_to.window(self.driver.window_handles[0])

            #navigate through folders and open a random level
            assetsFolder=self.driver.find_element_by_name("assets")
            assetsFolder.click()
            assetsFolder.send_keys(Keys.ENTER)

            levelsFolder = self.driver.find_element_by_name("Levels")
            levelsFolder.click()
            levelsFolder.send_keys(Keys.ENTER)

            elements = self.driver.find_elements_by_xpath("//ListItem[@ClassName='UIItem']")
            random_element = random.choice(elements)
            openedLevelName=random_element.get_attribute("Name")
            random_element.click()
            random_element.send_keys(Keys.ENTER)

            #return focus
            self.driver.switch_to.window(handle1)

            #change level name
            element = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Edit[starts-with(@AutomationId, '.<empty>.LevelEditor - ')]")
            element.send_keys(testname)
            newtext=element.text

            #change level background
            backgroundElement = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/ComboBox")
            backgroundElement.click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            backgroundOptions = self.driver.find_elements_by_xpath("/Window[@Name='LevelEditor']/MenuItem[starts-with(@AutomationId,'Background-')]")
            random_back = random.choice(backgroundOptions)
            newBackground=random_back.get_attribute("Name")
            random_back.click()
            self.driver.switch_to.window(handle1)

            #save the changes
            saveLevelButton = self.driver.find_element_by_accessibility_id("Save.<empty>.LevelEditor - 1.0.0")
            saveLevelButton.click()

            #open the same level once again and check that changes were applied
            openLevelButton.click()
            self.driver.switch_to.window(self.driver.window_handles[0])
            assetsFolder = self.driver.find_element_by_name("assets")
            assetsFolder.click()
            assetsFolder.send_keys(Keys.ENTER)
            levelsFolder = self.driver.find_element_by_name("Levels")
            levelsFolder.click()
            levelsFolder.send_keys(Keys.ENTER)

            wait = WebDriverWait(self.driver, 10)
            elements = wait.until(EC.visibility_of_all_elements_located((AppiumBy.XPATH, "//ListItem[@ClassName='UIItem']")))

            for el in elements:
                if el.get_attribute("Name") == openedLevelName:
                    found_element = el
                    found_element.click()
                    found_element.send_keys(Keys.ENTER)
                    self.driver.switch_to.window(handle1)
                    break

            #checking the name of the level
            element = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Edit[starts-with(@AutomationId, '.<empty>.LevelEditor - ')]")
            nameToCheck= element.text
            self.assertEqual(nameToCheck, newtext, "Level name does not match the expected value. Possible problem with changing level name or saving the changes.")

            #checking the background name
            backgroundElement = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/ComboBox")
            self.assertEqual(backgroundElement.text, newBackground, "Background does not match the expected value. Possible problem with changing background or saving the changes.")
        except Exception as e:
            print(f"An exception occurred: {e}")
            raise e