import random
import unittest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains, Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

class GoogleSearch(unittest.TestCase):
	
	def scroll_to_item(self, item):
		self.driver.execute_script('arguments[0].scrollIntoView(true);', item)
	
	def fill_text_field(self, elem_id, data, wait=0.4):
		try:
			field = self.driver.find_element_by_id(elem_id)
			self.scroll_to_item(field)
			field.clear()
			field.send_keys(data)
			time.sleep(wait)
			
			return field
		except NoSuchElementException:
			print('The item with id {} could not be found'.format(elem_id))
			exit()
			
	def click_item(self, item_id):
		try:
			item = self.driver.find_element_by_id(item_id)
			self.scroll_to_item(item)
			time.sleep(0.5)
			item.click()
			
			return item
		except NoSuchElementException:
			print('The item with id {} could not be found'.format(item_id))
			
	def wait_for_item(self, item_id, wait=10):
		item = WebDriverWait(self.driver, wait).until(EC.presence_of_element_located((By.ID, item_id)))
		
		return item
		
	def select_option(self, select_id, option_text):
		s = self.driver.find_element_by_id(select_id)
		self.scroll_to_item(s)
		select = Select(s)
		try:
			select.select_by_visible_text(option_text)
		except NoSuchElementException:
			print('<<{}>> is not in the option list'.format(option_text))
		
		return select
		
	def select_option_by_index(self, select_id, index):
		s = self.driver.find_element_by_id(select_id)
		self.scroll_to_item(s)
		select = Select(s)
		try:
			select.select_by_index(index)
		except:
			print('There are not available options')
		
		return select
		
	def fill_date_field(self, field_id, month, day, year):
		field = self.click_item(field_id)
		field.send_keys(month)
		field = self.click_item(field_id)
		field.send_keys(day)
		field = self.click_item(field_id)
		field.send_keys(year)
		
		return field
	
	def setUp(self):
		self.driver = Chrome()
		self.driver.maximize_window()
		self.actions = ActionChains(self.driver)
		self.driver.get("http://127.0.0.1:8000/")
		assert "SIRIUS" in self.driver.title
		
	def test_full_site_run(self):
		
		heuristic_name = 'Heuristica Nueva'
		heuristic_acronym = 'HN'
		"""
		user = "juansitu"
		full_name = "Juan Situ"
		telephone = "1234567"
		email = "juananana@situ.com"
		password = "jejeje"
		
		# Register a new user
		self.click_item('register_btn')
		self.wait_for_item('id_user')
		time.sleep(2)
		
		self.fill_text_field('id_user', user)
		self.fill_text_field('id_full_name', full_name)
		self.fill_text_field('id_telephone', telephone)
		self.fill_text_field('id_email', email)
		self.fill_text_field('id_password', password)
		field = self.fill_text_field('id_password_confirmation', password)
		time.sleep(0.5)
		field.submit()
		time.sleep(1.5)
		
		# If the user was already registered, log in
		if('register' in self.driver.current_url.split('/')):
			self.click_item('has_account')
			self.wait_for_item('id_user')
			self.fill_text_field('id_user', user)
			field = self.fill_text_field('id_password', password)
			time.sleep(0.5)
			field.submit()
			time.sleep(1.5)
			
		# Edit profile
		self.click_item('menu_profile')
		self.wait_for_item('id_full_name')
		time.sleep(2)
		
		self.fill_text_field('id_email', email)
		self.fill_text_field('id_telephone', telephone)
		self.fill_text_field('id_password', password)
		field = self.fill_text_field('id_password_confirmation', password)
		
		time.sleep(0.5)
		field.submit()
		time.sleep(2)
		self.click_item('message_modal_close')
		time.sleep(0.5)
		
		# Evaluate a site
		
		self.click_item('menu_evaluate')
		self.wait_for_item('id_evaluator')
		field = self.fill_date_field('id_date', '12', '27', '1994')
		self.select_option_by_index('id_website', 1)
		self.click_item('submit_evaluate_form')
		
		self.wait_for_item('tabber_buttons', wait = 30)
		select_item = self.driver.find_element_by_id('tabber_buttons')
		select = Select(select_item)
		for i in range(len(select.options)):
			self.scroll_to_item(select_item)
			self.select_option_by_index('tabber_buttons', i)
			input_groups = self.driver.find_elements_by_id('input_group')
			visible_groups = [inp_g for inp_g in input_groups if inp_g.is_displayed()]
			for i_group in visible_groups:
				inputs = i_group.find_elements_by_tag_name('input')
				inp = inputs[random.randint(0, len(inputs)-1)]
				self.scroll_to_item(inp)
				time.sleep(0.2)
				inp.click()
				
		self.click_item('submit_evaluate_items_form')
		time.sleep(5)
		self.click_item('message_modal_close')
		time.sleep(1)
		
		# See and edit a review
		self.wait_for_item('menu_reviews')
		self.click_item('menu_reviews')
		a = self.driver.find_element_by_id('reviews_table').find_elements_by_xpath("//a[contains(@id, 'edit_')]")
		a[0].click()
		time.sleep(3)
		
		# Click edit button
		self.wait_for_item('edit_review')
		self.click_item('edit_review')
		
		# Change values
		self.wait_for_item('tabber_buttons')
		
		select_item = self.driver.find_element_by_id('tabber_buttons')
		select = Select(select_item)
		for i in range(len(select.options)):
			self.scroll_to_item(select_item)
			self.select_option_by_index('tabber_buttons', i)
			input_groups = self.driver.find_elements_by_id('input_group')
			visible_groups = [inp_g for inp_g in input_groups if inp_g.is_displayed()]
			for i_group in visible_groups:
				inputs = i_group.find_elements_by_tag_name('input')
				inp = inputs[random.randint(0, len(inputs)-1)]
				self.scroll_to_item(inp)
				time.sleep(0.2)
				inp.click()
		
		time.sleep(2)
		self.click_item('edit_review_submit')
		time.sleep(3)
		"""
		user = 'nek'
		pswd = '08042009a'
		self.click_item('login_btn')
		self.fill_text_field('id_user', user)
		f = self.fill_text_field('id_password', pswd)
		f.submit()
		
		# Create new heuristic
		self.click_item('menu_settings')
		self.wait_for_item('menu_settings_heu')
		self.click_item('menu_settings_heu')
		self.wait_for_item('submit_heuristic_btn')
		self.fill_text_field('id_name', heuristic_name)
		time.sleep(0.5)
		field = self.fill_text_field('id_acronym', heuristic_acronym)
		time.sleep(0.5)
		field.submit()
		self.wait_for_item('message_modal_close')
		time.sleep(1)
		self.click_item('message_modal_close')
		
		# Edit heuristic
		self.wait_for_item('heuristic_table')
		time.sleep(3)
		rows = self.driver.find_elements_by_xpath('//tr[contains(@id, "heuristic_")]')
		edit_link = rows[-1].find_element_by_xpath('//a[contains(@id, "edit_heuristic_")]')
		self.click_item(edit_link.get_attribute('id'))
		self.wait_for_item('id_name')
		self.fill_text_field('id_name', heuristic_name+" Modificada")
		time.sleep(0.3)
		field = self.fill_text_field('id_acronym', heuristic_acronym+"M")
		time.sleep(0.3)
		field.submit()
		self.wait_for_item('message_modal_close')
		time.sleep(1)
		self.click_item('message_modal_close')
		
		# Delete heuristic
		self.wait_for_item('heuristic_table')
		time.sleep(3)
		rows = self.driver.find_elements_by_xpath('//tr[contains(@id, "heuristic_")]')
		delete_link = rows[-1].find_element_by_xpath('//a[contains(@id, "delete_heuristic_")]')
		self.click_item(delete_link.get_attribute('id'))
		time.sleep(1)
		self.wait_for_item('message_modal_close')
		self.click_item('message_modal_close')
		time.sleep(10)
		
	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
