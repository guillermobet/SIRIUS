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
			print('There are no available options')
		
		return s
		
	def select_random_option(self, select_id):
		s = self.driver.find_element_by_id(select_id)
		self.scroll_to_item(s)
		select = Select(s)
		try:
			select.select_by_index(random.randint(1, len(select.options)-1))
		except:
			print('There are no available options')
		
		return s
		
	def fill_date_field(self, field_id, month, day, year):
		field = self.click_item(field_id)
		field.send_keys(month)
		field = self.click_item(field_id)
		field.send_keys(day)
		field = self.click_item(field_id)
		field.send_keys(year)
		
		return field
		
	def log_in(self):
		user = 'nek'
		pswd = '08042009a'
		self.click_item('login_btn')
		self.fill_text_field('id_user', user)
		f = self.fill_text_field('id_password', pswd)
		f.submit()
		
	def log_out(self):
		time.sleep(3)
		self.click_item('menu_logout')
		
	def register(self):
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
			
	def edit_profile(self):
		user = "juansitu"
		full_name = "Juan Situ"
		telephone = "1234567"
		email = "juananana@situ.com"
		password = "jejeje"
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
		
	def evaluate_site(self):
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
		
	def edit_review(self):
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
		self.wait_for_item('message_modal_close')
		time.sleep(2)
		self.click_item('message_modal_close')
		
	def create_meta_heuristic(self):
		heuristic_name = 'Heuristica Nueva'
		heuristic_acronym = 'HN'
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
		
	def edit_meta_heuristic(self):
		heuristic_name = 'Heuristica Nueva'
		heuristic_acronym = 'HN'
		# Edit heuristic
		self.wait_for_item('heuristic_table')
		time.sleep(3)
		row = self.driver.find_element_by_xpath('//td[text()="{}"]'.format(heuristic_name)).find_element_by_xpath('..')
		edit_link = row.find_element_by_xpath('./td/a[contains(@id, "edit_heuristic_")]')
		self.click_item(edit_link.get_attribute('id'))
		self.wait_for_item('id_name')
		time.sleep(2)
		self.fill_text_field('id_name', heuristic_name+" Modificada")
		time.sleep(0.3)
		field = self.fill_text_field('id_acronym', heuristic_acronym+"M")
		time.sleep(0.3)
		field.submit()
		self.wait_for_item('message_modal_close')
		time.sleep(1)
		self.click_item('message_modal_close')
		
	def delete_meta_heuristic(self):
		heuristic_name = 'Heuristica Nueva'
		heuristic_acronym = 'HN'
		# Delete heuristic
		self.wait_for_item('heuristic_table')
		time.sleep(3)
		row = self.driver.find_element_by_xpath('//td[text()="{}"]'.format(heuristic_name+" Modificada")).find_element_by_xpath('..')
		delete_link = row.find_element_by_xpath('./td/a[contains(@id, "delete_heuristic_")]')
		self.click_item(delete_link.get_attribute('id'))
		time.sleep(1)
		self.wait_for_item('message_modal_close')
		self.click_item('message_modal_close')
		
	def create_sub_heuristic(self):
		sub_heuristic_name = 'SubHeuristica Nueva'
		sub_heuristic_acronym = 'HN0'
		
		# Create new sub-heuristic
		#self.click_item('menu_settings')
		self.wait_for_item('menu_settings_subheu')
		self.click_item('menu_settings_subheu')
		self.wait_for_item('add_subheuristic_btn')
		time.sleep(1)
		self.click_item('add_subheuristic_btn')
		self.wait_for_item('id_heuristic')
		time.sleep(1)
		
		self.select_random_option('id_heuristic')
		time.sleep(0.5)
		self.fill_text_field('id_name', sub_heuristic_name)
		time.sleep(0.5)
		self.fill_text_field('id_acronym', sub_heuristic_acronym)
		time.sleep(0.5)
		self.select_random_option('id_atribute')
		time.sleep(0.5)
		
		input_groups = self.driver.find_elements_by_id('input-group')
		for i_group in input_groups:
			inputs = i_group.find_elements_by_tag_name('input')
			inp = inputs[random.randint(0, len(inputs)-1)]
			self.scroll_to_item(inp)
			time.sleep(0.3)
			inp.click()
			
		self.click_item('submit_meta_criteria_btn')
		self.wait_for_item('message_modal_close')
		time.sleep(1)
		self.click_item('message_modal_close')
		
	def edit_sub_heuristic(self):
		sub_heuristic_name = 'SubHeuristica Nueva'
		sub_heuristic_acronym = 'HN0'
		
		# Edit sub-heuristic
		self.wait_for_item('criteria_table')
		time.sleep(3)
		row = self.driver.find_element_by_xpath('//td[text()="{}"]'.format(sub_heuristic_name)).find_element_by_xpath('..')
		edit_link = row.find_element_by_xpath('./td/a[contains(@id, "edit_criteria_")]')
		self.click_item(edit_link.get_attribute('id'))
		self.wait_for_item('id_heuristic-edit')
		time.sleep(5)
		self.select_random_option('id_heuristic-edit')
		time.sleep(0.5)
		self.fill_text_field('id_name-edit', sub_heuristic_name+" Modificada")
		time.sleep(0.5)
		self.fill_text_field('id_acronym-edit', sub_heuristic_acronym+"M")
		time.sleep(0.5)
		self.select_random_option('id_atribute-edit')
		time.sleep(0.5)
		input_groups = self.driver.find_elements_by_id('input-group-edit')
		for i_group in input_groups:
			inputs = i_group.find_elements_by_tag_name('input')
			inp = inputs[random.randint(0, len(inputs)-1)]
			self.scroll_to_item(inp)
			time.sleep(0.3)
			inp.click()
			
		self.click_item('edit_meta_criteria_btn')
		self.wait_for_item('message_modal_close')
		time.sleep(1)
		self.click_item('message_modal_close')
		
	def delete_sub_heuristic(self):
		sub_heuristic_name = 'SubHeuristica Nueva'
		sub_heuristic_acronym = 'HN0'
		
		# Delete sub-heuristic
		self.wait_for_item('criteria_table')
		time.sleep(3)
		row = self.driver.find_element_by_xpath('//td[text()="{}"]'.format(sub_heuristic_name+" Modificada")).find_element_by_xpath('..')
		delete_link = row.find_element_by_xpath('./td/a[contains(@id, "delete_criteria_")]')
		self.click_item(delete_link.get_attribute('id'))
		time.sleep(1)
		self.wait_for_item('message_modal_close')
		self.click_item('message_modal_close')
		
	def create_website(self):
		website_name = "PAGINITA BELLA"
		website_url = "https://www.ldc.usb.ve/~12-11469"
		website_description = "Portal con el proposito de educar a las masas ignorantes de la USB, especialmente a los computistas"
		
		self.wait_for_item('menu_websites')
		self.click_item('menu_websites')
		
		# Create new website
		self.wait_for_item('id_website_name')
		self.fill_text_field('id_website_name', website_name)
		time.sleep(0.5)
		self.fill_text_field('id_website_url', website_url)
		time.sleep(0.5)
		self.select_random_option('id_website_type')
		time.sleep(0.5)
		field = self.fill_text_field('id_website_description', website_description)
		time.sleep(0.5)
		field.submit()
		
		time.sleep(1)
		self.wait_for_item('message_modal_close')
		self.click_item('message_modal_close')
		
	def edit_website(self):
		website_name = "PAGINITA BELLA"
		website_url = "https://www.ldc.usb.ve/~12-11469"
		website_description = "Portal con el proposito de educar a las masas ignorantes de la USB, especialmente a los computistas"
		
		self.wait_for_item('website_table')
		time.sleep(3)
		
		# Select website
		row = self.driver.find_element_by_xpath('//td[text()="{}"]'.format(website_name)).find_element_by_xpath('..')
		edit_link = row.find_element_by_xpath('./td/a[contains(@id, "edit_website_")]')
		self.click_item(edit_link.get_attribute('id'))
		
		# Edit website
		self.wait_for_item('id_website_name')
		self.fill_text_field('id_website_name', website_name+" Pero Mejor")
		time.sleep(0.5)
		self.fill_text_field('id_website_url', website_url+"_mejorado")
		time.sleep(0.5)
		self.select_random_option('id_website_type')
		time.sleep(0.5)
		field = self.fill_text_field('id_website_description', website_description+" y productistas")
		time.sleep(0.5)
		field.submit()
		
		time.sleep(1)
		self.wait_for_item('message_modal_close')
		self.click_item('message_modal_close')
		
	def show_and_generate_report(self):
		self.wait_for_item('menu_reports')
		self.click_item('menu_reports')
		
		self.wait_for_item('website_selector')
		while True:
			self.select_random_option('website_selector')
			time.sleep(0.6)
			rows = self.driver.find_elements_by_tag_name('tr')
			if(len(rows) > 0):
				break
		time.sleep(5)
		
		self.click_item('generate_pdf_btn')		
		
			
	
	def setUp(self):
		self.driver = Chrome()
		self.driver.maximize_window()
		self.actions = ActionChains(self.driver)
		self.driver.get("http://127.0.0.1:8000/")
		assert "SIRIUS" in self.driver.title
		
	def test_full_site_run(self):
		self.register()
		self.edit_profile()
		self.evaluate_site()
		self.edit_review()
		self.log_out()
		
		self.log_in()
		self.create_website()
		self.edit_website()
		self.create_meta_heuristic()
		self.edit_meta_heuristic()
		self.delete_meta_heuristic()
		self.create_sub_heuristic()
		self.edit_sub_heuristic()
		self.delete_sub_heuristic()
		self.show_and_generate_report()
		time.sleep(10)
		
	def tearDown(self):
		self.driver.close()

if __name__ == "__main__":
	unittest.main()
