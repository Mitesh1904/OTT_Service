from flask import Flask,request,render_template
from flask.helpers import send_file
from sqlalchemy import *
from sqlalchemy.sql import text
from sqlalchemy.engine import *
from sqlalchemy import event
from datetime import *
import datetime
import re

#for on the foreign key constraints 
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Customer():
    def __init__(self):
        self.engine=create_engine('sqlite:///OTT_Service_Database.db', echo = False)
    
    def add(self,firstname,lastname,email,password,mobileno,address):
        self.id=''
        #Customer data
        Query=text('select * from Customer')
        output=self.engine.connect().execute(Query).fetchall()
        #creating subscription id automatically
        if len(output)==0:
            self.id="CUSTOMER_0"
        else:
            str1=output[len(output)-1][1]
            str2=str1[9:]
            self.id="CUSTOMER_"+str(int(str2)+1)
        #insert into Customer
        Query=text(f'insert into Customer (Email,Customer_ID,Last_Name,First_Name) values ("{email}","{self.id}","{lastname}","{firstname}")')
        self.engine.connect().execute(Query)
        #insert into User_login
        Query=text(f'insert into User_Login_data (Email,Password) values ("{email}","{password}")')
        self.engine.connect().execute(Query)
        for i in range(len(mobileno)):
            #insert into Customer Phone no
            Query=text(f'insert into Customer_Phone_No (Phone_No,Customer_ID) values ("{mobileno[i]}","{self.id}")')
            self.engine.connect().execute(Query)
        for i in range(len(address)):
            #insert into Customer Address
            Query=text(f'insert into Customer_Address (Address,Customer_ID) values ("{address[i]}","{self.id}")') 
            self.engine.connect().execute(Query)
        return(self.id)
    def update(self,id,list1,list2,mobileno,address):
        for i in range(len(list1)):
            #update Customer
            Query=text(f'Update Customer set {list1[i]} = "{list2[i]}" where Customer_ID="{id}"')
            self.engine.connect().execute(Query)
        #delete Customer_No
        Query=text(f'Delete from Customer_Phone_No where Customer_ID="{id}"')
        self.engine.connect().execute(Query)
        #delete Customer_Addrees
        Query=text(f'Delete from Customer_Address where Customer_ID="{id}"')
        self.engine.connect().execute(Query)
        for i in range(len(mobileno)):
            #update Customer_No
            Query=text(f'insert into Customer_Phone_No (Phone_No,Customer_ID) values ("{mobileno[i]}","{id}")')
            self.engine.connect().execute(Query)
        for i in range(len(address)):
            #update Customer_Address
            Query=text(f'insert into Customer_Address (Address,Customer_ID) values ("{address[i]}","{id}")') 
            self.engine.connect().execute(Query)

class Subscribe():
    def __init__(self):
        self.engine=create_engine('sqlite:///OTT_Service_Database.db', echo = False)
    
    def add(self,subscription_id,customer_id,method):
        self.payid=''
        #paymet data
        Query=text('select * from Payment')
        output=self.engine.connect().execute(Query).fetchall()
        #creating subscription id automatically
        if len(output)==0:
            self.payid="PAYMENTNO_0"
        else:
            str1=output[len(output)-1][0]
            str2=str1[10:]
            self.payid="PAYMENTNO_"+str(int(str2)+1)
        #Price for Subscription
        Query=text(f'select Price from Subscription where Subscription_ID="{subscription_id}"')
        output=self.engine.connect().execute(Query).fetchall()
        self.Amount=output[0][0]
        self.subscription_date=datetime.datetime.now().strftime('%d-%m-%Y')
        self.expire_date = datetime.datetime.now()+datetime.timedelta(days=-30)
        self.expire_date=self.expire_date.strftime('%d-%m-%Y')
        #insert into Payment
        Query=text(f'insert into Payment (Payment_ID,Amount,Payment_Date,Payment_type,Customer_ID,Subscription_ID) values ("{self.payid}","{self.Amount}","{self.subscription_date}","{method}","{customer_id}","{subscription_id}")')
        self.engine.connect().execute(Query)
        #insert into Subscribe
        Query=text(f'insert into Subscribe (Subscription_Date,Expire_Date,Customer_ID,Subscription_ID) values ("{self.subscription_date}","{self.expire_date}","{customer_id}","{subscription_id}")')
        self.engine.connect().execute(Query)

