import os
import unittest
from selenium import webdriver


class InterfacesTest(unittest.TestCase):
    HOST_URL = "172.0.0.1"

    def setUp(self):
        self.driver = webdriver.Chrome('./test/drivers/chromedriver')
    
    def test_login_expecting_sucess(self) -> None:
        self.driver.get(f"http://admin:admin@{self.HOST_URL}")

        # Search for logout button
        supposed_logout_button = self.driver.find_element_by_xpath("/html/body/header/nav/div/form")
        if supposed_logout_button is None:
            # If not found fail teste
            self.fail("Logout button was not found")

        # If found search for action
        logout_button_action = supposed_logout_button.get_attribute("action")
        # Assert if action is logout user
        assert logout_button_action is not None and logout_button_action == "./logout"
    
    def test_login_expecting_fail(self) -> None:
        self.driver.get(f"http://admin:admin@{self.HOST_URL}")

        # Search for logout button
        supposed_logout_button = self.driver.find_element_by_xpath("/html/body/header/nav/div/form")
        if supposed_logout_button is not None:
            # If not found fail teste
            self.fail("Logout button was found")

        # If found search for action
        logout_button_action = supposed_logout_button.get_attribute("action")
        # Assert if action is logout user
        assert logout_button_action != "./logout"
    
    def test_quiz_submit_expecting_correct_answer(self) -> None:
        self.driver.get(f"http://admin:admim@{self.HOST_URL}")
        
        with open("test_correct_answer.py", "w+") as quiz_file:
            pass
    

    
