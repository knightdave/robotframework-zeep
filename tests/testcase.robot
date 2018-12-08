*** Settings ***
Library  Collections
Library  String
Library  ../src/ZeepLibrary/ZeepKeywords.py

*** Test Cases ***

*** Test Cases ***
Basic functionality
    Create Soap Client    http://www.dneonline.com/calculator.asmx?wsdl
    ${sum}               Call Soap Method    Add   ${4}    ${5}
    Should Be Equal As Numbers    ${sum}    9