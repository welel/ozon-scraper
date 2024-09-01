from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from ..exc import LoaderError
from ..selenium_loader import SeleniumLoader


class OzonLoader(SeleniumLoader):
    """Base ozon loader."""

    def bypass_captcha(self):
        max_tries = 10
        while True:
            if max_tries == 0:
                raise LoaderError("Max captcha bypass tries exceeded")
            try:
                btn = self.driver.find_element(by=By.CLASS_NAME, value="rb")
                self.logger.warning(
                    "Captha - reload button found: %s",
                    btn.get_attribute('outerHTML'),
                )
                btn.click()
                self.logger.info(
                    "Browser log: %s", self.driver.get_log('browser')
                )
                self._wait()
                max_tries -= 1
            except NoSuchElementException:
                break

    def bypass_age_banner(self):
        try:
            birth_input = self.driver.find_element(By.TAG_NAME, "input")
            name = birth_input.get_attribute("name")
            if name != "birthdate":
                return
            self.logger.info("Age banner detected...")

            birth_input.send_keys("05051995")  # ddmmyyyy
            btn = self.driver.find_element(By.CLASS_NAME, "c5ak_46")
            btn.click()
            self._wait()
        except NoSuchElementException:
            pass
