import re,bs4,requests,matplotlib,argparse
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import matplotlib.pyplot as plt
driver = webdriver.PhantomJS()
#avg marks among all students in  3rdsem,4thsem and subjects 
avgresult = {}
#mapping of student marks subject wise with key=Rollno
finaldata = {}
#mapping of laboratory total with key=Rollno
labdata = {}
def get_soup(text):
    return bs4.BeautifulSoup(text,'html.parser')
def display_single_student_detail(student,rollno):
    print 'Name:'+student['Name:']
    print 'Rollno:',rollno
    print 'Labtotal:(4thSem)', labdata[rollno]
    for key in sorted(student.keys()):
        if key != 'Name:':
            print key,student[key]

def extract_resultdata(soup,rollno):
    labdata[rollno] = 0
    student = {}
    labflag = False
    for tag in soup.find_all('span'):
        if tag.has_attr('id'):
            text = str(tag.get_text()).strip()
            
            if re.match(r'^lblsubject([1-9]|1[0-1])$',tag['id']) and re.match(r'\w+',text):
                sub = text
                if not avgresult.has_key(sub):
                    avgresult[sub] = 0
                if re.search(r'laboratory',sub,re.IGNORECASE):
                    labflag = True
            elif re.match(r'^lblsubTotal([1-9]|1[0-1])$',tag['id']) and re.match(r'\d+',text):
                student[sub] = text
                avgresult[sub] += int(text)
                if labflag:
                    labdata[rollno]+=int(text)
                    labflag = False
            
            elif re.match(r'lblPrvSemObnTot',tag['id']) and re.match(r'\d+',text):
                if not avgresult.has_key('3rdSemTotal'):
                    avgresult['3rdSemTotal']=0
                else:
                    avgresult['3rdSemTotal'] += int(text)
                student['3rdSemTotal']=text
                
            elif re.match(r'lblSemMarksTotal',tag['id']) and re.match(r'\d+',text):
                if not avgresult.has_key('4thSemTotal'):
                    avgresult['4thSemTotal']=0
                else:
                    avgresult['4thSemTotal']+=int(text)
                student['4thSemTotal']=text
    
    #result html src contains student name and father name alternatively with same style attribute
    #but only student_name is enough for result detail,hence ommiting the father's name
    flag =1
    for name in soup.find_all('td'):
        if name.has_attr('style') and name['style'] =='width:50%':
            out=str(name.get_text()).strip()
            if flag == 1 and re.match(r'\S+',out):
                student['Name:'] =out
                flag =0
            else:
                flag = 1 
    #display current student detail            
    display_single_student_detail(student,rollno)
    finaldata[rollno]=student;
    
def ghost_browser(args):
    #range of rollno
    x = 1
    y = 32
    if args.range:
        if len(args.range) > 1:
            y = args.range[1]
        x = args.range[0]
        
    for i in xrange(x,y+1):        
        roll=driver.find_element_by_id('ChildContent_txtRollNo')
        roll.clear()
        inp = '13cse44'
        inp=inp+abs(10-len(inp+str(i)))*'0'+str(i)
        print ".............Processing Rollno:"+inp+".............."
        roll.send_keys(inp)
        driver.find_element_by_id('ChildContent_btnShowResult').click()
        extract_resultdata(get_soup(driver.page_source),inp)
        driver.back()
        
def display_text():
    for key in sorted(finaldata.keys()):
            print "\nRollNo:%s"%(key)
            print "Name:",finaldata[key]['Name:']
            for ky in sorted(finaldata[key].keys()):
                if ky !='Name:':
                    print ky,finaldata[key][ky]

def lab_vs_theory():
    labres=[]
    theoryres=[]
    for key in sorted(finaldata.keys()):
        theoryres.append(int(finaldata[key]['4thSemTotal'])-labdata[key])
        labres.append(labdata[key])
    student =[i for i in xrange(1,len(labres)+1)]
    plt.plot(student,labres,linestyle='--',marker='o',color='k',label='LabTotal') 
    plt.plot(student,theoryres,marker='x',color='b',label='TheoryTotal')
    plt.xlabel('Students Rollno.')
    plt.ylabel('Total Marks in Theory vs Laboratory in 4thSem')
    plt.legend()
    print '\nSaving Graph of lab vs theory marks distribution'
    plt.savefig('lab_vs_theory.png')
    plt.clf()
def prev_vs_currsem():
    prevsem = []
    currsem = []
    for key in sorted(finaldata.keys()):
        prevsem.append(finaldata[key]['3rdSemTotal'])
        currsem.append(finaldata[key]['4thSemTotal'])
    student = [i for i in xrange(1,len(currsem)+1)]   
    plt.plot(student,prevsem,linestyle='--',marker='x',color='r',label='3rdSem')
    plt.plot(student,currsem,marker='o',color='k',label='4thSem')
    
    plt.xlabel('Students RollNo')
    plt.ylabel('Total Marks Obtained in 3rdSem vs 4th Sem')
    plt.legend()
    print '\nSaving Graph of prev vs curr sem comparision' 
    plt.savefig('3rdsem_vs_4thsem.png')  
def avg_marks_dist():
    plt.clf()
    subject = []
    marks = []
    for title in sorted(avgresult,key=avgresult.get,reverse=True):
        if not re.search(r'[34](rd|th)SemTotal',title):
            subject.append(title)
            marks.append(float(avgresult[title])/(1.0*len(finaldata.keys())))
   
    plt.pie(marks,labels=subject,colors=['b', 'g', 'w', 'c', 'b', 'y', 'g', 'w','r','c'],shadow=True,autopct='%.2f%%') 
    plt.title('Total-Average-Marks in 4th Sem:'+str(round(avgresult['4thSemTotal']/(1.0*len(finaldata.keys())),2)))
    matplotlib.rcParams.update({'font.size':8})
    #plt.show()
    print '\nSaving Pie Chart for avg-Marks'
    plt.savefig('avg_marks.png')
def mean_result():
    for title in sorted(avgresult,key=avgresult.get,reverse =True):
        #if title !='3rdSemTotal' or title != '4thSemTotal':
        print title,round(avgresult[title]/(1.0*len(finaldata.keys())),2)
def main(args):
    driver.get('http://182.71.46.50/result.aspx')
    #exam/course name i.e B.E,M.E etc
    myid=Select(driver.find_element_by_id('ChildContent_ddlExamName'))
    myid.select_by_value('B.E.')
    #selecting semester
    myid = Select(driver.find_element_by_id('ChildContent_ddlSemYear'))
    myid.select_by_value('04')
    #selecting stream 
    myid = Select(driver.find_element_by_id('ChildContent_ddlStream'))
    myid.select_by_value('COMPUTER SCIENCE & ENGINEERING')
    #headless browser will automate task of real browser
    ghost_browser(args)
    lab_vs_theory()
    prev_vs_currsem()
    avg_marks_dist()
    driver.close()    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--range',nargs='+',type=int,choices=xrange(1,33),help='display result between given roll numbers')
    args = parser.parse_args()
    main(args)
