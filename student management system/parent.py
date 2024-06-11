from flask import Flask,Blueprint,render_template,request,url_for,redirect,session ,flash
from database import*

parent=Blueprint('parent',__name__)

@parent.route('parent_home')
def parent_home():
	return render_template('parent_home.html')

@parent.route('parent_managestudent',methods=['post','get'])	
def parent_managestudent():
	data={}
	lid=session['lid']
	q="select * from course"
	res=select(q)
	data['co']=res

	q="select * from parent"
	res=select(q)
	data['pa']=res

	q="SELECT *,CONCAT(student.fname)AS sfname ,CONCAT(student.lname) AS slname,CONCAT(student.place)AS splace ,CONCAT (student.phone)AS sphone ,CONCAT (student.email) AS semail FROM student INNER JOIN course USING(course_id) INNER JOIN parent USING(parent_id)"
	res=select(q)
	data['stud']=res

	if "student" in request.form:
		c=request.form['c']
		
		f=request.form['fname']
		l=request.form['lname']
		a=request.form['pl']
		ph=request.form['phone']
		e=request.form['email']
		u=request.form['uname']
		p=request.form['pwd']
		q="select * from login where username='%s',password='%s'"%(u,p)
		select(q)
		if res:
			flash('already exist')

		else:
			
			q="insert into login values(null,'%s','%s','pending')"%(u,p)
			id=insert(q)
			q="insert into student values(null,'%s','%s',(select parent_id from parent where login_id='%s'),'%s','%s','%s','%s','%s')"%(id,c,lid,f,l,a,ph,e)
			insert(q)
			flash('insert successfully');
			print(q)
			return redirect(url_for('parent.parent_managestudent'))

	if "action" in request.args:
		action=request.args['action']
		sid=request.args['sid']

	else:
		action=None

	if action=='delete':
		q="delete from student where student_id='%s'"%(sid)
		delete(q)
		flash('insert successfully');
		return redirect(url_for('parent.parent_managestudent'))

	if action=='update':
		q="select * from student inner join course using (course_id) where student_id='%s'"%(sid)
		res=select(q)
		data['up']=res
	
	if  "submit" in request.form:
		c=request.form['c']
		
		f=request.form['fname']
		l=request.form['lname']
		a=request.form['pl']
		ph=request.form['phone']
		e=request.form['email']
		
		q="update student set course_id='%s',fname='%s',lname='%s',place='%s',phone='%s',email='%s'where student_id='%s'"%(c,f,l,a,ph,e,sid)
		update(q)
		flash('insert successfully');
		return redirect(url_for('parent.parent_managestudent'))
		
	return render_template('parent_managestudent.html',data=data)

@parent.route('/parent_viewattendance')
def parent_viewattendance():
	sid=request.args['sid']
	data={}
	q="select * from attendance inner join student using (student_id) where student_id='%s'"%(sid)
	res=select(q)
	data['att']=res

	return render_template('parent_viewattendance.html',data=data)

@parent.route('/parent_viewresult')	
def parent_viewresult():
	sid=request.args['sid']
	data={}
	q="select * from result inner join subject using(subject_id) inner join student using(student_id) where student_id='%s'"%(sid)
	res=select(q)
	data['resu']=res
	return render_template('parent_viewresult.html',data=data)

@parent.route('/parent_viewnotice')
def parent_viewnotice():
	data={}
	q="select * from notice inner join student using (student_id)"
	res=select(q)
	data['not']=res

	return render_template('parent_viewnotice.html',data=data)
	
@parent.route('/parent_sendfeedback',methods=['post','get'])	
def parent_sendfeedback():
	data={}
	q="""SELECT feedback_id,user_id,feedback,`date`,reply,CONCAT (parent.fname,' ',parent.lname) AS puname FROM feedback INNER JOIN parent ON parent.login_id=feedback.user_id
	UNION
	SELECT feedback_id,user_id,feedback,DATE,reply,CONCAT(student.fname,' ',student.lname) AS suname FROM feedback INNER JOIN student ON student.login_id=feedback.user_id
	UNION 
	SELECT feedback_id,user_id,feedback,DATE,reply,CONCAT(staff.firstname,' ',staff.lastname) AS stname FROM feedback INNER JOIN staff ON staff.login_id=feedback.user_id"""
	res=select(q)
	print(q)
	data['feee']=res
	print(res)
	
	if "feedback" in request.form:
		lid=session['lid']
		f=request.form['fee']
		q="insert into feedback values(null,'%s','%s','pending',curdate())"%(lid,f)
		insert(q)
		flash('insert successfully');
		return redirect(url_for('parent.parent_sendfeedback',data=data))

		
	return render_template('parent_sendfeedback.html',data=data)
	
		

	

	
	

	