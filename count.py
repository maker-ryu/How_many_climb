import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


posts = []

def get_instagram_posts(username):
    # ChromeDriver의 경로를 지정합니다.
    chromedriver_path = '/Users/dev_kiku/Downloads/chromedriver'

    # Selenium 웹 드라이버를 설정합니다.
    service = Service(executable_path=r'/Users/dev_kiku/Downloads/chromedriver')
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # 브라우저 창을 열지 않고 실행합니다.
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome(chromedriver_path, options=options)
    driver = webdriver.Chrome(service=service, options=options)

    # 인스타그램 홈페이지를 엽니다.
    driver.get('https://www.instagram.com/')

    # 페이지 로딩을 위해 약간의 시간을 기다립니다.
    time.sleep(2)

    # 아이디와 비밀번호를 입력하고 로그인합니다.
    username_input = driver.find_element(By.XPATH, r'//*[@id="loginForm"]/div/div[1]/div/label/input')
    password_input = driver.find_element(By.XPATH, r'//*[@id="loginForm"]/div/div[2]/div/label/input')
    username_input.send_keys('id')
    password_input.send_keys('password')
    password_input.send_keys(Keys.RETURN)
    print('login success')

    # 페이지 로딩을 위해 약간의 시간을 기다립니다.
    time.sleep(3)

    # 프로필 페이지로 이동합니다.
    driver.get(f'https://www.instagram.com/{username}/')
    print('move to profile page')

    # 페이지 로딩을 위해 약간의 시간을 기다립니다.
    time.sleep(2)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/p/"]'))
    )
    element.click()

    # 게시물의 내용을 크롤링합니다.
    while True:
        # # 게시물의 <h1> 태그 내용을 크롤링합니다.
        # h1_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'PolarisIGCoreText'))
        # )
        # print(h1_element)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        h1_tags = soup.find_all('h1', class_='PolarisIGCoreText')
        posts = [tag.get_text() for tag in h1_tags]
        print(posts)
        # posts.append(h1_element)

        # 다음 게시물로 이동하기 위해 버튼을 클릭합니다.
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.coreSpriteRightPaginationArrow'))
        )
        next_button.click()

        # 더 이상 다음 게시물이 없으면 종료합니다.
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href*="/p/"]'))
            )
        except:
            break

    # time.sleep(10)

    # 스크롤을 맨 아래로 내려 모든 게시물을 로드합니다.
    # last_height = driver.execute_script("return document.body.scrollHeight")
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(2)
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    # elements = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, f".{'_aagw'}"))
    # )
    # for element in elements:
    #     element.click()

    #     post_text = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, '_aacl'))
    #     ).text
    #     print(post_text)

    # aagws = driver.find_element(By.XPATH, r'//*[@id="mount_0_0_9x"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[2]/article/div/div/div[11]/div[1]/a/div[1]/div[2]')
    # aagws.click()

    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # posts = soup.find_all('div', {'class': '_aagw'})
    # print(posts)

    # for aagw in aagws:
    #     aagw.click()
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')
    #     posts = soup.find_all('div', {'class': '_aacl'})
    #     print(posts)

    # # 페이지 소스를 BeautifulSoup로 파싱합니다.
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    

    # # 각 게시물의 텍스트를 추출합니다.
    # posts = soup.find_all('div', {'class': '_aagw'})
    # print(posts)
    # # for post in posts:
        
    
    # # post_texts = [post.text for post in posts]

    # 웹 드라이버를 종료합니다.
    driver.quit()

    return 

# 인스타그램 아이디를 입력하여 크롤링합니다.
instagram_id = 'sio_0k_wall'
get_instagram_posts(instagram_id)
print(posts)

# 결과를 출력합니다.
# for post in posts:
#     print(post)
