import time

import undetected_chromedriver as uc

from config import SeleniumConfig
from ..abstract import AbstractLoader


class SeleniumLoader(AbstractLoader):
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