customber =Customer()
sub1= Subscribe()
app = Flask(__name__) 
engine=create_engine('sqlite:///OTT_Service_Database.db', echo = False)

@app.route('/')
def Main():
    return render_template('OTT_Service_Home_page.html',singed=0,customber_id=None)

@app.route('/show_and_movie/',methods=['GET','POST'])
def show_and_movie():
    if request.method=='POST':
        return render_template('OTT_Service_Shows_and_Movies_page.html')

@app.route('/About/',methods=['GET','POST'])
def About():
    if request.method=='POST':
        return render_template('OTT_Service_About_page.html')

@app.route('/sign_in/',methods=['GET','POST'])
def sing_in():
    if request.method=='POST':
        id=request.form['Customer_id']
        return render_template('OTT_Service_Login_page.html',error_sing=0,id=id)

@app.route('/search/',methods=['GET','POST'])
def search():
    if request.method=='POST':
        search1=request.form['search']
        check=False
        id=request.form['Customer_id']
        if(id=='None'):
            singed=0
        else:
            singed=1
        Query=text("select * from Shows_and_Movies natural join include natural join Subscription")
        output=engine.connect().execute(Query).fetchall()
        data=[]
        d=[]
        for i in output:
            l1=[str(item).lower() for item in i]
            if(search1.lower() in l1):
                data.append(list(i))
                d.append(list(i)[5])
                check=True
        if(check):
            return render_template('OTT_Service_Search_Result.html',singed=singed,customber_id=id,values=data,d=d)
        else:
            return render_template('OTT_Service_Search_Result.html',singed=singed,customber_id=id,values="None",d="None")


@app.route('/play_video/',methods=['GET','POST'])
def play_video():
    if request.method=='POST':
        test=0
        id=request.form['Customer_id']
        d=request.form['sub1']
        d=d[1:len(d)-1]
        v=d.split(',')
        value=[]
        for i in v:
            if(i.strip()[0]=="'"):
                value.append(i.strip()[1:len(i.strip())-1])
            else:
                value.append(i.strip())
        Query=text(f'Select Subscription_ID,Expire_Date from Subscribe where Customer_ID="{id}"')
        output=engine.connect().execute(Query).fetchall()
        sub_list=[]
        exp_date=[]
        for i in output:
            sub_list.append(i[0])
            exp_date.append(i[1])
        check=[]
        for i in exp_date:
            if(datetime.datetime.strptime(i, "%d-%m-%Y")>datetime.datetime.now()):
                check.append(True)
            else:
                check.append(False)
        for i in range(len(check)):
            if(check[i]):
                if(sub_list[i] in value):
                    test=1
        return render_template('OTT_Service_video_page.html',t=test,id=id)

@app.route('/User_data/',methods=['GET','POST'])
def user_data():
    if request.method=='POST':
        id=request.form['Customer_id']
        output1=[]
        output2=[]
        Query=text(f"select * from Customer where Customer_ID='{id}'")
        out1=engine.connect().execute(Query).fetchall()
        Query=text(f"select * from Customer_Address where Customer_ID='{id}'")
        out2=engine.connect().execute(Query).fetchall()
        Query=text(f"select * from Customer_Phone_No where Customer_ID='{id}'")
        out3=engine.connect().execute(Query).fetchall()
        Query=text(f"select Subscription_ID,Subscription_Date,Expire_Date date,Subscription_Type,Price from Subscribe natural join Subscription where s1.Customer_ID='{id}'")
        out4=engine.connect().execute(Query).fetchall()
        Query=text(f"select Payment_ID,Subscription_Type,Amount,Payment_Date,Payment_type from Customer natural join payment natural join Subscription where c1.Customer_ID='{id}'")
        output3=engine.connect().execute(Query).fetchall()
        for i in out1[0]:
            output1.append(i)
        for i in out2:
            output1.append(i[0])
        if(len(out2)==1):
            output1.append(' ')
        for i in out3:
            output1.append(i[0])
        if(len(out3)==1):
            output1.append(' ')
        for i in out4:
            x=[]
            for j in range(len(i)):
                if(j==2):
                    if(datetime.datetime.strptime(i[2], "%d-%m-%Y")>datetime.datetime.now()):
                        x.append(str(datetime.datetime.strptime(i[2], "%d-%m-%Y")-datetime.datetime.now())[0:2].strip()+' days left')
                    else:
                        x.append('expire')
                else:
                    x.append(i[j])
            output2.append(x)
        return render_template('OTT_Service_User_data_page.html',id=id,customber_data=output1,Subscription_data=output2,payment_data=output3,error_e=' ',error_r=' ',error_p=' ',values=[' ','',''],check=0)

