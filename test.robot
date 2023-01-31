*** Settings ***
Library    random



*** Test Cases ***
01 TC-Testing the robot-fw
    Log    This is a log


02 TC-Testing the robot-fw
    Fail    This is a Fail Test case

    
03 TC-Testing the robot-fw
    ${num}    Evaluate    random.randint(1,2)
    IF  ${num} == ${1}
        Log    this Value is 1
    ELSE
        Fail    Num is not equal to 1
    END
       

04 TC-Testing the robot-fw
    Log    Hello Mars
    
    
05 TC-Testing the robot-fw
    Should be equal    1    2
