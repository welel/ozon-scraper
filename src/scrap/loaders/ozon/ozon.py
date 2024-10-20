from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from scrap.loaders.exc import LoaderError
from scrap.loaders.selenium_loader import SeleniumLoader


class OzonLoader(SeleniumLoader):
    """Base ozon loader."""

    def bypass_captcha(self) -> None:
        max_tries = 10
        while True:
            if max_tries == 0:
                raise LoaderError("Max captcha bypass tries exceeded")
            try:
                btn = self.driver.find_element(by=By.CLASS_NAME, value="rb")
                self.logger.warning(
                    "Captha - reload button found: %s",
                    btn.get_attribute("outerHTML"),
                )
                btn.click()
                self.logger.info(
                    "Browser log: %s", self.driver.get_log("browser")
                )
                self._wait()
                max_tries -= 1
            except NoSuchElementException:
                break

    def bypass_age_banner(self) -> None:
        try:
            birth_input = self.driver.find_element(By.TAG_NAME, "input")
            name = birth_input.get_attribute("name")
            if name != "birthdate":
                return
            self.logger.info("Age banner detected...")

            birth_input.send_keys("05051995")  # ddmmyyyy
            btn = self.driver.find_element(By.TAG_NAME, "button")
            btn.click()
            self._wait()
        except NoSuchElementException:
            pass

    def accept_cookie(self) -> None:
        try:
            accept_cookie_btn = self.driver.find_element(
                By.CLASS_NAME, "d6f_9"
            )
            ActionChains(self.driver).move_to_element(
                accept_cookie_btn
            ).perform()
            accept_cookie_btn.click()
        except NoSuchElementException:
            pass