@app.route('/Sign_up/',methods=['GET','POST'])
def Sign_up():
    if request.method=='POST':
        id=request.form['Customer_id']
        value=[]
        if(id!='None'):
            d=request.form['data_all']
            d=d[1:len(d)-1]
            v=d.split(',')
            value1=[]
            for i in v:
                if(i.strip()[0]=="'"):
                    value1.append(i.strip()[1:len(i.strip())-1])
                else:
                    value1.append(i.strip())
            value=[value1[3],value1[2],value1[0],value1[6],value1[7],value1[4],value1[5]]
        else:
            for i in range (9):
                value.append('')
        error=' '*44
        return render_template('OTT_Service_Sing_Up_page.html',error_f=error,error_l=error,error_em=error,error_n=error,error_ad=error,error_p=error,error_r=error,error_x=error,id=id,values=value)

@app.route('/Subscription/',methods=['GET','POST'])
def subcription():
    if request.method=='POST':
        id=request.form['Customer_id']
        Query=text("Select * from Subscription")
        output=engine.connect().execute(Query).fetchall()
        err=' '.center(50)
        v=[]
        v.append(id)
        for i in range(8):
            v.append('')
        return render_template('OTT_Service_Subscription_page.html',subscription=output,error_sub=err,error_method=err,error_third=err,error_cname=err,error_cno=err,error_mm=err,error_yy=err,error_cv=err,values=v)

@app.route('/signed_in/',methods=['GET','POST'])
def singed_in():
    if(request.method=='POST'):
        uname=request.form['username']
        password=request.form['singpass']
        Query=text("Select * from User_Login_data")
        output=engine.connect().execute(Query).fetchall()
        if (str(uname).strip(),str(password).strip()) in output :
            Query=text(f"Select Customer_ID from Customer where Email='{str(uname).strip()}'")
            output=engine.connect().execute(Query).fetchall()
            id=output[0][0]
            return render_template('OTT_Service_Home_page.html',singed=1,customber_id=id)
        else:
            return render_template('OTT_Service_Login_page.html',error_sing=1)

