from flask import Flask,Blueprint,render_template,request,session,redirect,url_for,flash
from database import*

student=Blueprint('student',__name__)

@student.route('/student_home')
def student_home():
	return render_template('student_home.html')
@student.route('/student_viewcourse')
def student_viewcourse():
	data={}
	q="select * from course "
	res=select(q)
	data['cou']=res

	return render_template('student_viewcourse.html',data=data)

@student.route('student_viewsubject')	
def student_viewsubject():
	cid=request.args['cid']
	data={}
	q="select * from subject inner join course using (course_id) where course_id='%s'"%(cid)
	res=select(q)
	data['sub']=res
	return render_template('student_viewsubject.html',data=data)

@student.route('student_viewattendence')
def student_viewattendence():

	data={}
	q="select * from attendance inner join student using(student_id)"
	res=select(q)
	data['att']=res

	return render_template('student_viewattendence.html',data=data)

@student.route('student_viewresult')
def student_viewresult():
	data={}
	q="select * from result inner join subject using (subject_id) inner join student using(student_id)"
	res=select(q)
	data['resl']=res
	return render_template('student_viewresult.html',data=data)

@student.route('student_applyleave',methods=['post','get'])
def student_applyleave():
	if "leave" in request.form:
		stid=session['lid']
		d=request.form['date']
		s=request.form['status']
		q="insert into `leave` values(null,'%s','student','%s','%s')"%(stid,d,s)
		insert(q)
		flash('insert successfully');
		return redirect(url_for('student.student_applyleave'))

		
	return render_template('student_applyleave.html')
	
@student.route('student_sendfeedback',methods=['post','get'])
def student_sendfeedback():
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
		stid=session['lid']
		f=request.form['fee']
		q="insert into feedback  values(null,'%s','%s','pending',curdate())"%(stid,f)
		insert(q)
		flash('insert successfully');
		return redirect(url_for('student.student_sendfeedback'))
	return render_template('student_sendfeedback.html',data=data)
			
			
		
		
	
			
	