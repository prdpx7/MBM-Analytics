# MBM-Analytics
College Result Analysis
--------
*due to change in university website, it might not work now*

**Extracting Yearend Semester Result Using PhantomJS and Selenium Webdriver in Python2.7**
* Extraction of Result according to the Student's RollNo will include Total Marks in Previous Semester as well as year-end Semester
  and Marks in each Theory Exam as well Laboratory/Practical Exam.
* Displaying Result Details of Each Student for given range in RollNo.
* First graph will compare Total marks of 3rd Sem(prev sem) with 4th Sem(year-end sem) from RollNo.1 to 32 ( all students who are enrolled in both exams ).
![3rd_vs_4th](https://raw.githubusercontent.com/prdpx7/MBM-Analytics/master/3rdsem_vs_4thsem.png)
* Second graph will compare Total Marks obtained in Theory Exams vs Lab/Practical Exams of year-end Semester(4thSem,2015).
![theory vs lab](https://raw.githubusercontent.com/prdpx7/MBM-Analytics/master/lab_vs_theory.png)
* Pie Chart will show avg-marks among all subjects(Theory and Practicals) of the year-end Semester(4thSem,2015).
![pie chart](https://raw.githubusercontent.com/prdpx7/MBM-Analytics/master/final_avg_dist.png)

#### Demo
[![asciicast](https://asciinema.org/a/aofoemh6caq9jl5mrsvxbv6jf.png)](https://asciinema.org/a/aofoemh6caq9jl5mrsvxbv6jf)

**Resources used in this Project**
* [Matplotlib](http://matplotlib.org/)
* [Selenium](http://selenium-python.readthedocs.org/)
* [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [PhantomJS](http://phantomjs.org/)

**Installation**
```
$ sudo apt-get phantomjs python python-pip
$ pip install matplotlib selenium bs4 requests
$ git clone https://github.com/prdpx7/MBM-Analytics.git

```
