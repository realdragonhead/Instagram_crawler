### Code write date : 2020.05.07
### Tested Chrome version         78.0.3904.97
### Tested chromedriver version   same with browser
### Tested OS					  Windows, Mac OS

import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import Request, urlopen
import time
import re
import pandas as pd
import csv
import ins


#*********************************** USAGE **************************************#
#--------------------------------------------------------------------------------#
#---- First of all set Chrome and chrome driver version same --------------------#
#---- Use "search" function in text editor to find 'quote' ----------------------#
#---- and then find 'instagram account' and set your instagram account ----------#
#---- Please set 'time sleeper' adequately to local computer network speed ------#
#---- 'instagram account' and 'time sleeper' is defined as 'quote' --------------#
#---- and put ins.py same directory with this code ------------------------------#
#--------------------------------------------------------------------------------#
#********************************************************************************#


### instagram account #### 
Instagram_id = ""	###### Essential
Instagram_pw = ""	###### Essential

###### type defined #######
tags_dataset = []
csv_text = []

##### Input string ####################
##### type keyword without spacing ####
keyword = ""

###### target URL ######
url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

###### web driver loading part #####
driver = wd.Chrome("/Users/dragonheadreal/Downloads/chromedriver")
driver.get(url)

#<<<<< time sleeper >>>>>#
print("###########################################################################")
print("#--v.0.01-----------------------------------------------------------------#")
print("#------------------------------ Instruction ------------------------------#")
print("#--- Hello, this is Instagram crawler, there is caution before run -------#")
print("#--- This program crawl location name, url, face, hashtag, uploaded date -#")
print("#--- Make sure 'target.csv' is empty, if you run this program again ------#")
print("#--- This program will add data to 'target.csv'. So should change --------#")
print("#--- previous 'target.csv' file's name, before Program running. ----------#")
print("#--- AND DON'T USE ILLEGAL WAY. ------------------------------------------#")
print("#-------------------------------------------------------------------------#")
print("#-----------------------------------------------------made by Dragonhead--#")
print("###########################################################################")
print(" ")
print(" ")
time.sleep(8)

##### popup remover ######
try:
	if(driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/div/button')!=None):
		driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div/div/button').click()	
except:
	print('There is no popup')

driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()

###### login screen detector ######
try:
	if(driver.find_element_by_name('username')!=None):
		ac = driver.find_element_by_name('username')
		ac.clear()
		###### Instagram ID insert ######
		ac.send_keys(Instagram_id)
		pw = driver.find_element_by_name('password')
		pw.clear()
		###### Instagram PW insert ######
		pw.send_keys(Instagram_pw)
	
		btn = driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div[2]/div/div/div[1]/div/form/div[4]/button")
		btn.click()
		#<<<<< time sleeper >>>>>#
		time.sleep(8)
		driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
	
except:
	print("---------------------------------------------------------------------------")
	print('-------------------- There is no login process ----------------------------')
	print("---------------------------------------------------------------------------")

###### login save screen handler #####
try:
	driver.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF').click()
	time.sleep(6)
	driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
except:
	print("---------------------------------------------------------------------------")
	print("---------------------------------------------------------------------------")
	print('-------------------- There is no login save process -----------------------')
	print("---------------------------------------------------------------------------")
	print("---------------------------------------------------------------------------")
	
for i in range(76086):
	## variable list
	## 1. pname : user's name
	## 2. purls : user's profile link
	## 3. plink : post's link
	## 4. pdate : every single post uploaded date
	## 5. ulink : user's face photo(detected from instagram)
	## 6. ulocs : user's posting location
	## 7. ptags : tags data set every single post

	#<<<<<< time sleeper >>>>>>#
	time.sleep(7)
	try:
		########### saving process #############
		#### 01. saving user's name ############
		csv_text = []
		csv_text.append(i)
		print("##################################", i, "######################################")
		print(" ")
		print("saving", i, "post's user name and user profile link...")
		purls = ins.get_user_name(driver)
		pname = ins.cut_user_name(purls)
		csv_text.append(pname)
		csv_text.append(purls)
		print("--------user's name :", pname)
		print("--------user's profile linke :", purls)
		print(" ")
	
		#### 02. saving post's link ############
		print("saving", i, "post's link...")
		plink = ins.get_post_link(driver)
		csv_text.append(plink)
		print("--------user's post link :", plink)
		print(" ")
	
		#### 03. saving post update date #######
		print("saving", i, "post's update date...")
		pdate = ins.get_post_date(driver)
		csv_text.append(pdate)
		print("--------post is uploaded date :", pdate)
		print(" ")
		
		#### 04. saving user's face photo link #
		print("saving", pname, "'s face photo...")
		ulink = ins.get_user_face(driver, purls)
		csv_text.append(ulink)
		print("--------user's face photo link :", ulink)

		#### 05. saving user's posting location #####
		print("saving", i, "post's location...")
		plocs = ins.get_user_locs(driver)
		csv_text.append(plocs)
		print("--------location :", plocs)
		print(" ")
 	
		#### 06. saving tags ###################
		print("saving", i, "post's face photo...")
		ptags = ins.get_post_tags(driver)
		csv_text.append(ptags)
		print("--------hashtag saving is done!")
		print(csv_text)
		print(" ")

		####### saving to csv all data#######
		f = open('test.csv', 'a', newline='')
		wr = csv.writer(f)
		wr.writerow(csv_text)
		f.close()

	except EOFError:
		###### saving exception handler ######
		print('please input saving exception handler code')
		
	try:
		######### skip next page #############
		WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a._65Bje.coreSpriteRightPaginationArrow')))
		driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
	except:
		f.close()
		driver.close() 
	#<<<<< time sleeper >>>>>#
	time.sleep(3)
driver.close()


