import requests as r
import time
from bs4 import BeautifulSoup
from login_values import *

login_data = {
    'anchor' : '',
    'username' : username,
    'password' : password                             #initialising data variables
}

print('logging in...')
s = r.Session()
res = s.get('https://' + domain + '/login/index.php')
soup = BeautifulSoup(res.content, 'html5lib')
login_data['logintoken'] = soup.find('input', attrs={'name': 'logintoken'})['value']
res = s.post('https://' + domain + '/login/index.php', data=login_data)
if res.status_code==200:
    print("login successful :)\n")
    subs_list = []
    while(True):
        # finding available attendances 
        res = s.get('https://' + domain + '/calendar/view.php?view=day')                  #domain
        soup = BeautifulSoup(res.content, 'html5lib')
        l = soup.find_all('div', attrs={'data-type':'event'})
        count=0                                                            #initialising data variables
        new_sub_list = []
        data=[]
        for i in l:
            i = str(i)
            x = BeautifulSoup(i, 'html5lib')                                        #initialising beautifulsoap
            sub = {}
            link = x.find('a',attrs={'class':'card-link'})['href']
            if link.startswith('https://' + domain + '/mod/attendance/view.php?id='):
                sub['link'] = link
                new_sub_list.append(link)
                for j in x.find_all('a'):
                    if j['href'].startswith('https://' + domain + '/course/view.php?id='):
                        sub['name'] = j.text
                for j in x.find_all('div',attrs={'class': 'col-xs-11'}):
                    if j.text.startswith('Today'):
                        sub['time'] = j.text.split(', ')[1]
                        sub['timestamp'] = BeautifulSoup(str(j),'html5lib').find('a')['href'].split('time=')[1]
                if int(sub['timestamp'])>time.time():
                    count+=1
                data.append(sub)

        # printing available attendances
        if subs_list!=new_sub_list or subs_list==[]:
            print("\n#####   Today's Attendances    #####\n")
            for i in data:
                if len(i['name'])>35:
                    print(i['name'][:33]+'..','\t', i['time'])
                else:
                    print(i['name'].ljust(35),'\t', i['time'])
            print("\n####################################\n\n\n")
            subs_list = new_sub_list

        # submitting the attendance
        if count>0:
            for i in data:
                if int(i['timestamp'])>time.time():
                    att_data = {
                        '_qf__mod_attendance_form_studentattendance': '1',
                        'mform_isexpanded_id_session': '1',
                        'submitbutton': 'Save changes'
                    }
                    res = s.get(i['link'])
                    soup = BeautifulSoup(res.content, 'html5lib')
                    for j in soup.find_all('a'):
                        try:
                            if j['href'].startswith('https://' + domain + '/mod/attendance/attendance.php?sessid='):
                                x = s.get(j['href'])
                                x = BeautifulSoup(x.content, 'html5lib')
                                att_data['status'] = x.find('input', attrs={'name' : 'status'})['value']
                                att_data['sessid'],att_data['sesskey'] = j['href'].split('sessid=')[1].split('&sesskey=')
                                # print(att_data)
                                res = s.post('https://' + domain + '/mod/attendance/attendance.php', data=att_data)
                                if(res.status_code==200):
                                    print(':: Submitted attendance of '+ i['name']+'.\n')
                                else:
                                    print(':: Failed to submit attendance of '+ i['name']+'.\n')
                        except:
                            pass

        time.sleep(200)
else:
    print('login failed :(')
