import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#---- Function list
#---- 1. get_user_name(driver)
#---- 2. get_post_link(driver)
#---- 3. get_post_date(driver)
#---- 4. get_user_face(driver)
#---- 5. get_user_locs(driver)
#---- 6. get_post_tags(driver)
#---- 7. cut_user_name(driver)
#---- 8. remove_hashtag(target_list)

# saving user's name
def get_user_name(driver):
	try:
		target = driver.find_element_by_css_selector('.sqdOP.yWX7d._8A5w5.ZIAjV')
		name_result = target.get_attribute('href')
		return name_result
	except:
		return " "

# saving post's link
def get_post_link(driver):
	try:
		target = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a')
		link_result = target.get_attribute('href')
		return link_result 
	except:
		return " "

# saving post's uploaded date
def get_post_date(driver):
	try:
		target = driver.find_element_by_css_selector('time.FH9sR.Nzb55')
		date_result = target.get_attribute('datetime')
		return date_result 
	except:
		return " "

# saving user's face photo
def get_user_face(driver, user_prf):
	driver.execute_script('window.open("' + user_prf + '");')
	tabs = driver.window_handles
	
	driver.switch_to.window(tabs[1])
	time.sleep(6)

	try:
		driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
	except:
		print('there is no face photo: posting loading error')
		driver.close()
		driver.switch_to.window(tabs[0])
		return " "

	for i in range(20):
		try:
			time.sleep(5)
			try:
				target = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/div[1]/img')
			except:
				target = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/div[1]/img')

			target_txt = target.get_attribute('alt')

			if '사람' in target_txt:
				result_face = target.get_attribute('src')
				driver.close()
				driver.switch_to.window(tabs[0])
				return result_face

		except:
			print('there is no face photo: crawling error')
			driver.close()
			driver.switch_to.window(tabs[0])
			return " "

		try:
			WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a._65Bje.coreSpriteRightPaginationArrow')))
			driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()
		except:
			print('there is no face photo: there is no face photo posting')
			driver.close()
			driver.switch_to.window(tabs[0])
			return " "

#saving user's location
def get_user_locs(driver):
	try:
		target = driver.find_element_by_css_selector('a.O4GlU')
		locs_result = target.get_attribute('text')
		return locs_result
	except:
		return " "

# saving post's tag's in array
def get_post_tags(driver):
	try:
		target = driver.find_element_by_css_selector('.C7I1f.X7jCj')
		target_html = target.get_attribute('innerHTML')
		tagslist = re.findall('#[A-Za-z0-9가-힣]+', target_html)
		tags_result = remove_hashtag(tagslist)
		return tags_result
	except:
		return " "

# extract user's name from user's profile linke
def cut_user_name(name):
	return name[26:-1]

# removing hashtag in text
def remove_hashtag(target_list):
	removed_result  = []
	tags_temp = ''.join(target_list).replace("#", " ")
	tags_temps = tags_temp.split(" ")
	for tag in tags_temps:
		removed_result.append(tag)
	return removed_result

