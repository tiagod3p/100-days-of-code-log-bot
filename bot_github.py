from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime

# Getting the first day of challenge and the actual day.
day_0 = datetime.strptime("DATE_YOU_STARTED", "%d/%m/%Y")
today = datetime.now()

# Getting the current day of challenge.
day_x = today - day_0

# Getting the current month, day, and year.
current_month = datetime.strftime(today, "%B")
current_day = datetime.strftime(today, "%d")
current_year = datetime.strftime(today, "%Y")


class BotGithub:
    def __init__(self, site, username, password, progress, thoughts):
        self.site = site
        self.username = username
        self.password = password
        self.progress = progress
        self.thoughts = thoughts

        self.driver_path = "./chromedriver"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("user-data-dir=Perfil")
        self.bot = webdriver.Chrome(self.driver_path, options=self.options)

    def acess_site(self):
        self.bot.get(self.site)

    def check_login(self):
        """Checks if the user is already logged in.

        Returns:
            True -- Logged in.
            False -- Don't logged.
        """
        try:
            profile_photo = self.bot.find_element_by_xpath(
                "/html/body/div[1]/header/div[7]/details/summary/img"
            )
            profile_photo.click()

            profile_link = self.bot.find_element_by_xpath(
                "/html/body/div[1]/header/div[7]/details/details-menu/div[1]/a/strong"
            )
            profile_link_html = profile_link.get_attribute("innerHTML")

            if self.username == profile_link_html:
                print("User already logged in.")
                profile_photo_exit = self.bot.find_element_by_css_selector(
                    "body > div.position-relative.js-header-wrapper > header > div.Header-item.position-relative.mr-0.d-none.d-lg-flex > details > summary"
                )
                profile_photo_exit.click()
                return True
            else:
                return False

        except Exception as e:
            print("Error in autentication:", e)

    def click_sign_in(self):
        try:
            btn_sign_in = self.bot.find_element_by_link_text("Sign in")
            btn_sign_in.click()
        except Exception as e:
            print("Error clicking in the Sign in button: ", e)

    def login(self):
        try:
            usr_field = self.bot.find_element_by_xpath('//*[@id="login_field"]')
            pass_field = self.bot.find_element_by_xpath('//*[@id="password"]')

            usr_field.send_keys(self.username)
            pass_field.send_keys(self.password)
        except Exception as e:
            print("Typing error:", e)

        try:
            button_login = self.bot.find_element_by_name("commit")
            button_login.click()
            print("User logged in.")
        except Exception as e2:
            print("Error clicking in Sign in button:", e2)

    def acess_repository(self):
        try:
            button_repository = self.bot.find_element_by_xpath(
                '//*[@id="repos-container"]/ul/li[2]/div/a/span[2]'
            )
            button_repository.click()
        except Exception as e:
            print("Error trying to acess repository.", e)

    def acess_log(self):
        try:
            btn_log_md = self.bot.find_element_by_xpath(
                '//*[@id="readme"]/div[2]/article/ul[1]/li[2]/a'
            )
            btn_log_md.click()
        except Exception as e:
            print("Error clicking in log.md", e)

    def acess_edit_file(self):
        try:
            btn_edit = self.bot.find_element_by_css_selector(
                "body > div.application-main > div > main > div.container-lg.clearfix.new-discussion-timeline.p-responsive > div > div.Box.mt-3.position-relative > div.Box-header.py-2.d-flex.flex-column.flex-shrink-0.flex-md-row.flex-md-items-center > div.d-flex.py-1.py-md-0.flex-auto.flex-order-1.flex-md-order-2.flex-sm-grow-0.flex-justify-between > div:nth-child(2) > form.inline-form.js-update-url-with-hash > button > svg"
            )
            btn_edit.click()
        except Exception as e:
            print("Error clicking in edit.", e)

    def add_daily_log(self):
        """
        Add the daily log.

        First got down the scrollbar,
        Then click the last but one row,
        Lastly write the progress and thoughts of the day automatically.
        """
        try:
            scrollbar = self.bot.find_element_by_xpath(
                '//*[@id="new_blob"]/div[5]/div[2]/div/div[1]'
            )
            scrollbar.send_keys(Keys.DOWN * 35)

            sleep(3)

            field = self.bot.find_element_by_xpath(
                '//*[@id="new_blob"]/div[5]/div[2]/div/div[5]/div[1]/div/div/div/div[5]/div[last()-1]/pre'
            )
            field.send_keys(
                f"### Day {day_x.days} {current_month} {current_day}, {current_year}",
                f"\n\n**Today's Progress**: {self.progress}",
                f"\n\n**Thoughts:**: {self.thoughts}",
            )
        except Exception as e:
            print("Error adding the daily log:", e)

    def commit_changes(self):
        try:
            btn_commit = self.bot.find_element_by_xpath('//*[@id="submit-file"]')
            btn_commit.click()
            print("Today's log added with sucessful.")
        except Exception as e:
            print("Error clicking commit_changes: ", e)

    def exit(self):
        self.bot.quit()
        print("Exit with sucessful!")


if __name__ == "__main__":

    progress = input("Today's progress: ")
    thoughts = input("Thoughts: ")

    bot = BotGithub(
        "https://github.com/", "YOUR_USER", "YOUR_PASSWORD", progress, thoughts
    )
    bot.acess_site()

    # Checking if the user isn't logged
    if bot.check_login() is False:
        bot.click_sign_in()
        bot.login()

    bot.acess_repository()
    bot.acess_log()
    bot.acess_edit_file()
    sleep(3)
    bot.add_daily_log()
    sleep(3)
    bot.commit_changes()

    sleep(50)
    bot.exit()
