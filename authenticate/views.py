from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import DatabaseError
from django.contrib import auth
# from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
import models
from authentication import auth_user
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import authenticate as u_authenticate
from django.contrib.auth import logout
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.db import IntegrityError
from datetime import datetime
from workspace.views import AuthenticationPsk


header = "<span style=\"color: #ff6600; font-family: Verdana, Geneva, sans-serif;font-size: 120%;\">HUU Dashboard.</span><br><br>"
def user_login(request):
#     c = {}
#     c.update(csrf(request))
#     msg= "This URL is no longer available. Please use new HUU Dashboard URL <a href=\"http://wwwin-HUUdashboard.cisco.com\">http://wwwin-HUUdashboard.cisco.com.</a>"
    
    msg= header+"<span style=\"font-weight: normal;\"> Please use your CEC Username and Password.<br> New users can enter their CEC User-id and Password, then click on Register button. You will receive an email notification once the registration is complete.</span>"
    return render(request, 'authenticate/login.html', {'msg': msg,})

def authenticate_user(request,reg=''):

    user_id = request.POST.get('userid')
    password = request.POST.get('password')


    #print(a.password[str(user_id)])
    #print("password ",password)
    if user_id and password:
        auth_obj = auth_user()
        authenticated,result = auth_obj.ldap_bind(userid=user_id,password=password)
    else:
        msg = "Invalid CEC UserID or Password."
        return render(request, 'authenticate/login.html', {'msg': msg,})
    print  "11111",authenticated,result
    if authenticated:
        print("user_id", user_id.encode('UTF-8'))
        a = AuthenticationPsk(password_auth=password.encode('UTF-8'), user_auth=user_id.encode('UTF-8'))
        try:
            user = User.objects.get(username=user_id)
            if user and not user.is_active:
                msg = header+"You account is not yet activated. You will receive a mail once the registration process is complete."
                return render(request, 'authenticate/login.html', {'msg': msg,})
        except User.DoesNotExist:
            msg = header+"You are not a registered user."
            return render(request, 'authenticate/login.html', {'msg': msg,})
        password = '12345'
        user = u_authenticate(username=user_id, password=password)
        try:
            user = u_authenticate(username=user_id, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    msg = header+"You account is not yet activated. You will receive a mail once the registration process is complete."
                    return render(request, 'authenticate/login.html', {'msg': msg,})
        except:
            print "request", request,
            logout(request)
            msg = header+"Unable to connect to CEC. Please try after sometime."
            return render(request, 'authenticate/login.html', {'msg': msg,})
        request.session['user_d'] = result
        request.session['users'] = user_id
        return HttpResponseRedirect('/workspace/index/?authenticated')
    else:
        msg = header+"Invalid CEC UserID or Password."
        return render(request, 'authenticate/login.html', {'msg': msg,})
    return render(request, 'authenticate/login.html', {'msg': msg,})

def request_registration(request):
    user_id = request.POST.get('userid') 
    password = request.POST.get('password')
    if request.method == 'POST':

    #     user_list =['aberhane','amporter','acap','bricolli','dnadiyad','jimille2','pandari','ramsharm','rnasnas','rchikkat','smnambia','atluris','thironak','vikollur','anishgeo','gballer','tgamba']
        user_list =['anishgeo','jkhilran']
        """ The below two lines are used for access to developer in dev environment"""
        # if user_id in user_list:
        #     pass
        # #else:
        #     #return render(request,'redirect.html',{})
        """ end """
        auth_obj = auth_user()
        authenticated,result = auth_obj.ldap_bind(userid=user_id,password=password)
        print("authenticated = ",authenticated,"result =",result)
        if authenticated:
            print("**********************in authenticated **********************************")
            try:
                user = User.objects.get(username=user_id)
                if user.is_active:
                    msg = header+"You are a registered HUU Dashboard user. Please login using CEC Credentials."
                    return render(request, 'authenticate/login.html', {'msg': msg,})
                else:
                    msg = header+"You account is not yet activated. You will receive a mail once the registration process is complete."
                    return render(request, 'authenticate/login.html', {'msg': msg,})
            except User.DoesNotExist:
                #DatabaseError
                msg = "User doesnt exist"
            nw = datetime.now()
            try:
                u = User.objects.create_user(username=user_id,password='12345',first_name=result['givenName'][0], last_name=result['sn'][0], email=result['mail'][0],last_login=nw)
                u.is_active = False
                u.save()
                msg = "user saved"
            except:
                msg = header+"Registration failed. Please try again."
                return render(request, 'authenticate/login.html', {'msg': msg,})

            mail_to = 'jkhilran@cisco.com,'#gballer@cisco.com,pandari@cisco.com
            html = """Hello HUU Dashboard Admin,<br><br> User """+user_id+' raised an access request. <br>Please approve/reject user at HUU Dashboard > Admin > User Settings<br><br>HUU Dashboard.'
            sender = 'huudashboard'
            recipients = mail_to.split(',')
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "HUU:New User Registration Request"
            msg['From'] = sender
            msg['To'] = ", ".join(recipients)
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            message = ''

            try:
                server = smtplib.SMTP('outbound.cisco.com',25)
                server.sendmail(sender, recipients, msg.as_string())
                server.quit()
                message =  "Successfully sent email"
            except smtplib.SMTPException:
                message =  "Error: Unable to send email"
            msg = "Your registration request submitted. You will receive an email confirmation once the request is approved."
            return render(request, 'authenticate/registration_complete.html', {'msg': msg,})
        else:
            msg = "Incorrect CEC UserID or Password."
            print(msg)
            return render(request, 'authenticate/login.html', {'msg': msg,})

    return render(request, 'authenticate/registration_complete.html')


def approve_user(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_name')
        status = request.POST.get('status')
        print "user_id : ", user_id
        try:
            user_d = User.objects.get(username=user_id)
        except:
            #DatabaseError
            msg = "Database Error"
        if user_d:
            if status=='true':
                user_d.is_active = True
                user_d.save()
                response_data['msg'] = 'User Added'
                sub = "HUUDashboard: User Registration Request Accepted"
                html = "Hello "+user_d.first_name+" "+user_d.last_name+"<br><p> Your registration to HUU Dashboard is complete. You can now log in to HUU Dashboard portal using your CEC Credentials. <br><br>If you need any assistance please contact CSPG HUU Dashboard Team. | <a href=\"mailto:HUUdashboard@cisco.com\">HUUdashboard@cisco.com</a><p><br>HUU Dashboard Team."
            else:
                user_d.delete()
                response_data['msg'] = 'User Removed'
                sub = "HUUDashboard: User Registration Request Rejected"
                html = "Hello "+user_d.first_name+" "+user_d.last_name+"<br><p> Your registration to HUU Dashboard is rejected. <br><br>If you need any assistance please contact CSPG HUU Dashboard Team. | <a href=\"mailto:HUUdashboard@cisco.com\">HUUdashboard@cisco.com</a><p><br>HUU Dashboard Team."
        mail_to = user_d.email       
        sender = 'huudashboard'
        recipients = mail_to.split(',')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = sub
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        message = ''
        try:
            server = smtplib.SMTP('outbound.cisco.com',25)
            server.sendmail(sender, recipients, msg.as_string())   
            server.quit()      
            message =  "Successfully sent email"
        except smtplib.SMTPException:
            message =  "Error: Unable to send email"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    try:
        user_d = User.objects.get(username=user_id)
    except:
        #DatabaseError
        msg="Databse Error"
        
    try:
        inactive_users = User.objects.filter(is_active=False)
    except:
        #DatabaseError
        msg = "Databse Error"
    response_data['inactive_users'] = inactive_users
    
    try:
        all_users = User.objects.all()
    except:
        #DatabaseError
        msg = "Databse Error"
    response_data['all_users'] = all_users
    return render(request, 'authenticate/approve_user.html', response_data)

def add_user(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_name')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        nw = datetime.now()
        try:
            u = User.objects.create_user(username=user_id,password='12345',first_name=f_name, last_name=l_name, email=user_id+'@cisco.com', last_login=nw)
            u.is_active = True
            u.save() 
            msg ="User Added"
        except IntegrityError as e:
            print "#"*5, "Error : ",e.message
            msg ="User Exists"
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    try:
        inactive_users = User.objects.filter(is_active=False)
    except:
        DatabaseError
    response_data['inactive_users'] = inactive_users
    
    return render(request, 'authenticate/approve_user.html', response_data)

def delete_user(request):
    response_data = {}
    if request.method == 'POST' and request.is_ajax():
        user_id = request.POST.get('user_name')

        try:
            User.objects.get(username=user_id).delete()
        except:
            #DatabaseError
            msg ="No user found."
        msg ="User "+user_id+" Deleted."
        response_data['msg'] = msg
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return render(request, 'authenticate/approve_user.html', response_data)

def invalid(request):
    return render_to_response('authenticate/invalid.html')

def user_logout(request):
    logout(request)
    msg = "Successfully Logged Out."
    return render(request, 'authenticate/login.html', {'msg': msg,})

