from selenium import webdriver
import eel
import time
import re
import random
import os
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException

eel.init("web")


chrome = "F:\\Microsoft VS Code\\Progect\\chromedriver.exe"


Likeall = 0
Likehours = 0
Subscriptions_all = 0
Subscriptions_hours = 0
Unsubscriptions_all = 0
last_person= "NON"
username = ''
login =''



def reraid_statistic_like():

	file = open("Statistic.txt", 'r')
	value1 = next(file) 
	value2 = next(file) 
	value3 = next(file) 

	value1_int = int(value1) + 1
	file.close()

	file = open("Statistic.txt", 'w')
	file.write(str(value1_int))
	file.write('\n')
	file.write(value2)
	file.write(value3)
	file.close()


def reraid_statistic_subscriptions():
	
	file = open("Statistic.txt", 'r')
	value1 = next(file) 
	value2 = next(file)
	value3 = next(file)

	value2_int = int(value2) + 1
	file.close()

	file = open("Statistic.txt", 'w')
	file.write(value1)
	file.write(str(value2_int))
	file.write('\n')
	file.write(value3)
	file.close()






def Search_by_person(actions_per_day, person):

    t=open("persons_list.txt", 'w')
    t.close
    
    actions_per_house = actions_per_day/24

    browser.get(f'https://www.instagram.com/{person}/') 
    time.sleep(random.randrange(3,5))
    
    element = "//section/main/div/header/section/ul/li[2]/a"
    browser.find_element_by_xpath(element).click()
    time.sleep(random.randrange(3,5))

    global last_person
    pers= []
    persons = []
    num_scroll = 0
    temp=0
    nomber_of_persons = 0

    
    element = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")


    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %6,element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %4,element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %3,element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %2,element)
    time.sleep(0.8)
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" %1.4,element)
    time.sleep(0.8)

    # Поиск человека, на котором закончился прошлый круг
    if last_person != "NON":
        while temp==0 :
            num_scroll +=1
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",element)
            if num_scroll %10 == 0:
                persons = browser.find_elements_by_xpath("//html/body/div[5]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a[@title]")
                nomber_of_persons = 0
                for i in range(len(persons)):
                    nomber_of_persons +=1
                    if (str(persons[i].get_attribute('href'))) == last_person:
                        temp = 1
                        break
   
    #Собираем ссылки
    
    while len(persons) < actions_per_house*5+nomber_of_persons:
        browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",element)
        persons = browser.find_elements_by_xpath("//html/body/div[5]/div/div/div[2]/ul/div/li/div/div[1]/div[2]/div[1]/span/a[@title]")
    for i in range(nomber_of_persons, len(persons)):
        pers.append(str(persons[i].get_attribute('href')))



    t=open("persons_list.txt", 'w') # Файл неотфилтрованных пользователей
    for person in pers:
        t.write(person)
        t.write("\n")
    t.close



