import sys
from time import sleep
from selenium import webdriver
from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


TeamNameBoxID = 'input_14'
GameRoundBoxID = 'input_17'
GameQuestionBoxID = 'input_18'
FirstHalfPointBoxID = 'input_16'
SecondHalfPointBoxID = 'input_19'
AnswerBoxID = 'input_6'
SubmitButtonID = 'input_7'
HalftimeAndFinalAnswerBoxIDs= [
    'input_20',
    'input_21', 
    'input_22', 
    'input_23',
]
FinalQuestionWagerID = 'input_24'
Rounds = ['1','2','3','halftime','4','5','6','final','tiebreaker']
Questions = [3,3,3,1,3,3,3,1,1]  # number of times an answer is required per round.
Answers  =  [1,1,1,4,1,1,1,4,1]  # number of strings of answers per round.
BasePoints = [
    ['2', '4', '6',],
    ['2', '4', '6',],   
    ['2', '4', '6',],    
    [],
    ['5', '7', '9',],
    ['5', '7', '9',],
    ['5', '7', '9',],
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
     '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',],  
    [],     
] 

sample_answers = {
    'first': {
        'Round': '1',
        'Question': '2',
        'Points': '6',
        'Answer': 'First round answer',
    },
    'halftime': {
        'Round': 'Halftime',
        'Answer': [
            'alpha', 
            'beta', 
            'delta', 
            'gamma',
        ],
        'Points': 'None. nothing is wagered'
    },
    'second': {
        'Round': '5',
        'Question': '2',
        'Points': '9',
        'Answer': 'second round answer',
    },
    'final': {
        'Round': 'Final',
        'Answer': [
            'alpha', 
            'beta', 
            'delta', 
            'gamma',
        ], 
        'Points': '20',        
    },
    'tiebreaker': {
        'Round': 'Tiebreaker',
        'Answer': 'The final decision (no points)'
    }
}

firsthalf_field_ids = {
    'Round': GameRoundBoxID,
    'Question': GameQuestionBoxID,
    'Points': FirstHalfPointBoxID,
    'Answer': AnswerBoxID,
}

seconhalf_field_ids = {
    'Round': GameRoundBoxID,
    'Question': GameQuestionBoxID,
    'Points': SecondHalfPointBoxID,
    'Answer': AnswerBoxID,
}

halftime_field_ids = {
    'Round': GameRoundBoxID,
    'Answer': HalftimeAndFinalAnswerBoxIDs,
}

final_field_ids = {
    'Round': GameRoundBoxID,
    'Answer': HalftimeAndFinalAnswerBoxIDs,
    'Points': FinalQuestionWagerID,  # TODO edge case. this field is an input box. the other rounds this is a dropdown.
}

tiebreaker_field_ids = {
    'Round': GameRoundBoxID,
    'Answer': AnswerBoxID,
}

@logger.catch
def main():

    def Fill_a_field(value, field_id):
        sleep(.1)
        team = web.find_element_by_id(field_id)
        team.send_keys(value)
        return

    def Fill_a_dropdown(value, field_id):
        sleep(.1)
        roundbox = Select(web.find_element_by_id(field_id))
        roundbox.select_by_value(value)
        return

    Fill_field = {
        'Round': Fill_a_dropdown,
        'Question': Fill_a_dropdown,
        'Points': Fill_a_dropdown,
        'Answer': Fill_a_field,    
    }

    for k,v in sample_answers.items():
        web = webdriver.Chrome()
        web.get('https://form.jotform.com/202575177230149')        
        Fill_a_field(f'Key: {k}', TeamNameBoxID)
        if k == 'first':
            for k1, v1 in v.items():
                Fill_field[k1](v1, firsthalf_field_ids[k1])
        if k == 'second':
            for k1, v1 in v.items():
                Fill_field[k1](v1, seconhalf_field_ids[k1])
        if k == 'halftime':
            for k1, v1 in v.items():
                if k1 == 'Question': 
                    pass  # there is no question number field here
                elif k1 == 'Points':
                    pass  # truly do nothing there is no point wager.
                elif k1 == 'Answer':
                    pass  # must handle 4 answer boxes
                else:
                    Fill_field[k1](v1, halftime_field_ids[k1])            
        if k == 'final':
            for k1, v1 in v.items():
                if k1 == 'Question': 
                    pass  # there is no question number field here                
                elif k1 == 'Answer':
                    pass  # must handle 4 answer boxes
                elif k1 == 'Points':  # EDGE-CASE. This round uses input not dropdown.
                    Fill_a_field(v1, final_field_ids[k1])
                else:
                    Fill_field[k1](v1, final_field_ids[k1])   
        if k == 'tiebreaker':
            for k1, v1 in v.items():
                if k1 == 'Question': 
                    pass  # there is no question number field here
                elif k1 == 'Points':
                    pass  # truly do nothing there is no point wager.
                else:
                    Fill_field[k1](v1, tiebreaker_field_ids[k1])  
        
        sleep(5)
        web.close()
        sleep(1)
    sys.exit(0)


"""
Fill_a_field(f'Key: {k}', AnswerBoxID)



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

sleep(10)
web.close()
"""


main()
