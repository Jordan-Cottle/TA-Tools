# TA-Tools
A collection of tools I've built to assist in grading and organizing my work as a grader/TA

Most of the scripts in this project require the creation of an info.py file. When using a script, look for info being imported and make note of any components required inside of it. For these scripts to fucntion properly you will need to create an info.py file that satisfies the requirements of the script.

* setup.py is a tool to rename and organize bulk submissions downlaoded from canvas

* grading.py is a tool to compile and execute java source code in bulk organized into folders

* labPartners.py takes a list of students and divides them into random teams of 2. 
  * Teams will be made of all male-male and female-female pairs wherever possible. 
  * A single team of three or a male-female team may be created due to an odd number of students or an extra male and female. 
  * Creating a male-female team is prioritized over creating two teams of 3 
