from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import NoAlertPresentException
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import unittest, time, re
import re
import json

from main import Fileparser

def getFingerprint(text):
    # due to the interrupted support of the Retina API, we used selenium on the retina demo to retreive the fingerprints
    # goes through the entire text and retreives response from the text
    try:
        time.sleep(2.5)
        driver.find_element_by_name("body").clear()
        driver.find_element_by_name("body").send_keys(corpus[j])
        driver.find_element_by_name("commit").click()
        time.sleep(0.5)
        response = driver.find_element_by_css_selector(".response_code > pre").text
        time.sleep(1.5)
        while (response != "200"):
            time.sleep(0.2)
            driver.find_element_by_name("commit").click()
            time.sleep(0.2)
            response = driver.find_element_by_css_selector(".response_code > pre").text
            if(response=="400"):
                driver.find_element_by_name("body").clear()
                driver.find_element_by_name("body").send_keys("no")

        fingerprint = driver.find_element_by_css_selector(".json:nth-child(1) > code").text
        txt = fingerprint+"|"
        return txt
    except (NoSuchElementException, StaleElementReferenceException):
        return "FAIL|"
        pass





driver = webdriver.Chrome(executable_path='C:/chromedriver/chromedriver.exe')
base_url = "http://api.cortical.io/Text.htm#!/text/"
driver.get(base_url + "/")
verificationErrors = []

sourcePath="C:\DiplomaProject\AlmarimiCorpus\Corpus"
goalPath="C:\DiplomaProject\AlmarimiFingerprints\Fingerprints"
# here, we can define which texts to extract
for i in range(0,40):
    sPath=sourcePath+str(i)+".txt"
    gPath= goalPath+str(i) + ".txt"
    corpus=Fileparser.get_corpus_from_file(sPath)


    driver.find_element_by_link_text("Expand Operations").click()
    time.sleep(2);
    textList=[]
    failedIndices=[]
    with open(gPath, 'w', encoding="utf-8", errors='ignore') as goalFile:
        goalFile.truncate(0)
        for j in range(len(corpus)-1):
            txt=getFingerprint(corpus[j]);
            if(txt=="FAIL|"):
                print("fail")
                failedIndices.append(j)
            textList.append(txt)

        print("fixing fails")
        while(len(failedIndices)!=0):
            newFails=[]
            for j in range(len(failedIndices)):
                idx = failedIndices[j]
                newFails.append(idx)
                txt = getFingerprint(corpus[idx]);
                if(txt!="FAIL|"):
                    newFails.remove(idx)
                    textList.pop(idx)
                    textList.insert(idx,txt)
                    print("fail removed")
            failedIndices=newFails


        for t in textList:
            goalFile.write(t)
driver.close();
