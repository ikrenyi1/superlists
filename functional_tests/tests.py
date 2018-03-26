from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time
import unittest

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_text_in_element(self, elemen_id, text):
        WebDriverWait(self.browser, 10).until(
            expected_conditions.text_to_be_present_in_element(
                (By.ID, elemen_id), text)
        )

    def wait_for_row_in_list_table(self, row_text):
        #table = self.browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #self.assertIn(row_text, [row.text for row in rows])

        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if (time.time() - start_time) > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # check out homepage
        self.browser.get(self.live_server_url)

        # page title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1')
        self.assertIn('To-Do', header_text.text)

        # invite to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        # type "Buy peacock feathers"
        inputbox.send_keys('Buy peacock feathers')
        # hit enter, page updates
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)
        self.wait_for_text_in_element('id_list_table', 'Buy peacock feathers')

        # add second item to list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)

        # The page updates again and now shows both items on her list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

    #def test_multiple_users_can_start_lists_at_different_urls(self):
    #    self.browser.get(self.live_server_url)
    #    inputbox = self.browser.find_element_by_id('id_new_item')
    #    inputbox.send_keys('Buy peacock feathers')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
