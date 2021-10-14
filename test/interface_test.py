import os
import hashlib
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.adduser import addUser
class InterfacesTest(unittest.TestCase):
    HOST_URL = "127.0.0.1:8080"

    def setUp(self):
        os.system("./start.sh")
        serv = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=serv)
    
    def test_login_valid_credentials(self) -> None:
        self.driver.get(f"http://admin:admin@{self.HOST_URL}")

        # Search for logout button
        supposed_logout_button = self.driver.find_element(By.XPATH, "/html/body/header/nav/div/form")
        if supposed_logout_button is None:
            # If not found fail teste
            self.fail("Logout button was not found")

        # If found search for action
        logout_button_action = supposed_logout_button.get_attribute("action")
        # Assert if action is logout user
        assert logout_button_action is not None and logout_button_action[-6:] == "logout"
    
    def test_login_invalid_credentials(self) -> None:
        self.driver.get(f"http://x:x@{self.HOST_URL}")

        with self.assertRaises(NoSuchElementException):
            self.driver.find_element(By.XPATH, "/html/body/header/nav/div/form")


    def test_quiz_submit_correct_answer(self) -> None:
        self.driver.get(f"http://admin:admin@{self.HOST_URL}")
        
        submit_file_name = "test_correct_answer.py"
        with open(submit_file_name, "w+") as quiz_file:
            quiz_file.write('''def desafio1(number): return 0''')

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="resposta"]'))
        ).send_keys(f"{os.getcwd()}/{submit_file_name}")
        self.driver.find_element(By.XPATH, '//button[text()="Enviar"]').click()
        
        os.remove(submit_file_name)
        assert self.driver.find_elements(By.TAG_NAME, "td")[2].text == 'OK!'


    def test_quiz_submit_wrong_answer(self) -> None:
        self.driver.get(f"http://admin:admin@{self.HOST_URL}")
        
        submit_file_name = "test_wrong_answer.py"
        with open(submit_file_name, "w+") as quiz_file:
            quiz_file.write('''def desafio1(number): return 1''')

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="resposta"]'))
        ).send_keys(f"{os.getcwd()}/{submit_file_name}")
        self.driver.find_element(By.XPATH, '//button[text()="Enviar"]').click()
        
        os.remove(submit_file_name)
        assert self.driver.find_elements(By.TAG_NAME, "td")[2].text == 'Erro'
    
