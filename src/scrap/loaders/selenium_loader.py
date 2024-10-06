import time

import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from scrap.config import SeleniumConfig

from .abstract import Loader


class SeleniumLoader(Loader):
    url: str
    wait_time: float = 1.0

    def __init__(self, url: str | None = None):
        super().__init__()
        self.url = url or self.url
        options = uc.ChromeOptions()
        options.add_argument(f"user-agent={SeleniumConfig.default_user_agent}")
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1440,900')
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = uc.Chrome(
            options=options,
            driver_executable_path=SeleniumConfig.chrome_driver_path,
        )
        self.driver.get(self.url)
        self._wait()

    def _wait(self, wait_time: float | None = None) -> None:
        """Wait for wait_time with debug log."""
        wait_time = wait_time or self.wait_time
        self.logger.debug("Waiting for %s sec", self.wait_time)
        time.sleep(self.wait_time)

    def _shutdown(self) -> None:
        self.logger.info("Shutdown selenium instance...")
        self.driver.quit()

    def _scroll_down_until_bottom(
            self,
            step_px: int = 1000,
            wait_time: float = 2.0,
            step_in_row: int = 1,
            max_step: int | None = None,
    ) -> bool:
        """Scrolls page with dynamically loading content to the very bottom.

        Args:
            step_px: Size of a step in px.
            wait_time: Pause on `wait_time` sec after `step_in_row` steps.
            step_in_row: Performs `step_in_row` steps without a pause.
            max_step: Stops after `max_step` performed steps.

        Retruns:
            True - stopped by the end of the page;
            False - stopped by max_step steps.
        """
        def get_last_element_y_coordinate() -> int:
            last_element_of_body = "//body/*[last()]"
            last_el = self.driver.find_element(By.XPATH, last_element_of_body)
            return last_el.location["y"]

        current_y = get_last_element_y_coordinate()
        while True:
            for _ in range(step_in_row):
                ActionChains(self.driver).scroll_by_amount(
                    0, step_px
                ).perform()
                max_step -= 1
                time.sleep(wait_time)

            new_y = get_last_element_y_coordinate()
            if current_y == new_y:
                break
            current_y = new_y

            if max_step <= 0:
                return False
        return True

    def _get_clipboard_text(self) -> str:
        self.driver.set_permissions("clipboard-read", "granted")
        return self.driver.execute_script(
            "const text = await navigator.clipboard.readText(); return text;"
        )
