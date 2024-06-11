from flask import Flask,Blueprint,render_template,request,url_for,session,redirect,flash
from database import*

staff=Blueprint('staff',__name__)
@staff.route('/staff_home')
def staff_home():
	return render_template('staff_home.html')

@staff.route('staff_viewstudent')
def staff_viewstudent():
	data={}
	q="select *,CONCAT(student.fname)AS sfname ,CONCAT(student.lname) AS slname,CONCAT(student.place)AS splace ,CONCAT (student.phone)AS sphone ,CONCAT (student.email) AS semail from student inner join parent using (parent_id) inner join course using (course_id)"
	res=select(q)
	data['view']=res
	return render_template('staff_viewstudent.html',data=data)	

@staff.route('staff_applyleave',methods=['post','get'])
def staff_applyleave():
	if "leave" in request.form:
		sid=session['lid']
		d=request.form['date']
		s=request.form['status']
		q="insert into `leave` values(null,'%s','staff','%s','%s')"%(sid,d,s)
		insert(q)
		flash('insert successfully');
		return redirect(url_for('staff.staff_applyleave'))

		
	return render_template('staff_applyleave.html')

@staff.route('staff_sendfeedback',methods=['post','get'])	
def staff_sendfeedback():
	data={}
	q="""  
	SELECT feedback_id,user_id,feedback,`date`,reply,CONCAT (parent.fname,' ',parent.lname) AS puname FROM feedback INNER JOIN parent ON parent.login_id=feedback.user_id
	UNION
	SELECT feedback_id,user_id,feedback,DATE,reply,CONCAT(student.fname,' ',student.lname) AS suname FROM feedback INNER JOIN student ON student.login_id=feedback.user_id
	UNION 
	SELECT feedback_id,user_id,feedback,DATE,reply,CONCAT(staff.firstname,' ',staff.lastname) AS stname FROM feedback INNER JOIN staff ON staff.login_id=feedback.user_id    """
	res=select(q)
	data['feee']=res

	if "feedback" in request.form:
		sid=session['lid']
		f=request.form['fee']
		q="insert into feedback  values(null,'%s','%s','pending',curdate())"%(sid,f)
		insert(q)
		flash('insert successfully');
		return redirect(url_for('staff.staff_sendfeedback'))
		
	return render_template('staff_sendfeedback.html',data=data)

@staff.route('staff_addattendance',methods=['post','get'])	
def staff_addattendance():
	
	data={}
	s=request.args['sid']
	q="select * from attendance inner join student using (student_id) where student_id='%s'"%(s)
	res=select(q)
	data['attendance']=res
	
	if "attendance" in request.form:
		s=request.args['sid']
		a=request.form['att']
		q="insert into attendance values(null,'%s','%s',curdate())"%(s,a)
		insert(q)
		flash('insert successfully');
		return redirect(url_for('staff.staff_addattendance',sid=sid))
		
	return render_template('staff_addattendance.html',data=data)

@staff.route('staff_addresult',methods=['post','get'])	
def staff_addresult():
	data={}
	s=request.args['sid']
	q="select * from subject "
	res=select(q)
	data['subject']=res

	q="select * from result inner join student using(student_id) inner join subject using (subject_id) where student_id='%s'"%(s)
	res=select(q)
	data['result']=res

	if "result" in request.form:
		s=request.form['sub']
		sid=request.args['sid']
		q="insert into result values(null,'%s','%s')"%(s,sid)
		insert(q)
		return redirect(url_for('staff.staff_addresult',sid=sid))
		
	return render_template('staff_addresult.html',data=data)

@staff.route('staff_addnotice',methods=['post','get'])
def staff_addnotice():
	data={}
	s=request.args['sid']
	q="select * from notice inner join student using (student_id) where student_id='%s'"%(s)
	res=select(q)
	data['notice']=res

	if "notice" in request.form:
		s=request.args['sid']
		n=request.form['not']
		q="insert into notice values(null,'%s','%s')"%(s,n)
		insert(q)
		return redirect(url_for('staff.staff_addnotice'))
		
	return render_template('staff_addnotice.html',data=data)
		
	
	
	

		
