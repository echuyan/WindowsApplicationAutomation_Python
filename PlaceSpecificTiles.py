import unittest
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import ctypes
import struct

levelName="Level1"
numberOfTilesInMenu=15
xSize=16
ySize=20
#Gray color: R = 158, G = 158, B = 158
#Yellow color: R = 255, G = 182, B = 0
#Red color at (389, 1016): R=255, G=0, B=0
#Blue color at (614, 1016): R=86, G=111, B=255
grayColor = (158, 158, 158)
yellowColor = ( 255, 182, 0)
redColor = (255, 0, 0)
blueColor =( 86, 111, 255)


class PlaceSpecificTiles (unittest.TestCase):
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
            #open level
            openLevelButton=self.driver.find_element_by_accessibility_id("Open Level.<empty>.LevelEditor - 1.0.0")
            openLevelButton.click()

            #change focus to dialogue window
            windows = self.driver.window_handles
            handle0=self.driver.window_handles[0]
            handle1=self.driver.window_handles[1]

            self.driver.switch_to.window(self.driver.window_handles[0])

            #navigate through folders and open a level
            assetsFolder=self.driver.find_element_by_name("assets")
            assetsFolder.click()
            assetsFolder.send_keys(Keys.ENTER)

            levelsFolder = self.driver.find_element_by_name("Levels")
            levelsFolder.click()
            levelsFolder.send_keys(Keys.ENTER)

            wait = WebDriverWait(self.driver, 10)
            elements = wait.until(EC.visibility_of_all_elements_located((AppiumBy.XPATH, "//ListItem[@ClassName='UIItem']")))

            for el in elements:
                if el.get_attribute("Name") == levelName:
                    found_element = el
                    found_element.click()
                    found_element.send_keys(Keys.ENTER)
                    self.driver.switch_to.window(handle1)
                    break

            gdi32 = ctypes.windll.gdi32
            user32 = ctypes.windll.user32
            desktop_window = user32.GetDesktopWindow()
            device_context = user32.GetDC(desktop_window)

            #getting red, blue and random tile coordinates
            redTileXOffset = 0
            blueTileXOffset = 0
            #tilesMenu = self.driver.find_element_by_xpath("(//Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Custom[starts-with(@AutomationId, '.<empty>.LevelEditor - ')])[last()]")
            tilesMenu = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, "(//Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Custom[starts-with(@AutomationId, '.<empty>.LevelEditor - ')])[last()]")))
            bounding_rect=tilesMenu.get_attribute("BoundingRectangle")
            rect_values = bounding_rect.split(' ')
            left = int(rect_values[0].split(':')[1])
            top = int(rect_values[1].split(':')[1])
            width = int(rect_values[2].split(':')[1])
            height = int(rect_values[3].split(':')[1])
            randomPos = random.randint(1, numberOfTilesInMenu)
            randomTileXOffset = int((width / numberOfTilesInMenu) * randomPos - (width / (2 * numberOfTilesInMenu)))
            tilesYOffset=int(height/2)
            pixel_color = gdi32.GetPixel(device_context, int(left + (width / numberOfTilesInMenu) * randomPos - (width / (2 * numberOfTilesInMenu))), int(top + height/2))
            rgb_bytes = struct.pack("I", pixel_color)[:3]
            randomColor = struct.unpack("BBB", rgb_bytes)

            for i in range(1, numberOfTilesInMenu):
                pixel_color = gdi32.GetPixel(device_context, int(left + (width / numberOfTilesInMenu) * i-(width / (2 * numberOfTilesInMenu))), int(top + tilesYOffset))
                rgb_bytes = struct.pack("I", pixel_color)[:3]
                rgb_struct = struct.unpack("BBB", rgb_bytes)
                if rgb_struct==redColor:
                    print("found red")
                    redTileXOffset = int((width / numberOfTilesInMenu) * i - (width / (2 * numberOfTilesInMenu)))
                else:
                    if rgb_struct==blueColor:
                        print("found blue")
                        blueTileXOffset = int((width / numberOfTilesInMenu) * i - (width / (2 * numberOfTilesInMenu)))




            #getting first gray, first yellow and [1,4] tiles positions
            mainField = self.driver.find_element_by_xpath("(//Window[@Name='LevelEditor - 1.0.0'][starts-with(@AutomationId, 'LevelEditor - ')]/Custom[starts-with(@AutomationId, '.<empty>.LevelEditor - ')])[1]")
            bounding_rect=mainField.get_attribute("BoundingRectangle")
            rect_values = bounding_rect.split(' ')
            left = int(rect_values[0].split(':')[1])
            top = int(rect_values[1].split(':')[1])
            width = int(rect_values[2].split(':')[1])
            height = int(rect_values[3].split(':')[1])
            stepX = int (width/xSize)
            stepY = int (height/ySize)
            oneFourTileXOffset=int (stepX*4-stepX/2)
            oneFourTileYOffset=int(stepY/2)
            firstGrayTileXOffset=0
            firstGrayTileYOffset=0
            firstYellowTileXOffset=0
            firstYellowTileYOffset=0
            foundGray=0
            foundYellow=0
            for i in range(1, xSize):
                for j in range(1, ySize):
                    pixel_color = gdi32.GetPixel(device_context, int(left + (width / xSize) * i-(width / (2 * xSize))), int(top + (height / ySize) * j-(height / (2 * ySize))))
                    rgb_bytes = struct.pack("I", pixel_color)[:3]
                    rgb_struct = struct.unpack("BBB", rgb_bytes)
                    if rgb_struct==grayColor and foundGray==0:
                        print("found gray")
                        foundGray=1
                        firstGrayTileXOffset = int((width / xSize) * i-(width / (2 * xSize)))
                        firstGrayTileYOffset = int((height / ySize) * j-(height / (2 * ySize)))
                    else:
                        if rgb_struct==yellowColor and foundYellow==0:
                            print("found yellow")
                            foundYellow=1
                            firstYellowTileXOffset = int((width / xSize) * i - (width / (2 * xSize)))
                            firstYellowTileYOffset = int((height / ySize) * j - (height / (2 * ySize)))



            action_chains = ActionChains(self.driver)

            # Replace the first gray tile on the left with a red tile.
            action_chains.move_to_element_with_offset(tilesMenu, redTileXOffset, tilesYOffset).click().perform()
            action_chains.move_to_element_with_offset(mainField, firstGrayTileXOffset, firstGrayTileYOffset).click().perform()
            #check the new color
            pixel_color = gdi32.GetPixel(device_context, int(left + firstGrayTileXOffset),int(top + firstGrayTileYOffset))
            rgb_bytes = struct.pack("I", pixel_color)[:3]
            rgb_struct = struct.unpack("BBB", rgb_bytes)
            self.assertEqual(rgb_struct,redColor,"Failed to change color from gray to red.")

            # Replace the first yellow tile on the left with a blue tile.
            action_chains.move_to_element_with_offset(tilesMenu, blueTileXOffset, tilesYOffset).click().perform()
            action_chains.move_to_element_with_offset(mainField, firstYellowTileXOffset, firstYellowTileYOffset).click().perform()
            pixel_color = gdi32.GetPixel(device_context, int(left + firstYellowTileXOffset), int(top + firstYellowTileYOffset))
            rgb_bytes = struct.pack("I", pixel_color)[:3]
            rgb_struct = struct.unpack("BBB", rgb_bytes)
            self.assertEqual(rgb_struct, blueColor, "Failed to change color from yellow to blue.")

            # Place any tile in the 4th column from the right on the first row.
            action_chains.move_to_element_with_offset(tilesMenu, randomTileXOffset, tilesYOffset).click().perform()
            action_chains.move_to_element_with_offset(mainField, oneFourTileXOffset, oneFourTileYOffset).click().perform()
            pixel_color = gdi32.GetPixel(device_context, int(left + oneFourTileXOffset), int(top + oneFourTileYOffset))
            rgb_bytes = struct.pack("I", pixel_color)[:3]
            rgb_struct = struct.unpack("BBB", rgb_bytes)

            # Save.
            saveLevelButton = self.driver.find_element_by_accessibility_id("Save.<empty>.LevelEditor - 1.0.0")
            saveLevelButton.click()
            user32.ReleaseDC(desktop_window, device_context)
        except Exception as e:
            print(f"An exception occurred: {e}")
            raise e
