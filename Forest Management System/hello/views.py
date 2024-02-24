from email import message
from email.message import EmailMessage
import os
from random import randint
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.mail import send_mail
import hashlib
from hello.models import customer, Product, Visitors_pass
from easy_pdf.rendering import render_to_pdf
# Create your views here.
def home(request):
    return render(request,"home.html")

def user(request):
    return render(request,"user.html")

def uuser(request):
    cust_name=request.GET.get('cust_name')
    password=request.GET.get('password')
    password=hashlib.md5(password.encode('utf-8')).hexdigest()
    address=request.GET.get('address')
    phone=request.GET.get('phone')
    email=request.GET.get('email')
    u=customer(cust_name=cust_name,password=password,address=address,phone=phone,email=email)
    u.save()
    v=customer.objects.get(email=email)
    res = send_mail("Customer registration", "Congratulations...! "+v.cust_name+" Your registration is successfull and your customer id is "+str(v.id) , "forestfsm@gmail.com", [email])
    return render(request,"login.html")

def login(request):
    return render(request,"login.html")

def ulogin(request):
    cust_name=request.GET.get('cust_name')
    password=request.GET.get('password')
    password=hashlib.md5(password.encode('utf-8')).hexdigest()
    print(cust_name,password)
    u=customer.objects.filter(cust_name=cust_name,password=password)
    if(u):
        response=render(request,'userpart.html')
        response.set_cookie('cust_name',cust_name)
        return response
    else:
        return render(request,'login.html')

def order(request):
    return render(request,"orders.html")

def orders(request):
    pro_list=Product.objects.all()

    istr='''
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script>
       function ord(ono)
       {
           $.get("http://127.0.0.1:8000/uorder/",{ono:ono}).done(function(data)
           {
               alert(data);
           });
       }
    </script>
    
    '''
    cnt=1
    for proi in pro_list:
        istr+='''
        <div class="w3-quarter" >
            <br><br>
                <div class="card">
                    <img src="http://127.0.0.1:8000/hello/media/hello/media/'''+str(cnt)+'''.jpg" style="width:100%">
                    <h3>'''+proi.p_name+'''</h3>
                    <p class="price">'''+proi.p_price+'''</p>
                    <p>'''+proi.p_description+'''</p>
                    <p><button type="button" id="ordnow" onclick=ord('''+str(proi.id)+''')>Buy</button></p>
                </div>
         </div>
        '''

        cnt+=1
    if cnt%4 == 0:
        istr+='''</div><div>'''

    return HttpResponse(istr)

from django.core.mail import EmailMessage
def uorder(request):
    cust_name=request.COOKIES.get('cust_name')
    ono=request.GET.get('ono')
    m=Product.objects.filter(id=ono)
    c=customer.objects.filter(cust_name=cust_name)
    c.first().orders.add(m.first())
    c=customer.objects.get(cust_name=cust_name)
    email=c.email
    p=Product.objects.get(id=ono)
    p_name=p.p_name
    p_price=p.p_price
    p_description=p.p_description
    template = 'orderdetail.html'
    context = {'ono' : ono,'p_name':p_name,'cust_name':cust_name,'p_price':p_price,'p_description':p_description}
    pdf = render_to_pdf(template, context)
    email = EmailMessage("Order", "Product ordering", "forestfsm@gmail.com", [email])
    email.content_subtype = "pdf"
    email.attach('Product_ordering', pdf, 'application/pdf')
    res = email.send()
    return HttpResponse("Order placed successfully...")

def orderhistory(request):
    return render(request,"orderhistory.html",)

def uorderhistory(request):
    cust_name=request.COOKIES.get('cust_name')
    c=customer.objects.filter(cust_name__icontains=cust_name)
    o=c.first().orders.all()
    istr='''
    <div class="w3-padding-16" style="margin-left : 10px;"><b>Customer ID : </b>'''+str(c.first().id)+'''</div>
    <div class="w3-padding-16" style="margin-left : 10px;"><b>Customer Name : </b>'''+cust_name+'''</div>
     <table>
      <tr>
        <th>Product_ID</th>
        <th>Product_Name</th>
        <th>Description</th>
        <th>Price</th>
      </tr>
    '''
    cnt=1

    for a in o:
        p=Product.objects.get(id=a.id)
        istr+='''
                <tr>
                <td>'''+str(a.id)+'''</td>
                <td>'''+p.p_name+'''</td>
                <td>'''+p.p_description+'''</td>
                <td>'''+str(p.p_price)+'''</td>
                </tr>
        '''
    cnt+=1
    return HttpResponse(istr)

def upass(request):
    return render(request,"pass.html")

def uupass(request):
    cust_name=request.COOKIES.get('cust_name')
    date_of_visit=request.GET.get('date_of_visit')
    price=request.GET.get('price')
    c=customer.objects.filter(cust_name__icontains=cust_name)
    for a in c:
        print(a.id)
    print(cust_name,date_of_visit,a.id)
    v=Visitors_pass(date_of_visit=date_of_visit,price=price,vpass_id=a.id)
    v.save()
    c=customer.objects.get(cust_name=cust_name)
    email=c.email
    date_of_visit=v.date_of_visit
    price=v.price
    template = 'passdetail.html'
    context = {'cust_name':cust_name,'date_of_visit':date_of_visit,'price':price}
    pdf = render_to_pdf(template, context)
    email = EmailMessage("Pass", "Visitor Pass", "forestfsm@gmail.com", [email])
    email.content_subtype = "pdf"
    email.attach('Pass', pdf, 'application/pdf')
    res = email.send()
    return HttpResponse("Pass sent to your registered mail.")

def userpart(request):
    return render(request,"userpart.html")

def sendSimpleEmail(request):
   res = send_mail("hi", "Hope you are doing fine", "forestfsm@gmail.com", ["chandanchandu266266@gmail.com"])
   return HttpResponse('%s'%res)

#Get OTP
def getotp(request):
    otp = randint(000000,999999) 
    email=request.GET.get('email') 
    file_exists = os.path.exists('enm.txt')
    ss=''
    if file_exists:
        f = open("enm.txt", "r")
        for fh in f:
            s=fh.split(":")
            em=s[0]
            if em==email:
                continue
            s+=fh
        f.close()        
    f = open("enm.txt", "w")
    ss+=email+":"+str(otp)
    f.write(ss)
    f.close()
    send_mail("OTP", "Your OTP is "+str(otp), "forestfsm@gmail.com", [email])
    return HttpResponse('Mail sent')

#Get change of password html page
def cpass(request):
    return render(request,"cpass.html")

#implementing change of password method
def changepass(request):
    email=request.GET.get('email') 
    rotp=request.GET.get('rotp') 
    npsw=request.GET.get('npsw') 
    f = open("enm.txt", "r")
    for fh in f:
        s=fh.split(":")
        em=s[0]
        otp=s[1]
        if em==email and otp==rotp :
                c=customer.objects.get(email=email)
                npsw=hashlib.md5(npsw.encode('utf-8')).hexdigest()
                c.password=npsw
                c.save()

                return HttpResponse("Password changed successfully...")
    return HttpResponse("OTP invalid")