def send_direct_message(person,quantity, message, img_path=''):

    Search_by_person(quantity, person)

    t=open("persons_list.txt",'r')
    usernames =[]
    i =0
    for line in t:
        i+=1
        line = re.sub(r'https://www.instagram.com/', '',line)
        line = re.sub(r'/', '',line)
        usernames.append(line)
        if i>=quantity:
            break
    t.close

    time.sleep(random.randrange(2, 4))

    browser.get(f'https://www.instagram.com/{login}/')

    direct_message_button = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"

    print("Отправляем сообщение...")
    browser.find_element_by_xpath(direct_message_button).click()
    time.sleep(random.randrange(3, 4))

    # отключаем всплывающее окно
    
    browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]").click()
    time.sleep(random.randrange(2, 4))

    browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/button").click()
    time.sleep(random.randrange(2, 4))

    # отправка сообщения нескольким пользователям
    for user in usernames:
        # вводим получателя
        to_input = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input")
        print(user)
        to_input.send_keys(user)
        time.sleep(random.randrange(3, 4))

        # выбираем получателя из списка
        browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[2]").find_element_by_tag_name("button").click()
        time.sleep(random.randrange(2, 4))

        browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # отправка текстового сообщения
        if message:
            text_message_area = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            text_message_area.clear()
            text_message_area.send_keys(message)
            time.sleep(random.randrange(2, 4))
            browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button").click()
            #print(f"Сообщение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))
        

        # отправка изображения
        if img_path:
            send_img_input = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
            send_img_input.send_keys(img_path)
            print(f"Изображение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))

        browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button").click()



def Search_by_hashtag(actions_per_day, hashtag):

    t=open("persons_list.txt", 'w')
    t.close

    browser.get(f' https://www.instagram.com/explore/tags/{hashtag}/') 
    time.sleep(random.randrange(3,5))

    actions_per_house = actions_per_day/24
    persons = []

    time.sleep(2)
    while len(persons)<actions_per_house*3:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = browser.find_element_by_xpath("//section/main/article/div[2]")
        element_a = element.find_elements_by_tag_name('a')
        for item in element_a:  
            href = item.get_attribute('href')
            persons.append(href)

    print(len(persons)) 

    t=open("hashtag_list.txt", 'w') # Файл неотфилтрованных пользователей
    for person in persons:
        t.write(person)
        t.write("\n")
    t.close






def Filters(person, publicationsmin, publicationsmax, subscribersmin, subscribersmax):

    browser.get(person)
    status = 1
    #Проверка закрытый аккаунт или нет
    element="//section/main/div/div/article/div/div/h2"
    if xpath_existence(element) == 1:
        try:
            if browser.find_element_by_xpath(element).text == "This Account is Private" or "Это закрытый аккаунт":
                print("Приватный аккаунт")
                status = 0
        except StaleElementReferenceException:
            print("Ошибка, элемента не существует")
    
    #Проверка количества пуюликаций
    element="//section/main/div/header/section/ul/li[1]/span/span"
    if xpath_existence(element) == 0:
        print("Ошибка, колличество публикайий не найденно")
    else:
        value = browser.find_element_by_xpath(element).text
        value = re.sub(r'\s', '',value)
        value = re.sub(r'тыс.','',value)
        value = re.sub(r'млн.','',value)
        value = re.sub(r',','',value)

    if publicationsmin !=0: #Проверка минимума
        if (int(value) < publicationsmin):
            #print("Недостаточно публикаций")
            status=0

    if publicationsmax !=0: #проверка максимума
        if (int(value) > publicationsmax):
            #print("Слишком большое количество публикаций")
            status=0

    #Проверка количества подпсчиков
    element="//section/main/div/header/section/ul/li[2]/a/span"
    if xpath_existence(element) == 0:
        print("Ошибка, колличество подписчиков не найденно")
    else:
        value = browser.find_element_by_xpath(element).text
        value = re.sub(r'\s', '',value)
        value = re.sub(r'тыс.','',value)
        value = re.sub(r'млн.','',value)
        value = re.sub(r',','',value)
    if subscribersmin !=0: #Проверка минимума
        if (int(value) < subscribersmin):
            #print("Недостаточно подписчиков")
            status=0

    if subscribersmax !=0: #проверка максимума
        if (int(value) > subscribersmax):
            #print("Слишком большое количество подписчиков")
            status=0

    return status


def Subscription_by_person(person):

    global Subscriptions_all, Subscriptions_hours,last_person, login

    element= "//section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button"

    if xpath_existence(element) == 0:
        print("Ошибка, код ощибки: 1")
    else:
        value = browser.find_element_by_xpath(element).text
        if value == "Подписаться":
            browser.find_element_by_xpath("//section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button").click()
            time.sleep(4)

            t=open(login, 'a')
            t.writelines(person)
            t.close()

            reraid_statistic_subscriptions()
            Subscriptions_all+=1
            Subscriptions_hours+=1
            last_person = person


def Like_by_person(person):

    global Likeall,Likehours,last_person

    element= "//a[contains(@href, '/p')]"
    
    if xpath_existence(element) == 0:
        print("Ошибка, код ощибки: 1")
    else:
        posts = browser.find_elements_by_xpath(element)
        i=0
        for post in posts:
            posts[i] = post.get_attribute("href")
            i+=1

        for i in range(1):
            browser.get(posts[i])
            if xpath_existence("//section/main/div/div[1]/article/div[3]/section[1]/span[1]/button") == 0:
                print("Ошибка, нет кнопки лайка")
            else:
                browser.find_element_by_xpath("//section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                Likeall=Likeall+1
                Likehours = Likehours + 1
            
        last_person = person
        reraid_statistic_like()
        time.sleep(4)

def Unsubscribe_all():


	try:
	    file = open('log_out.txt', 'r')
	except IOError as e:
	    print("Нет файла")
	else:

	    start_time = time.time()
	    r=open(login, 'r')

	    actions_per_house = actions_per_day/12
	    i=0

	    for person in r:
	        if i < actions_per_house:
	            person = re.sub(r'\n','',person) 

	            print(person)
	            
	            browser.get(person)

	            time.sleep(2)
	            element= "//section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button"

	            if xpath_existence(element) == 0:
	                print("Ошибка, код ощибки: 1")
	            else:
	                value = browser.find_element_by_xpath(element).text

	                if value == "Отписаться":
	                    #browser.find_element_by_xpath("//section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button").click()
	                    i+=1
	                    time.sleep(15)
	        else:
	            print("Отписались от ", i," человек, ждём",60*60 - (time.time() - start_time))
	            time.sleep(60*60 - (time.time()-start_time))

	    w=open(login, 'w')
	    w.close()       

	    r.close()





def smart_unsubscribe(username):

    #self = browser

    browser.get(f"https://www.instagram.com/{username}/")
    time.sleep(random.randrange(3, 6))
    followers_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
    followers_count = followers_button.get_attribute("title")

    following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
    following_count = following_button.find_element_by_tag_name("span").text


    time.sleep(random.randrange(3, 6))

    # если количество подписчиков больше 999, убираем из числа запятые
    if ',' in followers_count or following_count:
        followers_count, following_count = int(''.join(followers_count.split(','))), int(''.join(following_count.split(',')))
    else:
        followers_count, following_count = int(followers_count), int(following_count)

    print(f"Количество подписчиков: {followers_count}")
    followers_loops_count = int(followers_count / 12) + 1
    print(f"Число итераций для сбора подписчиков: {followers_loops_count}")

    print(f"Количество подписок: {following_count}")
    following_loops_count = int(following_count / 12) + 1
    print(f"Число итераций для сбора подписок: {following_loops_count}")

    # собираем список подписчиков
    followers_button.click()
    time.sleep(6)

    followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

    try:
        followers_urls = []
        print("Запускаем сбор подписчиков...")
        for i in range(1, followers_loops_count + 1):
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
            time.sleep(random.randrange(2, 4))
            print(f"Итерация #{i}")

        all_urls_div = followers_ul.find_elements_by_tag_name("li")

        for url in all_urls_div:
            url = url.find_element_by_tag_name("a").get_attribute("href")
            followers_urls.append(url)

        # сохраняем всех подписчиков пользователя в файл
        with open(f"{username}_followers_list.txt", "a") as followers_file:
            for link in followers_urls:
                followers_file.write(link + "\n")
    except Exception as ex:
        print(ex)
        #self.close_browser()

    time.sleep(random.randrange(4, 6))
    browser.get(f"https://www.instagram.com/{username}/")
    time.sleep(random.randrange(3, 6))

    # собираем список подписок
    following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
    following_button.click()
    time.sleep(random.randrange(3, 5))

    following_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")

    try:
        following_urls = []
        print("Запускаем сбор подписок")

        for i in range(1, following_loops_count + 1):
            browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
            time.sleep(random.randrange(2, 4))
            print(f"Итерация #{i}")

        all_urls_div = following_ul.find_elements_by_tag_name("li")

        for url in all_urls_div:
            url = url.find_element_by_tag_name("a").get_attribute("href")
            following_urls.append(url)

        # сохраняем всех подписок пользователя в файл
        with open(f"{username}_following_list.txt", "a") as following_file:
            for link in following_urls:
                following_file.write(link + "\n")

        """Сравниваем два списка, если пользователь есть в подписках, но его нет в подписчиках,
        заносим его в отдельный список"""

        count = 0
        unfollow_list = []
        for user in following_urls:
            if user not in followers_urls:
                count += 1
                unfollow_list.append(user)
        print(f"Нужно отписаться от {count} пользователей")

        # сохраняем всех от кого нужно отписаться в файл
        with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
            for user in unfollow_list:
                unfollow_file.write(user + "\n")

        print("Запускаем отписку...")
        time.sleep(2)

        # заходим к каждому пользователю на страницу и отписываемся
        with open(f"{username}_unfollow_list.txt") as unfollow_file:
            unfollow_users_list = unfollow_file.readlines()
            unfollow_users_list = [row.strip() for row in unfollow_users_list]

        try:
            count = len(unfollow_users_list)
            for user_url in unfollow_users_list:
                browser.get(user_url)
                time.sleep(random.randrange(4, 6))

                # кнопка отписки
                unfollow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
                unfollow_button.click()

                time.sleep(random.randrange(4, 6))
                # подтверждение отписки
                unfollow_button_confirm = browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]")
                unfollow_button_confirm.click()

                print(f"Отписались от {user_url}")
                count -= 1
                print(f"Осталось отписаться от: {count} пользователей")

                # time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(4, 6))

        except Exception as ex:
            print(ex)
            #self.close_browser()

    except Exception as ex:
        print(ex)
        #self.close_browser()

    time.sleep(random.randrange(4, 6))
    #self.close_browser()






def Authorization(login, password):
    browser.get("https://www.instagram.com/accounts/login")
    time.sleep(random.randrange(3,5))

    t=open("persons_list.txt", 'w')
    t.close

    login_use = browser.find_element_by_xpath("//section/main/div/div/div[1]/div/form/div/div[1]/div/label/input")
    login_use.send_keys(login)
    time.sleep(random.randrange(1,3))

    password_use = browser.find_element_by_xpath("//section/main/div/div/div[1]/div/form/div/div[2]/div/label/input")
    password_use.send_keys(password)
    time.sleep(random.randrange(1,3))

    click = browser.find_element_by_xpath("//section/main/div/div/div[1]/div/form/div/div[3]")
    click.click()
    time.sleep(random.randrange(1,3))


def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence



@eel.expose
def write_login(login_in, password):
	print("1212")
	t = open("log_out.txt", 'w')
	t.write(login_in)
	t.write("\n")
	t.write(password)
	t.close()
	on()
	

@eel.expose
def write_statistic(number):
	global Likeall,Subscriptions_all,Unsubscriptions_all
	file = open("Statistic.txt", 'r')
	value1 = next(file)
	Likeall = int(value1)
	value2 = next(file)
	Subscriptions_all = int (value2)
	value3 = next(file)
	Unsubscriptions_all = int (value3)
	file.close()
	if number == 1:
		return value1
	if number == 2:
		return value2
	if number == 3:
		return value3


	

@eel.expose
def on():
	global status,username,login

	print("Входим")

	try:
	    file = open('log_out.txt', 'r')
	except IOError as e:
	    eel.start("log.html",position=(600, 280), size=(800,500))
	else:
		login = next(file)
		username = login
		password = next(file)
		file.close()

		login = re.sub(r'\n','',login)

		Authorization(login, password)
		time.sleep(2)
		print("Проверка на вход")
		element = "//html/body/div[1]/section/main/div/div/div[1]/div/form/div[2]/p"
		if xpath_existence(element) == 1:
			if browser.find_element_by_xpath(element).text == "К сожалению, вы ввели неправильный пароль. Проверьте свой пароль еще раз." or browser.find_element_by_xpath(element).text == "Введенное вами имя пользователя не принадлежит аккаунту. Проверьте свое имя пользователя и повторите попытку.":
				print("Не тот пароль")
				os.remove('log_out.txt')
				on()
		else:
			print("Авторезировались")
			eel.start("main.html",position=(300, 100), size=(1280,800))


@eel.expose
def bot_by_person(subscribe_on, person, actions_per_day, minpublication, maxpublication, minsubscriptions, maxsubscriptions, minsubscribers, maxsubscribers):
    like_on = 1
    filter_on = 1
    subscribe_on = int(subscribe_on)
    actions_per_day = int(actions_per_day)
    minpublication = int(minpublication)
    maxpublication = int(maxpublication)
    minsubscriptions = int(minsubscriptions)
    maxsubscriptions = int(maxsubscriptions)
    minsubscribers = int(minsubscribers)
    maxsubscribers = int(maxsubscribers)

    while(1):

	    actions_per_house = actions_per_day/24
	   	

	    while (Likehours < actions_per_house or Subscriptions_hours < actions_per_house) and (like_on or subscribe_on) :

	        Search_by_person(actions_per_day, person)

	        t=open("persons_list.txt",'r')
	        file_list =[]

	        for line in t:
	            file_list.append(line)
	        t.close
	    
	        for person in file_list:

	            if Likehours < actions_per_house or Subscriptions_hours < actions_per_house:

	                if like_on:
	                    if Likehours < actions_per_house:
	                        if filter_on:
	                            if Filters(person, minpublication, maxpublication, minsubscribers, maxsubscribers):
	                                Like_by_person(person)
	                        else:
	                            Like_by_person(person)
	                    
	                if subscribe_on:
	                    if Subscriptions_hours < actions_per_house:
	                        if filter_on:
	                            if Filters(person, minpublication, maxpublication, minsubscribers, maxsubscribers):
	                                Subscription_by_person(person)
	                        else:
	                            Subscription_by_person(person)

	                time.sleep(2)
	                print(Likeall)
	            else:
	                break


        

@eel.expose
def bot_by_hashtag(subscribe_on, hashtag, actions_per_day, minpublication, maxpublication, minsubscriptions, maxsubscriptions, minsubscribers, maxsubscribers):

    subscribe_on = int(subscribe_on)
    actions_per_day = int(actions_per_day)
    minpublication = int(minpublication)
    maxpublication = int(maxpublication)
    minsubscriptions = int(minsubscriptions)
    maxsubscriptions = int(maxsubscriptions)
    minsubscribers = int(minsubscribers)
    maxsubscribers = int(maxsubscribers)
    like_on = 1
    filter_on = 1

    actions_per_house = actions_per_day/24


    Search_by_hashtag(actions_per_day, hashtag)

    while (Likehours < actions_per_house or Subscriptions_hours < actions_per_house) and (like_on or subscribe_on):

        t=open("hashtag_list.txt",'r')
        file_list =[]

        for line in t:
            file_list.append(line)
        t.close

        for post in file_list:
            
            browser.get(post)
            time.sleep(2)
            
            element = "//section/main/div/div[1]/article/header/div[2]/div[1]/div[1]/span"

            if xpath_existence(element) == 0:
                print("Ошибка, код ощибки: 1")
            else:
                
                element_find = browser.find_element_by_xpath(element)
                time.sleep(2)
                
                element_a = element_find.find_elements_by_tag_name('a')
                for item in element_a:
                    href = item.get_attribute('href')
                    person = href

                print(href)
                time.sleep(2)

                if Likehours < actions_per_house or Subscriptions_hours < actions_per_house:

                    if like_on:
                        if Likehours < actions_per_house:
                            if filter_on:
                                if Filters(person, minpublication, maxpublication, minsubscribers, maxsubscribers):
                                    Like_by_person(person)
                            else:
                                Like_by_person(person)
                        
                    if subscribe_on:
                        if Subscriptions_hours < actions_per_house:
                            if filter_on:
                                if Filters(person, minpublication, maxpublication, minsubscribers, maxsubscribers):
                                    Subscription_by_person(person)
                            else:
                                Subscription_by_person(person)

                else:
                    break

        

@eel.expose
def eel_send_direct_message(person,quantity, message, image):
	print("Отправка сообщения")
	while(1):
		quantity = 30
		print(person, " ", message)
		send_direct_message(person,quantity, message,'')
		quantity_all = quantity_all + quantity
		print("Отправленно ", quantity_all, " сообщений")
		print("Ждём пол часа ")
		time.sleep(30*60)

@eel.expose
def eel_smart_unsubscribe():
	print("Отписка от пользователей")
	smart_unsubscribe(username)

@eel.expose
def ell_unsubscribe_all():
	print("Отписка от пользователей")
	Unsubscribe_all()

@eel.expose
def out():
	os.remove('log_out.txt')
	on() 


browser = webdriver.Chrome(chrome)
on() 
print("Вышли")
time.sleep(10)
