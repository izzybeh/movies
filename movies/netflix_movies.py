from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import time
import netflix as n
from imdb import IMDb

chrome_options = Options()
chrome_options.add_argument('--headless')

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = s, options = chrome_options)

username = input('Enter username: ')
password = input('Enter password: ')

driver.get('https://www.netflix.com/login')
driver.find_element(By.CSS_SELECTOR, '#id_userLoginId').send_keys(username)
driver.find_element(By.CSS_SELECTOR, '#id_password').send_keys(password)
driver.find_element(By.CSS_SELECTOR, '.login-button').click()

# wait for page to load
print('logging in')
time.sleep(5)

# load profile
driver.find_element(By.CSS_SELECTOR, '.profile-link:first-of-type').click()
print('loading profile')
time.sleep(5)

# go to movies
driver.get('https://www.netflix.com/browse/genre/34399?so=az')
print('loading movies')
time.sleep(5)

def scroll_page():
    pre_scroll_height = driver.execute_script('return document.body.scrollHeight;')
    run_time, max_run_time = 0, 1

    while True:
        iteration_start = time.time()
        # Scroll webpage, the 100 allows for a more 'aggressive' scroll
        driver.execute_script('window.scrollTo(0, 100*document.body.scrollHeight);')

        post_scroll_height = driver.execute_script('return document.body.scrollHeight;')

        scrolled = post_scroll_height != pre_scroll_height
        timed_out = run_time >= max_run_time

        if scrolled:
            run_time = 0
            pre_scroll_height = post_scroll_height
        elif not scrolled and not timed_out:
            run_time += time.time() - iteration_start
        elif not scrolled and timed_out:
            break

scroll_page()


titles_elems = driver.find_elements(By.CSS_SELECTOR, '.ptrack-content > a > div.boxart-size-16x9.boxart-container.boxart-rounded > div')

titles = []
for title in titles_elems:
    titles.append(title.text)

print('Count:', len(titles))

# filter by z to a
driver.get('https://www.netflix.com/browse/genre/34399?so=za')
print('loading movies')
time.sleep(5)

scroll_page()

titles_elems_2 = driver.find_elements(By.CSS_SELECTOR, '.ptrack-content > a > div.boxart-size-16x9.boxart-container.boxart-rounded > div')

for title in titles_elems_2:
    titles.append(title.text)

print('Count:', len(titles))

netflix = n.Netflix()
# netflix.reset_database() # only need to call this one unless you want to drop your table everytime.

ia = IMDb()
# https://imdbpy.readthedocs.io/en/latest/usage/quickstart.html

def get_movie_id(name):
    try:
        movies = ia.search_movie(name)
        movie = movies[0]
        return movie.movieID
    except Exception as e:
        print(e)

def get_movie_details(id):
    try:
        movie = ia.get_movie(id, info=['main'])
        movie.infoset2keys

        certificates = movie.get('certificates')
        certificate = 'Unknown'
        if type(certificates) == list:
            for item in certificates:
                if 'United States' in item:
                    certificate = item.split(':')[1]
                    break

        movie_info = {
            'id': id,
            'title': movie.get('title'),
            'certificate': certificate,
            'score': movie.get('rating'),
            'genres': ','.join(movie.get('genres')),
            'runtime': movie.get('runtimes')[0],
            'cover': movie.get('cover url')
        }
        score = float(movie_info['score'])
        if score > 5:
            return movie_info
        else:
            return False
    except Exception as e:
        print(e)
count = 0
for title in titles:
    id = get_movie_id(title)
    movie_info = get_movie_details(id)
    count += 1
    print(f'{count} of {len(titles)}')

    if movie_info != False:
        netflix.add(movie_info)

