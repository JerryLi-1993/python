from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By


chrome_options = ChromeOptions()
# 设置为无头
# chrome_options.add_argument('--headless')
# 禁止加载图片
# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)
# 启动chrome
browser = Chrome(chrome_options=chrome_options)
browser.get('https://www.douyu.com/g_LOL')
# 等待js加载,以周排行数据加载为标志(定位class='WeekRankTitle-upDownBoxMiddleConRank'加载完成)
locator = (By.CLASS_NAME, 'DyListCover-hot')
WebDriverWait(browser, 30).until(ec.presence_of_element_located(locator))
# 输出
room_hot = browser.find_element_by_xpath("//span[@class='DyListCover-hot']").text
print(room_hot)
# 关闭chrome
browser.quit()
