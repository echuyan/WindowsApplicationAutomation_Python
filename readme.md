# Introduction

Please provide a video showing off your solution along with the code.
Please add a README as well detailing any tools used, installation instructions and describe your solution as well.

# Recommended tools/frameworks

For this test we recommend using WinAppDriver and Appium as it is a free to use framework.
This is not a mandatory tools to use, any other framework you are familiar with that accomplishes the job is fine.
Python code is preferable but not mandatory!

# Installation Instructions (Windows)

### WinAppDriver
Download and install WinAppDriver from https://github.com/Microsoft/WinAppDriver/releases
We tried with WindowsApplicationDriver_1.2.1.msi so we recommend using the same version.
After installation you need to enable developer mode in order to run WinAppDriver.

### Appium

<details><summary>C# instructions</summary>

#### Install Node.js
https://nodejs.org/en/download

#### Install Appium
npm i -g appium@next

#### Install .NET Core
https://dotnet.microsoft.com/en-us/download

</details>

<details><summary>Python instructions</summary>

#### Install Appium-Python-Client
`python -m pip install Appium-Python-Client==1.3.0`
</details>

# Element inspection
For element/UI inspection we used inspect.exe which is available from the Windows SDK.


# Objectives
We are providing you with an application developed in the JUCE framework. This is a simple desktop application that simulates
a level editor for a brick breaker game.

The objective is to implement a set of test cases.

When you open the editor you should be presented with a simple UI with a few buttons
* new level
* open level
* save
* clear

There is also a few labels for configuration of the level
* Title
* Next level
* Background

In the center you have a rendering of the actual level that is currently loaded. you will se a background (that can be
selected in the combo box), a set of bricks and a grid.

In the bottom right you will see one of each brick available for the game.


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









