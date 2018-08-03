from selenium import webdriver
import time
import json


def login():
    #driver = webdriver.Firefox(executable_path='Your Path')
    driver = webdriver.PhantomJS(executable_path='Your Path')
    driver.get('https://sh.lianjia.com/')

    loginBtn = driver.find_element_by_class_name('reg')
    time.sleep(1)
    loginBtn.click()

    tologinBtn = driver.find_element_by_class_name('tologin')
    time.sleep(1)
    tologinBtn.click()


    phoneNum = driver.find_element_by_class_name('topSpecial')
    passWord = driver.find_element_by_class_name('password')
    submitButton = driver.find_element_by_class_name('login-user-btn')


    username = input('Enter your username: ')
    psw = input('Enter your password: ')

    phoneNum.send_keys(username)
    passWord.send_keys(psw)
    time.sleep(2)
    submitButton.click()
    time.sleep(5)


    data = driver.get_cookies()
    with open('../lianjia_spider/cookie.json', 'w') as outputfile:
        json.dump(data, outputfile)
        driver.close()