@app.route('/New_Subscription/',methods=['GET','POST'])
def New_Subscription():
    check=0
    value=[]
    if request.method=='POST':
        value=[request.form['Customer_id'],request.form['Subscription'],request.form['payment'],request.form['third'],request.form['cname'],request.form['cno'],request.form['expmonth'],request.form['expyear'],request.form['cvc']]
        subscription=request.form['Subscription']
        error_third=' '.center(50)
        error_mm=' '.center(50)
        error_yy=' '.center(50)
        error_cno=' '.center(50)
        error_cname=' '.center(50)
        error_cv=' '.center(50)
        method=request.form['payment']
        id=request.form['Customer_id']
        if(subscription):
            Query=text(f"select * from Subscribe where Customer_ID='{id}'")
            output=engine.connect().execute(Query).fetchall()
            sub_data=[]
            for i in output:
                sub_data.append(i[3])
                if(i[3]==subscription):
                    ex_date=datetime.datetime.strptime(i[1],'%d-%m-%Y')
                    if(datetime.datetime.now()<ex_date):
                        error_sub="*This pack is already you had selected please select another"
                        break
            else:
                error_sub=" ".center(50)
            if(subscription=='SUBSCRIPTION_0'):
                if 'SUBSCRIPTION_0' in sub_data:
                    error_sub="*you can select free pack only once and that you already taken"
                else:
                    error_sub=" ".center(50)
        else:
            check=1
            error_sub="*Please Select one Sunscription Pack".center(50)
        if(method):
            error_method=" ".center(50)
        else:
            error_method="*Please select Payment method ".center(50)
            check=1
        if(method=="Third-party Billing"):
            third=request.form['third']
            if(third!=''):
                error_third=' '.center(50)
            else:
                check=1
                error_third='*Select the billing company'.center(50)
        elif(method=="Debit card") or (method=="Credit card"):
            name=request.form['cname']
            no=request.form['cno']
            mm=request.form['expmonth']
            yy=request.form['expyear']
            cv=request.form['cvc']
            if(not name):
                error_method="Please fill up Required filled".center(50)
                error_cname='*Card Holder Name is missing'.center(50)
                check=1
            else:
                error_cname=' '.center(50)
            if(len(no)==16 or len(no)==12):
                if(str(no).isdigit()):
                    card_no=[]
                    sum_even=0
                    sum_odd=0
                    for i in range(len(no)):
                        card_no.append(int(no[i]))
                    for i in range(len(card_no)):
                        if(i%2==0):
                            x=card_no[i]*2
                            if(len(str(x))>1):
                                x=(x%10)+(x//10)
                                sum_even+=x
                            else:    
                                sum_even+=x
                        else:
                            sum_odd+=card_no[i]
                    valid=((sum_even+sum_odd)%10==0)
                    if(valid):
                        error_cno=' '.center(50)
                    else:
                        error_method="*Please fill up Required filled".center(50)
                        error_cno='*Invalid Card No1'.center(50)
                        check=1
                else:
                    check=1
                    error_method="*Please fill up Required filled".center(50)
                    error_cno='*Invalid Card No2'.center(50)
            else:
                check=1
                error_cno='*Invalid Card No3'.center(50)
            if(mm):
                if(str(mm).isdigit()):
                    if((len(mm)==2 or len(mm)==1) and (int(mm)<=12 and int(mm)>=1 )):
                        error_mm=' '.center(50)
                    else:
                        error_method="*Please fill up Required filled".center(50)
                        error_mm='*Invaldi Expire-Month (enter in MM ex.(01))'
                        check=1
                else:
                        error_method="*Please fill up Required filled".center(50)
                        error_mm='*Invaldi Expire-Month'
                        check=1
            else:
                    error_method="*Please fill up Required filled".center(50)
                    error_mm='*Expire month is missing'
                    check=1
            if(yy):
                if(str(yy).isdigit()):
                    if(len(yy)==4 and (int(yy)<=2050 and int(yy)>=2020)):
                        error_yy=' '.center(50)
                    else:
                        error_method="*Please fill up Required filled".center(50)
                        error_yy='*Invaldi Expire-Year (enter in YYYY ex.(2021))'.center(55)
                        check=1
                else:
                        error_method="*Please fill up Required filled".center(50)
                        error_yy='*Invaldi Expire-Year (enter in YYYY ex.(2021))'.center(55)
                        check=1
            else:
                error_yy='*Expire year is missing'
                check=1
            if(cv):
                if(len(cv)==4 or len(cv)==3):
                    error_cv=' '.center(50)
                else:
                    error_method="*Please fill up Required filled".center(50)
                    error_cv='*Invaldi CVC Number'.center(55)
                    check=1
            else:
                error_cv='*Invaldi CVC Number'.center(55)
                check=1
        if(check!=1):
            error_method=" ".center(50)
        if(check==1):
            Query=text("Select * from Subscription")
            output=engine.connect().execute(Query).fetchall()
            return render_template('OTT_Service_Subscription_page.html',subscription=output,error_sub=error_sub,error_method=error_method,error_third=error_third,error_cname=error_cname,error_cno=error_cno,error_mm=error_mm,error_yy=error_yy,error_cv=error_cv,values=value)
        else:
            if(str(request.form['payment'])=='Third-party Billing'):
                method=str(request.form['third'])+'-'+str(request.form['payment'])
            else:
                method=str(request.form['payment'])
            sub1.add(request.form['Subscription'],id,method)
            return render_template('OTT_Service_Home_page.html',singed=1,customber_id=id)

@app.route('/Subscribe/',methods=['GET','POST'])
def subscribe():
    check=0;
    value=[]
    if request.method=='POST':
        id=request.form['Customer_id']
        first_name= request.form['first_name']
        last_name= request.form['last_name']
        email=request.form['email']
        num1=request.form['num1']
        num2=request.form['num2']
        add1=request.form['Address1']
        add2=request.form['Address2']
        if(id=='None'):
            pass1=request.form['pass']
            pass2=request.form['repass']
        else:
            error_p=' '.center(44)
            error_r=' ' 
        value.append(first_name)
        if(not first_name): 
            error_f='*First name is missing its required'.rjust(50)
            check=1
        else:
            error_f=' '*44
        value.append(last_name)
        if(not last_name):
            error_l='*Last name is missing its required'.rjust(50)
            check=1
        else:
            error_l=' '.center(44)
        value.append(email)
        if(not email):
            error_em='*Email is missing its required fill up'.rjust(50)
            check=1
        elif(re.match(r"[a-zA-Z0-9._]{2,}?@[a-zA-Z]{2,}?\.[a-zA-z]{2,}",email,re.MULTILINE)):
            Query=text("Select Email from Customer")
            output=engine.connect().execute(Query).fetchall()
            if(id=='None'):
                for i in output:
                    if email.strip()==str(i[0]).strip():
                        error_em='*This mail is already have account add new account'.rjust(55)
                        check=1
                if(check!=1):
                    error_em=' '.rjust(50)
            else:
                Query=text(f"Select Email from Customer where Customer_ID='{id}'")
                output2=engine.connect().execute(Query).fetchall()
                if(output2[0][0]==email):
                    error_em=' '.rjust(50)
                else:
                    for i in output:
                        if email.strip()==str(i[0]).strip():
                            error_em='*This mail is already have account add new account'.rjust(55)
                            check=1
            if(check!=1):
                error_em=' '.rjust(50)
        else:
            error_em='*invalid Email'.rjust(50)
            check=1
        value.append(num1)
        value.append(num2)
        if(not num1) and (not num2) or ((len(num1)<10 and len(num2)<10)):
            error_n='*Mobile no is missing its required or invalid'.rjust(50)
            check=1
        else:
            error_n=' '.center(44)
        if(num1==num2):
            check=1
            error_n='*Mobile nos are same please only once '.rjust(50)
        value.append(add1)
        value.append(add2)
        if(not add1) and (not add2):
            error_ad='*Address is missing its required'.rjust(50)
            check=1
        else:
            error_ad=' '.center(44)
        if(add1.lower()==add2.lower()):
            error_ad='*Address are same please only once '.rjust(50)
            check=1
        if(id=="None"):
            value.append(pass1)
            if(not pass1):
                error_p='*Please enter new Password'.rjust(50)
                check=1
            elif (len(pass1)<8) or (not any(map(str.isdigit,pass1))) or (not any(map(str.isupper,pass1))) or (not any(map(str.islower,pass1))):
                error_p='*Password must contain Upper lower case and digit'.rjust(55)
                check=1
            else:
                error_p=' '.center(44)
                value.append(pass2)
            if(pass1!=pass2):
                error_r='*Please check Confirm Password'.rjust(50)
                check=1
            else:
                error_r=' '.center(44)
        if(check==1):
            return render_template('OTT_Service_Sing_Up_page.html',error_f=error_f,error_l=error_l,error_em=error_em,error_n=error_n,error_ad=error_ad,error_p=error_p,error_r=error_r,error_x=' '.center(44),id=id,values=value)        
        else:
            mobile_no=[]
            address=[]
            if(num1):
                mobile_no.append(num1)
            if(num2):
                mobile_no.append(num2)
            if(add1):
                address.append(add1)
            if(add2):
                address.append(add2)
            if(id=='None'):
                id=customber.add(first_name,last_name,email,pass1,mobile_no,address)
                Query=text("Select * from Subscription")
                output=engine.connect().execute(Query).fetchall()
                err=' '.center(50)
                v=[]
                v.append(id)
                for i in range(8):
                    v.append('')
                return render_template('OTT_Service_Subscription_page.html',subscription=output,error_sub=err,error_method=err,error_third=err,error_cname=err,error_cno=err,error_mm=err,error_yy=err,error_cv=err,values=v)
            else:
                l1=['Email','Last_Name','First_Name']
                l2=[email,last_name,first_name]
                customber.update(id,l1,l2,mobile_no,address)
                return render_template('OTT_Service_Home_page.html',singed=1,customber_id=id)

@app.route('/Change_Password/',methods=['GET','POST'])
def Change_Password():
    if request.method=='POST':
        check=0
        error_e=' '.rjust(50)
        error_r=' '.rjust(50)
        error_p=' '.rjust(50)
        id=request.form['Customer_id']
        email=request.form['email1']
        pass1=request.form['password1']
        pass2=request.form['password2']
        Query=text(f'select Email from Customer where Customer_ID="{id}"')
        output=engine.connect().execute(Query).fetchall()
        if(output[0][0]==email):
            Query=text(f'select Password from User_Login_data where Email="{email}"')
            output=engine.connect().execute(Query).fetchall()
            if(not pass1):
                error_p='*Please enter new Password'.rjust(50)
                check=1
            elif (len(pass1)<8) or (not any(map(str.isdigit,pass1))) or (not any(map(str.isupper,pass1))) or (not any(map(str.islower,pass1))):
                error_p='*Password must contain Upper lower case and digit'.rjust(55)
                check=1
            if(pass1!=pass2):
                error_r='*Please check Confirm Password'.rjust(50)
                check=1
            if(pass1==output[0][0]):
                error_p='*This is your old password please select new one'.rjust(55)
                check=1
        else:
            error_e='*invalid Email'.rjust(50)
            check=1
        if(check==1):
            return render_template('OTT_Service_User_data_page.html',id=id,customber_data=['','','','','','','',''],Subscription_data=['','','','',''],payment_data=['','','','','',''],error_e=error_e,error_r=error_r,error_p=error_p,values=[email,pass1,pass2],check=1)
        else:
            Query=text(f'Update User_Login_data set Password="{pass1}" where Email="{email}"')
            engine.connect().execute(Query)
            return render_template('OTT_Service_Home_page.html',singed=1,customber_id=id)

@app.route('/Set_password/',methods=['GET','POST'])
def Set_password():
    if request.method=='POST':
        check=0
        error_e=' '.rjust(50)
        error_r=' '.rjust(50)
        error_p=' '.rjust(50)
        id=request.form['Customer_id']
        email=request.form['email1']
        pass1=request.form['password1']
        pass2=request.form['password2']
        Query=text(f'select Email from Customer')
        out1=engine.connect().execute(Query).fetchall()
        output=[]
        for i in out1:
            output.append(i[0])
        if(email in output):
            Query=text(f'select Password from User_Login_data where Email="{email}"')
            output=engine.connect().execute(Query).fetchall()
            if(not pass1):
                error_p='*Please enter new Password'.rjust(50)
                check=1
            elif (len(pass1)<8) or (not any(map(str.isdigit,pass1))) or (not any(map(str.isupper,pass1))) or (not any(map(str.islower,pass1))):
                error_p='*Password must contain Upper lower case and digit'.rjust(55)
                check=1
            if(pass1!=pass2):
                error_r='*Please check Confirm Password'.rjust(50)
                check=1
            if(pass1==output[0][0]):
                error_p='*This is your old password please select new one'.rjust(55)
                check=1
        else:
            error_e='*invalid Email'.rjust(50)
            check=1
        if(check==1):
            return render_template('OTT_Service_Forgotten_Password_Page.html',id=id,values=[email,pass1,pass2],error_e=error_e,error_r=error_r,error_p=error_p)
        else:
            #update User_login
            Query=text(f'Update User_Login_data set Password="{pass1}" where Email="{email}"')
            engine.connect().execute(Query)
            return render_template('OTT_Service_Login_page.html',error_sing=0,id=None)

            
@app.route('/forgot_password/',methods=['GET','POST'])
def forgot_password():
    error_e=' '.rjust(50)
    error_r=' '.rjust(50)
    error_p=' '.rjust(50)
    if request.method=='POST':
        id=request.form['Customer_id']
        return render_template('OTT_Service_Forgotten_Password_Page.html',id=id,values=['','',''],error_e=error_e,error_r=error_r,error_p=error_p)
    

@app.route('/Home_page/',methods=['GET','POST'])
def log_out():
    if request.method=='POST':
        return render_template('OTT_Service_Home_page.html',singed=0,customber_id=None)
app.run(host="0.0.0.0",port=5000)
