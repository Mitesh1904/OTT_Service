from sqlalchemy import *
from sqlalchemy.sql import text
import os
from sqlalchemy.engine import *
from sqlalchemy import event

#Action,comedy,crime and mystery,horror,romance,thriller,other


#DATA_BASE class fro create new class
class DATA_BASE:

    #creating new database
    def __init__(self):
        self.engine = create_engine('sqlite:///OTT_Service_Database.db', echo = False)

     
    #create fun create all required tablse 
    def create(self):

        #Customber Table Create Query : 
        Query=text('''
        CREATE TABLE Customer(
        Email varchar2(40) NOT NULL UNIQUE, 
        Customer_ID varchar2(25) NOT NULL,
        Last_Name varchar2(50) NOT NULL, 
        First_Name varchar2(50) NOT NULL,
        CONSTRAINT Customer_primary_const PRIMARY KEY (Customer_ID))''')
        self.engine.connect().execute(Query)

        #Subscription Table Create Query : 
        Query=text('''
        CREATE TABLE Subscription(
        Subscription_ID varchar2(25) NOT NULL,
        Price INT NOT NULL,
        Subscription_Type varchar2(25) NOT NULL,
        CONSTRAINT Subscription_primary_const PRIMARY KEY (Subscription_ID))''')
        self.engine.connect().execute(Query)
        
        #Payment Table Create Query :
        Query=text('''
        CREATE TABLE Payment(
        Payment_ID varchar2(25) NOT NULL,
        Amount INT NOT NULL,
        Payment_Date date NOT NULL,
        Payment_type varchar2(35) NOT NULL,
        Customer_ID varchar2(25) NOT NULL,
        Subscription_ID varchar2(25) NOT NULL,
        CONSTRAINT Payment_primary_const PRIMARY KEY (Payment_ID),
        CONSTRAINT Payment_Customer_const FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) ON DELETE CASCADE,
        CONSTRAINT Payment_Subscription_const FOREIGN KEY (Subscription_ID) REFERENCES Subscription(Subscription_ID) ON DELETE CASCADE )''')
        self.engine.connect().execute(Query)

        #Shows_and_Movies Table Create Query :
        Query=text('''
        CREATE TABLE Shows_and_Movies(
        Description varchar2(500) NOT NULL,
        Rating INT NOT NULL Check(Rating<=10 and Rating>=0),
        Title varchar2(50) NOT NULL,
        Show_ID varchar2(40) NOT NULL,
        Genre varchar2(25) NOT NULL,
        CONSTRAINT Shows_primary_const PRIMARY KEY (Show_ID))''')
        self.engine.connect().execute(Query)
      
        #Subscribe Table Create Query :
        Query=text('''
        CREATE TABLE Subscribe(
        Subscription_Date date NOT NULL,
        Expire_Date date date NOT NULL,
        Customer_ID varchar2(25) NOT NULL,
        Subscription_ID varchar2(25) NOT NULL,
        CONSTRAINT Subscribe_primary_const PRIMARY KEY (Customer_ID, Subscription_ID,Subscription_Date),
        CONSTRAINT Subscribe_Customer_const FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) ON DELETE CASCADE,
        CONSTRAINT Subscribe_Subscription_const FOREIGN KEY (Subscription_ID) REFERENCES Subscription(Subscription_ID) ON DELETE CASCADE)''')
        self.engine.connect().execute(Query)

        #Include Table Create Query :
        Query=text('''
        CREATE TABLE Include(
        Subscription_ID varchar2(25) NOT NULL,
        Show_ID varchar2(25) NOT NULL,
        CONSTRAINT Include_primary_const PRIMARY KEY (Subscription_ID, Show_ID),
        CONSTRAINT Include_Subscription_const FOREIGN KEY (Subscription_ID) REFERENCES Subscription(Subscription_ID) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT Include_Show_const FOREIGN KEY (Show_ID) REFERENCES Shows_and_Movies(Show_ID) ON DELETE CASCADE ON UPDATE CASCADE)''')
        self.engine.connect().execute(Query)
        
        #Customer_Address Table Create Query :
        Query=text('''
        CREATE TABLE Customer_Address(
        Address varchar2(250) NOT NULL,
        Customer_ID varchar2(25) NOT NULL,
        CONSTRAINT Address_primary_const PRIMARY KEY (Address, Customer_ID),
        CONSTRAINT Address_Customer_const FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) ON DELETE CASCADE)''')
        self.engine.connect().execute(Query)
        
        #Customer_Phone_No Table Create Query :
        Query=text('''
        CREATE TABLE Customer_Phone_No(
        Phone_No INT NOT NULL,
        Customer_ID varchar2(25) NOT NULL,
        CONSTRAINT Phone_primary_const PRIMARY KEY (Phone_No, Customer_ID),
        CONSTRAINT Phone_Customer_const FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) ON DELETE CASCADE)''')
        self.engine.connect().execute(Query)
        
        #Login Table Create Query :
        Query=text('''
        CREATE TABLE User_Login_data(
        Email varchar2(40) NOT NULL,
        Password varchar2(40) NOT NULL,
        CONSTRAINT Customer_primary_const PRIMARY KEY (Email),
        CONSTRAINT Email_Customer_const FOREIGN KEY (Email) REFERENCES Customer(Email) ON UPDATE CASCADE ON DELETE CASCADE)''')
        self.engine.connect().execute(Query)

        #default values
        self.Subscription_id="SUBSCRIPTION_0"
        Query=text(f'insert into Subscription (Subscription_ID,Price,Subscription_Type) values ("{self.Subscription_id}","00","free Trial")')
        self.engine.connect().execute(Query)
        self.Show_ID="SHOW_0"
        Query=text(f'insert into Shows_and_Movies (Show_ID,Description,Rating,Title,Genre) values ("{self.Show_ID}","free_show","10","Free_Show","free")')
        self.engine.connect().execute(Query)
        Query=text(f'insert into Include (Subscription_ID,Show_ID) values ("{self.Subscription_id}","{self.Show_ID}")')
        self.engine.connect().execute(Query)
        
    #Display all realted data
    def display_all(self):

        #join all realted data of customer Query
        Query=text("select * from customer natural join customer_address natural join customer_phone_no")
        output_customer=self.engine.connect().execute(Query).fetchall()

        #join all subscription realted data of customer Query
        Query=text("select CUSTOMER_ID,FIRST_NAME,LAST_NAME,SUBSCRIPTION_DATE,EXPIRE_DATE, SUBSCRIPTION_ID from customer natural join subscribe")
        output_customer_subscribe=self.engine.connect().execute(Query).fetchall()
        
        #join all payment realted data of customer Query
        Query=text("select CUSTOMER_ID,FIRST_NAME,LAST_NAME,PAYMENT_ID,AMOUNT,Payment_Date,PAYMENT_TYPE,SUBSCRIPTION_ID from payment natural join customer")
        output_customer_payment=self.engine.connect().execute(Query).fetchall()
        
        #join all payment realted data of Sunscription Query
        Query=text("select SUBSCRIPTION_ID,SUBSCRIPTION_TYPE,PRICE,PAYMENT_ID,AMOUNT,Payment_Date,PAYMENT_TYPE,CUSTOMER_ID from payment natural join subscription")
        output_subcription_payment=self.engine.connect().execute(Query).fetchall()

        #Include data
        Include().display()

        #Subscription data 
        Subscription().display()

        #Shows and movies data 
        Shows_and_Movies().display()

        #All Subscription realted data of customer
        if(len(output_customer_subscribe)!=0):
            print("\n")
            print("Customer Subscription Data given below".center(180))
            print("\n\n\t\t   ----------------------------------------------------------------------------------------------------------------------------------")
            print("\t\t   |     Customer_ID     |     First_Name     |     Last_Name     |   Subscription_Date   |    Expire_Date    |   Subscription_ID   |")
            print("\t\t   ----------------------------------------------------------------------------------------------------------------------------------")
            for i in output_customer_subscribe:
                print("\t\t   |{}|{}|{}|{}|{}|{}|".format(str(i[0]).center(21),str(i[1]).center(20),str(i[2]).center(19),str(i[3]).center(23),str(i[4]).center(19),str(i[5]).center(21)))
            print("\t\t   ----------------------------------------------------------------------------------------------------------------------------------")
        
        #All realted data of customer
        if(len(output_customer)!=0):
            print("\n")
            print("Customer Data given below".center(180))
            print("\n\n\t\t-----------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("\t\t|     Customer_ID     |            Email            |     Last_Name     |     First_Name     |                Address                |      Phone_No      |")
            print("\t\t-----------------------------------------------------------------------------------------------------------------------------------------------------------")
            for i in output_customer:
                print("\t\t|{}|{}|{}|{}|{}|{}|".format(str(i[1]).center(21),str(i[0]).center(29),str(i[2]).center(19),str(i[3]).center(20),str(i[4]).center(39),str(i[5]).center(20)))
            print("\t\t-----------------------------------------------------------------------------------------------------------------------------------------------------------")

        #All Payment realted data of customer
        
        if(len(output_customer_payment)!=0):
            print("\n")
            print("Customer Payment Data given below".center(180))
            print("\n\n\t--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("\t|     Customer_ID     |     First_Name     |     Last_Name     |     Payment_ID     |     Amount     |   Payment_Date   |    Payment_Type    |   Subscription_ID   |")
            print("\t--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            for i in output_customer_payment:
                print("\t|{}|{}|{}|{}|{}|{}|{}|{}|".format(str(i[0]).center(21),str(i[1]).center(20),str(i[2]).center(19),str(i[3]).center(20),str(i[4]).center(16),str(i[5]).center(18),str(i[6]).center(20),str(i[7]).center(21)))
            print("\t--------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        
        #All Payment realted data of Subscription
        if(len(output_subcription_payment)!=0):
            print("\n")
            print("Subscription Payment Data given below".center(180))
            print("\n\n\t---------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print("\t|   Subscription_ID   |   Subscription_Type   |    Price    |     Payment_ID     |     Amount     |   Payment_Date   |    Payment_Type    |       Customer_ID       |")
            print("\t---------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            for i in output_subcription_payment:
                print("\t|{}|{}|{}|{}|{}|{}|{}|{}|".format(str(i[0]).center(21),str(i[1]).center(23),str(i[2]).center(13),str(i[3]).center(20),str(i[4]).center(16),str(i[5]).center(18),str(i[6]).center(20),str(i[7]).center(25)))
            print("\t---------------------------------------------------------------------------------------------------------------------------------------------------------------------")

#Subscription class for updation in subscription table
class Subscription():
    #cunstructor which create connection with database
    def __init__(self):
        self.engine = create_engine('sqlite:///OTT_Service_Database.db', echo = False)
    
    #add Function for insert new raws
    def add(self,Subscription,price):
        self.Subscription=Subscription
        self.price=price
        Query=text('select * from Subscription')
        output=self.engine.connect().execute(Query).fetchall()
        str1=output[len(output)-1][0]
        str2=str1[13:]
        self.Subscription_id="SUBSCRIPTION_"+str(int(str2)+1)
        #insert Query 
        Query=text(f'insert into Subscription (Subscription_ID,Price,Subscription_Type) values ("{self.Subscription_id}","{self.price}","{self.Subscription}")')
        self.engine.connect().execute(Query)
        print("\n")
        print("Data Added Successfully".center(180))
        
    #delete Function for delete any raw by Subscription_id
    def delete(self,Subscription_id):
        self.Subscription_id=Subscription_id
        #delete Query
        Query=text(f'Delete from Subscription where Subscription_ID="{self.Subscription_id}"')
        self.engine.connect().execute(Query)
        print("\n")
        print("Data Deleted Successfully".center(180))

    #updete Function for delete any raw by Subscription_id
    def update(self,Subscription_id,list1,list2):
        self.Subscription_id=Subscription_id
        for i in range(len(list1)):
            #update Query
            Query=text(f'Update Subscription set {list1[i]} = "{list2[i]}" where Subscription_ID="{self.Subscription_id}"')
            self.engine.connect().execute(Query)
        print("\n")
        print("Data updated Successfully".center(180))

    def display(self):
        #Subscription data
        Query=text('select * from Subscription')
        output=self.engine.connect().execute(Query).fetchall()
        if(len(output)!=0):
            print("\n")
            print("Subscription Table Data given below".center(180))
            print("\n\n\t\t\t\t\t   -----------------------------------------------------------------------------------------")
            print("\t\t\t\t\t   |        Subscription_ID        |        Price        |        Subscription_type        |")
            print("\t\t\t\t\t   -----------------------------------------------------------------------------------------")
            for i in output:
                print("\t\t\t\t\t   |{}|{}|{}|".format(str(i[0]).center(31),str(i[1]).center(21),str(i[2]).center(33)))
            print("\t\t\t\t\t   -----------------------------------------------------------------------------------------")

#Shows_and_Movies class for updation in Shows_and_Movies table
class Shows_and_Movies():
    #cunstructor which create connection with database
    def __init__(self):
        self.engine = create_engine('sqlite:///OTT_Service_Database.db', echo = False)

    #add Function for insert new raws
    def add(self,Description,Rating,Title,Genre):
        Query=text('select * from Shows_and_Movies')
        output=self.engine.connect().execute(Query).fetchall()
        str1=output[len(output)-1][3]
        str2=str1[5:]
        self.Show_ID="SHOW_"+str(int(str2)+1)
        #insert Query 
        Query=text(f'insert into Shows_and_Movies (Show_ID,Description,Rating,Title,Genre) values ("{self.Show_ID}","{Description}","{Rating}","{Title}","{Genre}")')
        self.engine.connect().execute(Query)
        print("\n")
        print("Data Added Successfully".center(180))
    
    #delete Function for delete any raw by Subscription_id
    def delete(self,Show_ID):
        self.Show_ID=Show_ID
        #delete Query
        Query=text(f'Delete from Shows_and_Movies where Show_ID="{self.Show_ID}"')
        self.engine.connect().execute(Query)
        print("\n")
        print("Data Deleted Successfully".center(180))

    #updete Function for delete any raw by Subscription_id
    def update(self,Show_ID,list1,list2):
        self.Show_ID=Show_ID
        for i in range(len(list1)):
            #update Query
            Query=text(f'Update Shows_and_Movies set {list1[i]} = "{list2[i]}" where Show_ID="{self.Show_ID}"')
            self.engine.connect().execute(Query)
        print("\n")
        print("Data Updated Successfully".center(180))

    def display(self):
        Query=text('select * from Shows_and_Movies')
        output=self.engine.connect().execute(Query).fetchall()
        if(len(output)!=0):
            #Show details if exist
            print("\n")
            print("Shows_and_Movies Table Data given below".center(180))
            print("\n\n\t\t\t------------------------------------------------------------------------------------------------------------------------",end="")
            print("\n\t\t\t|        Show_ID        |        Description        |        Rating        |        Title        |        Genre        |")
            print("\t\t\t------------------------------------------------------------------------------------------------------------------------")
            for i in output:
                print("\t\t\t|{}|{}|{}|{}|{}|".format(str(i[3]).center(23),str(i[0]).center(27),str(i[1]).center(22),str(i[2]).center(21),str(i[4]).center(21)))
            print("\t\t\t------------------------------------------------------------------------------------------------------------------------")


#Include class for updation in Include table
class Include():
    #cunstructor which create connection with database
    def __init__(self):
        self.engine = create_engine('sqlite:///OTT_Service_Database.db', echo = False)

    #add Function for insert new raws
    def add(self,Subscription_id,Show_id):
        self.Subscription_id=Subscription_id
        self.Show_id=Show_id
        #insert Query 
        Query=text(f'insert into Include (Subscription_ID,Show_ID) values ("{self.Subscription_id}","{self.Show_id}")')
        self.engine.connect().execute(Query)
        print("\n")
        print("Data Added Successfully".center(180))
    
    #delete Function for delete any raw
    def delete(self,sub,show):
        self.Subscription_id=sub
        self.Show_id=show
        Query=text(f'delete from Include where Subscription_ID="{self.Subscription_id}" and Show_ID="{self.Show_id}"')
        self.engine.connect().execute(Query)
        print("Data Deleted Successfully".center(180))

    #delete Function for delete any raw
    def update(self,Subscription_id,Show_id,list1,list2):
        self.Subscription_id=Subscription_id
        self.Show_id=Show_id
        #update Query   
        for i in range(len(list1)):
            #update Query
            Query=text(f'Update Include set {list1[i]} = "{list2[i]}" where Subscription_ID="{self.Subscription_id}" and Show_ID="{self.Show_id}"')
            self.engine.connect().execute(Query)
        print("\n")
        print("Data Updated Successfully".center(180))

    def display(self):
        Query=text('select * from Include')
        output=self.engine.connect().execute(Query).fetchall()
        if(len(output)!=0):
            #Show details if exist
            print("\n")
            print("Include Table Data given below".center(180))
            print("\n\n\t\t\t\t\t\t\t   ---------------------------------------------------------",end="")
            print("\n\t\t\t\t\t\t\t   |        Show_ID        |        Subscription_ID        |")
            print("\t\t\t\t\t\t\t   ---------------------------------------------------------")
            for i in output:
                print("\t\t\t\t\t\t\t   |{}|{}|".format(str(i[1]).center(23),str(i[0]).center(31)))
            print("\t\t\t\t\t\t\t   ---------------------------------------------------------")


def menu():
    for i in range(180):
            print("*",end='')
    Sub= Subscription()
    Show=Shows_and_Movies()
    In= Include()
    while (True):           #menubar
        print("\n")
        print("*****  Select the option and update the data in database  *****".center(180)) #option
        print("\n\t\t\t 1. Add data in tables ")
        print("\n\t\t\t 2. Update data in tables ")
        print("\n\t\t\t 3. Delete data in tables ")
        print("\n\t\t\t 4. Show all data of tables ")
        print("\n\t\t\t 5. Exit")
        i=int(input("\n\n\t\t\t Enter Your Option here : "))
        #for updation in tables tables names
        if(i<=3):
            print("\n")
            print("*****   Select the Table update the data in database   *****".center(180))
            print("\n\t\t\t 1. Subscription Table ")
            print("\n\t\t\t 2. Shows_and_Movies Table ")
            print("\n\t\t\t 3. Include ") 
            j=int(input("\n\n\t\t\t Enter Your Option here : "))
            if(j>3 or j<1):
                print("\n\t\t\t Invalid Input")
                continue
        engine = create_engine('sqlite:///OTT_Service_Database.db', echo = False)
        Query=text('select * from Shows_and_Movies')
        output_Shows=engine.connect().execute(Query).fetchall() #details of all tables store in output variable for some checking purpose (like subscription id exist ot not)
        Query=text('select * from Subscription')
        output_Subscription=engine.connect().execute(Query).fetchall()
        Query=text('select * from Include')
        output_include=engine.connect().execute(Query).fetchall()

        #for add opretion
        if(i==1):
            
            #for adding new data in Subscription
            if(j==1):
                Sub.display()
                if len(output_Subscription)>=1:
                    print("\n\t\t\t (Enter New Data which not exist in above) \n")
                typ=input("\n\t\t\t Enter Subscription_type : ")
                price=int(input("\n\t\t\t Enter Price : "))
                Sub.add(typ,price)  #call add function which add new raw

            #for adding new data in Show_and_Movies
            elif(j==2):
                Show.display()
                if len(output_Shows)>=1:
                    print("\n\t\t\t (Enter New Data which not exist in above) \n")
                des=input("\n\t\t\t Enter Description : ")
                while(True):
                    rate=float(input("\n\t\t\t Enter Rating (betweem 1 to 10) : "))
                    if(rate<=10 and rate>=1):
                        break
                    else:
                        print("\n\t\t\t Invalid input")
                title=input("\n\t\t\t Enter Title : ")
                Genre=input("\n\t\t\t Enter Genre : ")
                Show.add(des,rate,title,Genre)
            
            #for adding new data in Includes_table
            elif(j==3):
                if(len(output_Subscription)>=1 and len(output_Shows)>=1):
                    while(True):
                        Show.display()
                        show=input("\n\t\t\t Enter Show_ID from the above list : ")
                        for i in output_Shows:
                            if str(show).strip() == list(i)[3]:
                                break
                        else:
                            print("\n\t\t\t Invalid input enter from the list")
                            continue
                        break
                    while(True):
                        Sub.display()
                        subscription=input("\n\t\t\t Enter Subscription_ID from the above list : ")
                        for i in output_Subscription:
                            if str(subscription).strip() == list(i)[0]:
                                break
                        else:
                            print("\n\t\t\t Invalid input enter from the list")
                            continue
                        break
                    if (subscription,show) in output_include:
                        print("\n\t\t\t This data All ready exist in this table")
                    else:
                        In.add(subscription,show)
                else:
                    print("\n\t\t\t First Add data into Show_and_movies table and Subscription table")

        #for update opretion
        elif(i==2):

            #for update data in Subscription
            if(j==1):
                if(len(output_Subscription)==0):
                    print("\n\t\t\t This table have not any data".center(180))
                    continue
                Sub.display()
                id=input("\n\t\t\t Enter id which data do you want to update (enter from above list) : ")
                if(id=='SUBSCRIPTION_0'):
                    print("\n\t\t\t This Entry can not be update".center(180))
                    continue
                for i in output_Subscription:
                    if str(id).strip() == list(i)[0]:  #check Subscriptuion id which given by user is exist or not
                        l1=[]
                        l2=[]
                        for attribute in ['Subscription_Type','Price']:
                            while(True):    #for update Subscription type and Price
                                check=input(f"\n\t\t\t Do you want to update {attribute} : ('Y' or 'n') : ")
                                if(check[0]=='Y' or check[0]=='y'):
                                    l1.append(attribute)  #appending attributes for change
                                    l2.append(input("\n\t\t\t Enter New vale : "))  #appending new data for change
                                    break
                                elif((check[0]=='N' or check[0]=='n')):
                                    break
                                else:
                                    print("\n\t\t\t Invalid Inputs ")
                        if(len(l1)>=1): #if any new value is given for update than call class update function/Method
                            Sub.update(id,l1,l2)    #l1--> List of Attribute which would update #l2 --> List of new values 
                        break
                else:
                    print("\n\t\t\t Invalid input")
            
            #for update data in Show_and_Movies
            elif(j==2):
                if(len(output_Shows)==0):
                    print("\n\t\t\t This table have not any data".center(180))
                    continue
                Show.display()
                id=input("\n\t\t\t Enter id which data do you want to update (enter from above list) : ")
                for i in output_Shows:
                    if str(id).strip() == list(i)[3]:
                        l1=[]
                        l2=[]
                        for attribute in ['Description','Rating','Title','Genre']:
                            while(True):
                                check=input(f"\n\t\t\t Do you want to update {attribute} : ('Y' or 'n') : ")
                                if(check[0]=='Y' or check[0]=='y'):
                                    l1.append(attribute)  #appending attributes for 
                                    if(attribute=='Rating'):
                                        while(True):
                                            rate=float(input("\n\t\t\t Enter Rating (betweem 1 to 10) : "))
                                            if(rate<=10 and rate>=1):
                                                l2.append(rate)
                                                break
                                            else:
                                                print("\n\t\t\t Invalid input")
                                        break
                                    else:
                                        l2.append(input("\n\t\t\t Enter New vale : "))  #appending new data for change
                                        break
                                elif((check[0]=='N' or check[0]=='n')):
                                    break
                                else:
                                    print("\n\t\t\t Invalid Inputs ")
                    if(len(l1)>=1):
                        Show.update(id,l1,l2)
                    break
                else:
                    print("\n\t\t\t Invalid input")
            
            #for update data in Include Table
            elif(j==3):
                if(len(output_include)>=1):
                    In.display()
                    show=input("\n\t\t\t Enter Show_ID from the above list (Which raw do you want to update) : ")
                    for i in output_include:
                        if str(show).strip() == list(i)[1]:
                            break
                    else:
                        print("\n\t\t\t Invalid input")
                        continue
                    subscription=input("\n\t\t\t Enter Subscription_ID from the above list (Which raw do you want to update) : ")
                    for i in output_include:
                        if str(subscription).strip() == list(i)[0]:
                            break
                    else:
                        print("\n\t\t\t Invalid input")
                        continue
                    l1=[]
                    l2=[]
                    while(True):
                        check=input(f"\n\t\t\t Do you want to update Subscription_ID : ('Y' or 'n') : ")
                        if(check[0]=='Y' or check[0]=='y'):
                            l1.append('Subscription_ID')  #appending attributes for 
                            while(True):
                                Sub.display()
                                id=input("\n\t\t\t Enter Subscription_ID from the above list : ")
                                for i in output_Subscription:
                                    if str(id).strip() == list(i)[0]:
                                        l2.append(id)
                                        break
                                else:
                                    print("\n\t\t\t Invalid input enter from the list")
                                    continue
                                break
                            break
                        elif((check[0]=='N' or check[0]=='n')):
                            break
                        else:
                            print("\n\t\t\t Invalid Inputs ")
                    while(True):
                        check=input(f"\n\t\t\t Do you want to update Show_ID : ('Y' or 'n') : ")
                        if(check[0]=='Y' or check[0]=='y'):
                            l1.append('Show_ID')  #appending attributes for update
                            while(True):
                                Show.display()
                                id=input("\n\t\t\t Enter Show_ID from the above list : ")
                                for i in output_Shows:
                                    if str(id).strip() == list(i)[3]:
                                        l2.append(id)
                                        break
                                else:
                                    print("\n\t\t\t Invalid input enter from the list")
                                    continue
                                break
                            break
                        elif((check[0]=='N' or check[0]=='n')):
                            break
                        else:
                            print("\n\t\t\t Invalid Inputs ")
                    if(len(l1)>=1):
                        if(len(l1)==1):
                            if(l1[0]=='Subscription_ID'):
                                if (l2[0],show) in output_include:
                                    print("\n\t\t\t This data All ready exist in this table")
                                else:
                                    In.update(subscription,show,l1,l2)
                            elif(l1[0]=='Show_ID'):
                                if (subscription,l2[0]) in output_include:
                                    print("\n\t\t\t This data All ready exist in this table")
                                else:
                                    In.update(subscription,show,l1,l2)
                        else:
                            if (l2[0],l2[1]) in output_include:
                                print("\n\t\t\t This data All ready exist in this table")
                            else:
                                In.update(subscription,show,l1,l2)
                else:
                    print("\n\t\t\t This table have not any data".center(180))

        #for delete opretion
        elif(i==3):
            #for delete data in Subscription
            if(j==1):
                if(len(output_Subscription)>=1):
                    Sub.display()
                    id=input("\n\t\t\t Enter id which data do you want to delete (enter from above list) : ")
                    if(id=='SUBSCRIPTION_0'):
                        print("\n\t\t\t This Entry can not be delete".center(180))
                        continue
                    for i in output_Subscription:
                        if str(id).strip() == list(i)[0]:  #check Subscriptuion id which given by user is exist or not
                            Sub.delete(id)  #call delete function which delete any from existing data
                            break
                    else:
                        print("\n\t\t\t Invalid input")
                else:
                    print("\n\t\t\t This table have not any data".center(180))

            #for delete data in Shows_and_Movies    
            elif(j==2):
                if(len(output_Shows)>=1):
                    Show.display()
                    id=input("\n\t\t\t Enter id which data do you want to delete (enter from above list) : ")
                    for i in output_Shows:
                        if str(id).strip() == list(i)[3]:
                            Show.delete(id)
                            break
                    else:
                        print("\n\t\t\t Invalid input")
                else:
                    print("\n\t\t\t This table have not any data".center(180))
            
            #for delete data in Include
            elif(j==3):
                if(len(output_include)>=1):
                    In.display()
                    show=input("\n\t\t\t Enter Show_ID from the above list : ")
                    subscription=input("\n\t\t\t Enter Subscription_ID from the above list : ")
                    if (subscription,show) in output_include:
                        In.delete(subscription,show)
                    else:
                        print("\n\t\t\t Invalid input")         
                else:
                    print("\n\t\t\t This table have not any data".center(180))

        #for show all detials
        elif(i==4):
            DATA= DATA_BASE()   #Create referancr of database class the called that create table
            DATA.display_all()

        #exit 
        elif (i==5):
            if(len(output_Subscription)>=1):    #it is mendatory that each subscription must have one show so we check that every show have some shows or not
                for j in output_Subscription:
                    j=list(j)
                    for k in output_include:
                        if j[0] in list(k):
                            break
                    else:
                        break
                else:
                    break
                print(f"\n\t\t\t Please Add Some Show for {j[0]} than exit")
                continue
            break
        #for invalid inputs
        else:
            print("\n\t\t\t   Invalid Input ")


    
#if database does not exist than go in else part and create new database 
if os.path.isfile('OTT_Service_database.db'):
    menu()  #call menu
else:
    DATA= DATA_BASE()
    DATA.create()
    menu()
print("\n\n")
for i in range(180):
    print("*",end='')
