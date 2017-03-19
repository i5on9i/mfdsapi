

from time import sleep
import re

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException

from browser_driver import SelDriver

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def genTree(content):
    parser = etree.HTMLParser()
    return etree.parse(StringIO(content), parser)

def waitElement(driver, xpath):
    while True:
        ret = driver.find_elements_by_xpath(xpath)
        if len(ret) != 0:
            return ret
        sleep(1)

class MfdsApi(object):
    def __init__(self):
        pass

class MfdsApiAddress(MfdsApi):

    host = "https://ezdrug.mfds.go.kr"
    
    def __init__(self, id=None, pw=None):
        
        self.id = id
        self.pw = pw

        # self.driver = SelDriver.firefox()
        self.driver = SelDriver.phantomJS()

        driver = self.driver
        
        # set window size
        # http://yizeng.me/2014/02/23/how-to-get-window-size-resize-or-maximize-window-using-selenium-webdriver/
        driver.set_window_size(480, 320)
        # driver.set_page_load_timeout(30)

        mainUrl = self.host
        driver.get(mainUrl)
        self._clickCompanyInfoMenu()


    def _clickCompanyInfoMenu(self):
        driver = self.driver
        
        waitElement(driver, "//div[@class='con-group1']//li/a")
        script = "var el = document.querySelector('div.con-group1 li>a');"\
                "el.click();"
        driver.execute_script(script)
        sleep(2)

    def _inputSearchKeyword(self, keyword):
        driver = self.driver

        # input
        inputXpath = '//input[contains(@id, "-entpName")]'
        inputKey = keyword
        inputEl = waitElement(driver, inputXpath)[0]
        print("> Search page has been loaded")

        # focus input and set value
        script = "var el = document.querySelector('input#{id}');"\
                "el.focus();"\
                "el.value='{value}';"\
                .format(id=inputEl.get_attribute('id'),
                        value=inputKey)
        driver.execute_script(script)

    def _clickSearchButton(self):

        # click search button
        btnXpath = '//div[@id="btn-search-01"]'
        btnEl = self.driver.find_elements_by_xpath(btnXpath)[0]
        btnEl.click()
        print('> Search Button is clicked')

    def _extractResult(self):
        driver = self.driver

        tbodyXpath = "//tbody[@class='v-grid-body']/tr"
        keys = ['kind', 'name', 'repr', 'regdate', 'address']
        rowsinfo = []

        trs = waitElement(driver, tbodyXpath)
        for tr in trs:
            tds = tr.find_elements_by_xpath("./td")
            info = {}
            for td, key in zip(tds, keys):
                info[key] = td.get_attribute('innerText')
            rowsinfo.append(info)
        
        return rowsinfo



    def search(self, keyword):
        """
            :return
                [{'address': '...', 'kind': '...', 'name' : '...',
                    'regdate': '...', 'repr': '...' },
                {'address': '...', 'kind': '...', 'name' : '...',
                    'regdate': '...', 'repr': '...' },
                ...]
        """
        self._inputSearchKeyword(keyword)
        self._clickSearchButton()

        # self._waitLoadingDone()
        sleep(2) # wait for response
        rowsinfo = self._extractResult()

        return rowsinfo

        


    def login(self):
        """
            This is not needed for now, 2017-03-19
        """
        if self.id is None or self.pw is None:
            eprint('id or pw is not set')
            return

        driver = self.driver

        # open the login page
        loginUrl = self.host + "/#!CCEAB01F010"
        # driver.set_page_load_timeout(5) # 5-seconds
        try :
            driver.get(loginUrl)
        except TimeoutException as e:
            print('stop loading : 5 seconds have been passed')
        
        loginBoxXpath = '//div[@id="civil-content"]//div[@class="login"]'
        waitElement(driver, loginBoxXpath)
        loginBoxEl = driver.find_elements_by_xpath(loginBoxXpath)[0]
        
        
        idEl = loginBoxEl.find_elements_by_xpath('.//div[@location="idField"]/input')[0]
        pwEl = loginBoxEl.find_elements_by_xpath('.//div[@location="pwField"]/input')[0]

        ActionChains(driver).move_to_element(idEl).click().perform()
        self._inputText(idEl, self.id)
        self._inputText(pwEl, self.pw)
        
        # do focus all inputs
        driver.execute_script(
            "var ii = document.querySelectorAll('input');"\
            "for(var i; i<ii.length; i++){ii[i].focus();}")
        
        btn = loginBoxEl.find_elements_by_xpath('.//div[@class="btn_login"]//div[@role="button"]')[0]
        btn.click()

        print("--> Login")

    def _inputText(self, el, value):
        el.clear()
        el.send_keys(value)


    def getAddress(self, name):
        self.host + "/#!CCBAA02F010"

    def _waitLoadingDone(self):
        """
            This is not working well
        """
        driver = self.driver
        
        while True:
            ind = driver.find_elements_by_xpath('//div[contains(@class, "v-loading-indicator")]')[0]
            rer = re.search(r'display\s*:\s*(.*?);', ind.get_attribute('style'), re.DOTALL)
            if rer.group(1) == 'none':
                break
            sleep(1)
        

def main():
    
    mfds = MfdsApiAddress()
    addressinfo = mfds.search('태평양')
    addressinfo = mfds.search('태평양')
    
    

if __name__ == '__main__':
    main()