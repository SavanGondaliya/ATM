import sqlite3 as sql
import random,math
from datetime import datetime

conn = sql.connect('atm.db')

cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS TBL_ATM_DATA(
                        name text,
                        account_number number primary key,
                        mobile_number number,
                        pin number,
                        current_balance number,
                        last_transaction date
                ) ''')

cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS TBL_USER_TRANSACTION(
                    transaction_id INTEGER PRIMARY KEY,
                    name TEXT,
                    account_number INTEGER, 
                    transaction_date DATE,
                    transaction_type TEXT,
                    debited INTEGER,
                    credited INTEGER,
                    remain_amount INTEGER,
                    FOREIGN KEY(name) REFERENCES TBL_ATM_DATA(name),
                    FOREIGN KEY(account_number) REFERENCES TBL_ATM_DATA(account_number)
                ) ''')

def registration():    
    name = input("Enter Your Name (As per Bank Application) ::  ")
    mobile_number = int(input("Enter Your Mobile Number :: "))
    pin = int(input("Set Your ATM Pin :: "))
    confirm_pin = int(input("Confirm Your Pin ::"))
    account_number = (chr(math.ceil(random.uniform(64,68))) + str(math.ceil(random.uniform(1111111111111111,9999999999999999))))
    
    if(pin == confirm_pin):
        print("Registration Successfull.")
        current_balance = 0
        last_transaction_date = datetime.now().date()
        data = cursor.execute(''' INSERT INTO TBL_ATM_DATA (name, account_number, mobile_number, pin, current_balance, last_transaction)VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, account_number, mobile_number,pin, current_balance, last_transaction_date))
        conn.commit()
                
def check_balance(pin):

        validate(pin)
        balance = cursor.execute("select current_balance from TBL_ATM_DATA where pin = ?",(pin,))
        for balance in balance.fetchone():
            print("Your Current Balance is :: ",balance) 
        
                    
def reset_pin(current_pin):
    
    validate(current_pin) 
       
    user_pin = cursor.execute("select pin from TBL_ATM_DATA where pin = ?",(current_pin,))
    for pin in user_pin.fetchone():
        if(current_pin == pin):
            new_pin = int(input("Please Set Your new Pin :: "))
            cursor.execute("update TBL_ATM_DATA set pin = ? where pin = ? ",(new_pin,current_pin))
            print("Your New Pin Updated Successfully.")
            conn.commit()
            
def withdraw_money(pin):
    validate(pin),

    withdraw_amount = int(input("Please Enter Your Amount :: "))
    balance = cursor.execute("select current_balance from TBL_ATM_DATA where pin = ?",(pin,))

    for current_balance in balance.fetchone():

        current_balance -= withdraw_amount
        cursor.execute("update TBL_ATM_DATA set current_balance = ? where pin = ? ",(current_balance,pin,))
        conn.commit()

    print(withdraw_amount , " is Withdrawn in Your Account.")
    
    transaction_type = "withdraw"
    calculate_transaction(transaction_type,pin,withdraw_amount)

def deposite(pin):
    validate(pin)
    
    deposite_amount = int(input("Please Enter The Amount :: "))
    balance = cursor.execute("select current_balance from TBL_ATM_DATA where pin = ?",(pin,))

    for current_balance in balance.fetchone():

        current_balance +=int(deposite_amount)
        cursor.execute("update TBL_ATM_DATA set current_balance = ? where pin = ? ",(current_balance,pin,))
        conn.commit()

    print(deposite_amount , " is Deposited in Your Account.")

    transaction_type = "deposite"
    calculate_transaction(transaction_type,pin,deposite_amount)

def calculate_transaction(transaction,pin,amount):
    transaction_id = int(math.ceil(random.uniform(1111111111111111,9999999999999999)))
    transaction_date = datetime.now()
    user_data = cursor.execute("select name,account_number,current_balance from TBL_ATM_DATA where pin = ?",(pin,))
    for list in  user_data.fetchall():
        name,account_number,balanace = list
    print(transaction)    
    if(transaction == "withdraw"):
        credited = 0
        debited = amount
        cursor.execute(''' insert into TBL_USER_TRANSACTION(transaction_id,name,account_number,transaction_date,transaction_type,debited,credited) 
                       values(?,?,?,?,?,?,?) ''',(transaction_id,name,account_number,transaction,transaction_date,debited,credited,))
        conn.commit()
        print("inserted")
    elif(transaction == "deposite"):
        credited = amount
        debited = 0
        cursor.execute(''' insert into TBL_USER_TRANSACTION(transaction_id,name,account_number,transaction_date,transaction_type,debited,credited) 
                       values(?,?,?,?,?,?,?) ''',(transaction_id,name,account_number,transaction,transaction_date,debited,credited))
        conn.commit()
        print("inserted")

def show_transaction(pin):
    
    validate(pin)
    mobile_number = int(input("Enter Your Mobile Number :: "))

    confirm_pin = cursor.execute("select pin,account_number from TBL_ATM_DATA where mobile_number = ?",(mobile_number,))
    for data in confirm_pin.fetchall():
        confirm_pin,account_number = data
    if(confirm_pin == pin):
        user_info = cursor.execute("select * from TBL_USER_TRANSACTION where account_number = ?", (account_number,))
        user_info = user_info.fetchall()
        for i in user_info:
            print(i)

def validate(pin):
    user = cursor.execute("select name from TBL_ATM_DATA where pin = ?",(pin,))
    
    if(user == "NoneType"):    
        print("You are not Registered,Please Register Your Information.....")
        registration()
    else: 
        for user_pin in user.fetchone():
            user = user_pin    
        user_data = cursor.execute("select name from TBL_ATM_DATA")
        for users in user_data.fetchall():
            user_data = users
    
def main():

    print("\t\t\t\t\t\t  Welcome Swan&Crane ATM Services")
    
    print("\n1.Register \n2.Check Balanace \n3.Reset Pin \n4.Money Withdraw \n5.deposite \n6.Check Transaction \n7.exit")

    choice = int(input("Which Service You want to use :: "))

    if(choice == 1):
        registration()
    elif(choice == 2):
        pin = int(input("Enter Your Pin :: "))
        check_balance(pin)    
    elif(choice == 3):
        current_pin  = int(input("Enter Your current Pin :: "))
        reset_pin(current_pin)
    elif(choice == 4):
        pin = int(input("Enter Your Pin :: "))
        withdraw_money(pin)
    elif(choice == 5):
        pin = int(input("Enter Your Pin :: "))
        deposite(pin)
    elif(choice == 6):
        pin = int(input("Enter Your Pin :: "))
        show_transaction(pin)
    else:
        exit()

if __name__ == main() :
    main()