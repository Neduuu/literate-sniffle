import os
import html5lib
import pandas as pd
from courses import *
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()
options = Options()
options.add_argument("--silent")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--mute-audio")
options.add_argument('--disable-gpu')
options.add_argument("--log-level=3")
options.add_argument("--disable-logging")
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')




driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

def returnd():
    '''finds the course selection dropdown menu'''
    driver.get('https://brightspace.carleton.ca/d2l/home')
    try:
        login(driver)
    except:
        pass
    driver.find_element(By.CLASS_NAME, 'd2l-navigation-s-course-menu').click()
    return driver

def login(driver):
    '''Brightspace login'''
    username = driver.find_element(By.ID,'userNameInput')
    username.send_keys(os.getenv('USERNAME'))
    password = driver.find_element(By.ID,'passwordInput')
    password.send_keys(os.getenv('PASSWORD'))
    password.send_keys(Keys.RETURN)
    driver.implicitly_wait(3)
    return driver

def openclasses(driver):
    classes = driver.find_elements(By.CLASS_NAME, 'd2l-link.d2l-datalist-item-actioncontrol')
    names = []
    for course in classes:
        name = course.text
        names.append(name)
    return names, classes
      
def opentabs(names, classes, driver):
    ids = []
    for name in classes:
        linkpart = name.get_attribute("href")
        link = linkpart.split("/")[-1]
        ids.append(link)
        pos = classes.index(name)
        coursename = str(names[pos])
        driver.execute_script('''window.open("https://brightspace.carleton.ca/d2l/home/{}","_blank");'''.format(link))
    return ids

def opengrades(driver, ids):
    for id in ids:
        pos = ids.index(id)
        driver.switch_to.window(driver.window_handles[pos])
        driver.get('https://brightspace.carleton.ca/d2l/lms/grades/my_grades/main.d2l?ou={}'.format(id))
    return driver

def add_grade(driver,ids):
    dfs_s = []
    for id in ids:
        try:
            pos =  ids.index(id)
            driver.switch_to.window(driver.window_handles[pos])
            dfs = pd.read_html(driver.page_source)
            dfs_s.append(dfs)
        except Exception as e:
            print(e)
            pass
    return dfs_s

def removeuseless(ids, driver):
    notneeded = ['94066','84574','94067']
    newids = []
    #remove old tabs
    count = 0
    while True:
        for i in range(0,len(driver.window_handles)):
            try:
                driver.switch_to.window(driver.window_handles[i])
                link = driver.current_url
                tabid = link.split('/')[-1]
                if tabid in notneeded:
                    driver.close()
                elif not(tabid in ids):
                    driver.close()
                else:
                    pass
            except:
                break
        count += 1
        if count > 1:
            break
    #get new ids
    for i in range(0,len(driver.window_handles)):
        driver.switch_to.window(driver.window_handles[i])
        link = driver.current_url
        tabid = link.split('/')[-1]
        newids.append(tabid)
    return newids
            
def course_grades(dfs):
    '''Getting '''
    g_table = []
    for k,df in enumerate(dfs):
        for table in df:
            tables =pd.DataFrame(table)
            g_table.append(tables)
            try:
                for i,col in enumerate(tables['Grade Item.1']):                  
                    g = tables.loc[i,'Grade'].split(' ')[0] #Grade of assignment without %
                    if k == 0: #Getting grades for comp
                        for j in range(20):
                            #Getting assignments initialed as A(j)
                            if f'A{j}' in col and len(col) == 2 and g!= '0':
                                comp.add_assessments('Assignments',float(g))                      
                                break
                            if f'T{j}' in col and len(col) == 2 and g!= '0' :
                                comp.add_assessments('Tutorials',float(g))
                            if f'PP{j}' in col and len(col) == 3 and g != '0':
                                comp.add_assessments('PP',float(g))
                            if f'SE A{j}' in col and g!= '0':
                                comp.add_assessments('SE',float(g))
                        if 'Test' in col and len(col) == 6 and g!= '0':
                            comp.add_assessments('Tests',float(g))
                            break
                    if k == 1: #Getting grades for linear programming
                        if 'Quiz' in col and len(col) > 8 and g != '0':
                            l_prog.add_assessments('Quizzes',float(g))
                        if 'Test' in col and len(col) > 8 and g!= '0':
                            l_prog.add_assessments('Tests',float(g))
                        if 'Problem Set' in col and g!= '0':
                            l_prog.add_assessments('PS',float(g))
                    if k == 2: #Getting grades for calculus
                        if 'Test' in col and g != '0':
                            calc.add_assessments('Tests',float(g))
                    if k == 3: #Getting grades for music
                        pass
                    if k == 4: #Getting grades for stats
                        if 'Test' in col and g != '0':
                            stat.add_assessments('Tests',float(g))
                        if 'Assignment' in col and len(col.split(' ')) == 2 and g != '0':
                            stat.add_assessments('Assignments',float(g))
            except:
                pass
    

def csv_file():
    grade_list = [stat,calc,l_prog,comp]
    frames = []
    beys = []
    for course in grade_list:
        df = pd.DataFrame(course.show())
        frames.append(df)
        beys.append(course.name)
    result = pd.concat(frames, keys = beys)
    result.to_csv('coursegrades.csv')

def course_info():
    '''Every information regarding the courses '''
    #-----------------Removing assessments not taken in given course---------------
    grade_list = [stat,calc,l_prog,comp]
    for courses in grade_list:
        courses.remove_assessments()
    #-----------------Inputting assessment weights --------------------------------
    stat.weighted_grade([['Assignments',0.05],['Tests',0.15]])
    comp.weighted_grade([['Assignments',0.07], ['Tests',0.1],['Tutorials',0.013],['PP',0.013],['SE',0.0008]])
    l_prog.weighted_grade([['PS',0.03],['Tests',0.05],['Quizzes',0.01]])
    calc.weighted_grade([['Tests',0.15]])
    #-----------------inputting number of assessments ------------------------------
    l_prog.no_assessments([11,20,6])
    comp.no_assessments([2,11,5,11,6])
    stat.no_assessments([2,4])
    calc.no_assessments([4])
    print('Number of assessments stored')
    #----------------Saving plots of assessments -------------------------------------
    stat.course_plots()
    calc.course_plots()
    l_prog.course_plots()
    comp.course_plots()
    print('plots saved to folder')
    #-----------------Saving the predicted grades for each assessment for each course--------------------------------
    for course in grade_list:
        for assessment in course.assessments:
            course.grade_predict(assessment)
        print(f'Prediction for {course.name} is done')
    #----------------
       
def equal_array():
    grade_list = [stat,calc,l_prog,comp]
    for course in grade_list:
        course.equal_lists()



def main():
    driver = returnd()
    names, classes = openclasses(driver)
    ids = opentabs(names, classes, driver)
    ids = removeuseless(ids, driver)
    print(ids)
    grades = opengrades(driver, ids)
    grade_tables = add_grade(grades,ids)
    course_grades(grade_tables)
    course_info()
    l_prog.course_plots('Tests')
    print('done')
    
    
main()
#if __name__ == '__main__':
 #   main()
    