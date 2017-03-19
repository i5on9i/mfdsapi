# coding=utf-8
from __future__ import unicode_literals 

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# import sys

class SelDriver(object):
    @staticmethod
    def phantomJS():
        
        driver = webdriver.PhantomJS(executable_path='c:\\Program Files\\WebDrivers\\phantomjs.exe')
        
        # An implicit wait tells WebDriver to poll the DOM
        # for a certain amount of time when trying to find any 
        # element (or elements) not immediately available
        driver.implicitly_wait(10) # seconds


        return driver

    @staticmethod
    def firefox45():
        # sys.path.append("..\\drivers")
        firefoxPath = "c:\\Program Files\\Mozilla Firefox 45.0\\firefox.exe"
        # Web Driver
        binary = FirefoxBinary(firefoxPath)
        driver = webdriver.Firefox(firefox_binary=binary)

        return driver

    @staticmethod
    def firefox():
        # sys.path.append("..\\drivers")
        firefoxPath = "c:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
        # Web Driver
        binary = FirefoxBinary(firefoxPath)
        driver = webdriver.Firefox(firefox_binary=binary)



        return driver
