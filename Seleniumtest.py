from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


web = webdriver.Chrome()
web.get('https://form.jotform.com/202575177230149')
TeamNameBoxID = 14
GameRoundBoxID = 17
GameQuestionBoxID = 18
FirstHalfPointBoxID = 16
SecondHalfPointBoxID = 19
AnswerBoxID = 6
SubmitButtonID = 7
HalftimeAndFinalAnswerBoxID = [20, 21, 22, 23]
FinalQuestionWagerID = 24
Rounds = [1,2,3,'halftime',4,5,6,'final','tiebreaker']
Questions = [3,3,3,1,3,3,3,1,1]
Answers  =  [1,1,1,4,1,1,1,4,1]
BasePoints = [6,6,6,0,9,9,9,20,0]


sleep(1)
teamname = 'Alice'
team = web.find_element_by_xpath('//*[@id="input_14"]')
team.send_keys(teamname)

sleep(1)
round = '1'
roundbox = Select(web.find_element_by_id('input_17'))
roundbox.select_by_value(round)

sleep(1)
questionnumber = '3'
questionnumberbox = Select(web.find_element_by_id('input_18'))
questionnumberbox.select_by_value(questionnumber)

sleep(1)
pointvalue = '6'
pointvaluebox = Select(web.find_element_by_id('input_16'))
pointvaluebox.select_by_value(pointvalue)

sleep(1)
answer = 'Wonderland'
answerbox = web.find_element_by_xpath('//*[@id="input_6"]')
answerbox.send_keys(answer)
