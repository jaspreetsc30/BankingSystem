# Banking System


This is a simple command line program for simulating a simple banking system that allows users to register and carry out simple banking activities
***
## Specifications

Attached below are the following features allowed, they can be accessed by writing the following commands in the command line interface

| Feature | Description | Command |
| --- | --- | --- |
Account creation | To open a new bank account | `create`
Money deposit | To deposit money | `deposit`
Money withdrawal | To withdraw money | `withdraw`
Money transfer | To transfer cash between two users. | `transfer` 
List bank account balance | To list the account for the particular user | `balance`
Display transaction statement | To generate transaction statement for the particular user | `statement`

## Usage

In order to utilize the above functions, the following structure should be followed:

```python controller.py [OPERATION] [ARGUMENTS]```

Below contains all the available command line arguments

```python controller.py create [ID] [NAME] [CURRENCY]``` creates an account which requires a valid format of HKID, name as well as the choice of currency. The HKID format is as follows, the first digit must be a letter, followed by 6 numerals , the last digit is alphanumerical.

```python controller.py deposit [ID] [CURRENCY] [AMOUNT]``` deposits AMOUNT of CURRENCY into an account with ID

```python controller.py withdraw [ID] [CURRENCY] [AMOUNT]``` withdraws AMOUNT of CURRENCY from an account with ID

```python controller.py transfer [senderID] [CURRENCY] [AMOUNT] [recipientID]``` transfers AMOUNT of CURRENCY into an recipientID from a senderID

```python controller.py balance [ID]``` Lists out balance of an account ID

```python controller.py transaction [ID]``` Generates a statement of an account ID

### Example

```
$ python controller.py create Y1234567 Jasper HKD
Congratulations Jasper of id Y1234567. Your account has been created.
$ python controller.py deposit Y1234567 HKD 100000       
100000.0 HKD has been deposited
$ python controller.py withdraw Y1234567 HKD 100
100.0 HKD has been withdrawn from your account
$ python controller.py create Y6666666 Amy HKD
Congratulations Amy of id Y6666666. Your account has been created.
$ python controller.py transfer Y1234567 HKD 100 Y6666666
100.0 HKD has been transferred from your account to id holder Y6666666
$ python controller.py balance Y1234567
Your balance is as follows:
HKD: 99798.0
$ python controller.py statement Y1234567
User Name:
Jasper
Date                 Currency   Operation                       Amount
2022-06-06 03:49:37  HKD        DEPOSIT                         100000.000000
2022-06-06 03:49:46  HKD        WITHDRAWAL                      -100.000000
2022-06-06 03:49:46  HKD        WITHDRAWAL FEE                  -1.000000
2022-06-06 03:50:13  HKD        TRANSFER to Y6666666            -100.000000
2022-06-06 03:50:13  HKD        TRANSFER FEE                    -1.000000
>
```

## Design

### DB vs File
Generally, there are two main ways to ensure that data is persistent between runs, either through a database or file. Databases are extremely advantageous as they can store millions of records while having a short query time, however this method exceeds the requirements of the project.A file is used as persist data  instead.

### File Type
There are many popular file formats such as XML, JSON, CSV. XML was dropped due to it being harder to program and debug in comparison to JSON and CSV. JSON was the easiest to program due to JSON library in Python which allows conversion of JSON to dictionaries.



## Programming Environment
The project was developed and tested on a Windows 10 machine (64 bit OS) using the Python programming language
