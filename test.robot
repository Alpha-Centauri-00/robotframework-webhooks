*** Settings ***
Library    random



*** Test Cases ***
01 TC-Testing the robot-fw
    [Tags]    Pass    Smoke
    [Documentation]    this test case is always going to pass. printing a log
    Log    This is a log


02 TC-Testing the robot-fw
    [Tags]    Fail    Smoke
    [Documentation]    this test case is always going to Fail.
    Fail    This is a Fail Test case

    
03 TC-Testing the robot-fw
    [Tags]    N/A    Smoke
    [Documentation]    this test case could be Pass or Fail, status is going to be randomly
    ${num}    Evaluate    random.randint(1,2)
    
    IF  ${num} == ${1}
        Log    this Value is 1
    ELSE
        Fail    Num is not equal to 1
    END
       

04 TC-Testing the robot-fw
    [Tags]    Pass    Smoke    Skip
    [Documentation]    this test case could be Pass or Fail, status is going to be randomly
    Log    No run
