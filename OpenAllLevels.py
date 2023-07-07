import unittest
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OpenAllLevels (unittest.TestCase):
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
            #open levels
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

            wait = WebDriverWait(self.driver, 10)
            elements = wait.until(EC.visibility_of_all_elements_located((AppiumBy.XPATH, "//ListItem[@ClassName='UIItem']")))

            index =0
            length = len(elements)
            elements[index].click()
            elements[index].send_keys(Keys.ENTER)
            self.driver.switch_to.window(handle1)
            levelName = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Edit[starts-with(@AutomationId, '.<empty>.LevelEditor - ')]")
            self.assertIsNotNone(levelName, "Something went wrong with level opening.")
            index+=1

            while index<length:
                openLevelButton = self.driver.find_element_by_accessibility_id("Open Level.<empty>.LevelEditor - 1.0.0")
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
                length = len(elements)
                elements[index].click()
                elements[index].send_keys(Keys.ENTER)
                self.driver.switch_to.window(handle1)
                levelName = self.driver.find_element_by_xpath("/Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Edit[starts-with(@AutomationId, '.<empty>.LevelEditor - ')]")
                self.assertIsNotNone(levelName, "Something went wrong with level opening.")
                index += 1
        except Exception as e:
            print(f"An exception occurred: {e}")
            raise e