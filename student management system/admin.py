from flask import Flask,Blueprint,render_template,request,redirect,url_for,flash
from database import*

admin=Blueprint('admin',__name__)
@admin.route('/admin_home')
def admin_home():
	return render_template('admin_home.html')

@admin.route('/admin_managestaff',methods=['post','get'])	
def admin_managestaff():
	data={}
	q="select * from staff"
	res=select(q)
	data['stf']=res

	if "staffreg" in request.form:
		f=request.form['fname']
		l=request.form['lname']
		p=request.form['place']
		ph=request.form['phone']
		e=request.form['email']
		d=request.form['des']
		u=request.form['uname']
		p=request.form['pwd']

		q="select * from login where username='%s' and password='%s'"%(u,p)
		res=select(q)
		if res:
			flash('already exist')
		else:	
			
			q="insert into login values(null,'%s','%s','staff')"%(u,p)
			id=insert(q)

			q="insert into staff values(null,'%s','%s','%s','%s','%s','%s','%s')"%(id,f,l,p,ph,e,d)
			insert(q)

			flash('insert successfully');
			return redirect(url_for('admin.admin_managestaff'))

	if "action" in request.args:
		action=request.args['action']
		sid=request.args['sid']
	else:
		action=None

	if action=='delete':
		q="delete from staff where staff_id='%s'"%(sid)
		delete(q)
		flash('delete successfully');
		return redirect(url_for('admin.admin_managestaff'))

	if action=='update':
		q="select * from staff where staff_id='%s'"%(sid)
		res=select(q)
		data['up']=res
	if "update" in request.form:
		f=request.form['fname']
		l=request.form['lname']
		p=request.form['place']
		ph=request.form['phone']
		e=request.form['email']
		d=request.form['des']
		q="update staff set firstname='%s',lastname='%s',place='%s',phone='%s',email='%s',designation='%s' where staff_id='%s' "%(f,l,p,ph,e,d,sid)
		update(q)
		flash('update successfully');
		return redirect(url_for('admin.admin_managestaff'))

	return render_template('admin_managestaff.html',data=data)

@admin.route('/admin_viewstudents')
def admin_viewstudents():
	data={}
	q="SELECT *,`student`.login_id AS lid, student.fname AS sfname , student.lname AS slname,CONCAT(student.place)AS splace ,CONCAT (student.phone)AS sphone ,CONCAT (student.email) AS semail FROM student  inner join login using(login_id) INNER JOIN course USING(course_id) INNER JOIN parent USING(parent_id) "
	res=select(q)
	print(q)
	data['stu']=res

	if "action" in request.args:
		action=request.args['action']
		lid=request.args['lid']
		print(action)
	else:
		action=None

	if action=="accept":
		print("!!!!!!!!!!!!")
		q="update login set usertype='student' where login_id='%s'"%(lid)
		update(q)
		flash('update successfully');
		print(q)
		return redirect(url_for('admin.admin_viewstudents'))

	if action=="reject":
		q="update login set usertype='block' where login_id='%s'"%(lid)
		update(q)
		flash('update successfully');
		print(q)
		return redirect(url_for('admin.admin_viewstudents'))
				
	return render_template('admin_viewstudents.html',data=data)

@admin.route('/admin_managecourse',methods=['post','get'])	
def admin_managecourse():
	data={}
	q="select * from course"
	res=select(q)
	data['view']=res
	if "course" in request.form:
		c=request.form['cou']
		q="select * from course where course='%s'"%(c)
		res=select(q)
		if res:
			flash('already exist')
		else:
			q="insert into course values(null,'%s')"%(c)
			insert(q)
			flash('insert successfully');
			return redirect(url_for('admin.admin_managecourse'))

	if "action" in request.args:
		action=request.args['action']
		cid=request.args['cid']
	else:
		action=None
	if action=='delete':
		q="delete from course where course_id='%s'"%(cid)
		delete(q)
		flash('delete successfully');
		return redirect(url_for('admin.admin_managecourse'))

	if action=='update':
		q="select * from course where course_id='%s'"%(cid)
		res=select(q)
		data['up']=res
	if "update" in request.form:
		c=request.form['cou']
		q="update course set course='%s' where course_id='%s'"%(c,cid)
		update(q)
		flash('update successfully');
		return redirect(url_for('admin.admin_managecourse'))
				
	return render_template('admin_managecourse.html',data=data)

@admin.route('/admin_managesubject' ,methods=['post','get'])
def admin_managesubject():
	data={}
	q="select * from course"
	res=select(q)
	data['op']=res
	q="select * from subject inner join course using(course_id)"
	res=select(q)
	data['view']=res
	if "subject" in request.form:
		c=request.form['cou']
		s=request.form['sub']
		q="select * from subject where subject='%s' "%(s)
		res=select(q)
		if res:
			flash('already exist')
		else:
			
			q="insert into subject values(null,'%s','%s')"%(c,s)
			insert(q)
			flash('insert successfully');
			return redirect(url_for('admin.admin_managesubject'))

	if "action" in request.args:
		action=request.args['action']
		sid=request.args['sid']
	else:
		action=None
	if action=='delete':
		q="delete from subject where subject_id='%s'"%(sid)
		delete(q)
		flash('delete successfully');
		return redirect(url_for('admin.admin_managesubject'))

	if action=='update':
		q="select * from subject inner join course using(course_id) where subject_id='%s'"%(sid)
		res=select(q)
		data['up']=res

	if "update" in request.form:
		c=request.form['cou']
		s=request.form['sub']
		q="update subject set course_id='%s',subject='%s' where subject_id='%s'"%(c,s,sid)
		update(q)
		flash('update successfully');
			
		return redirect(url_for('admin.admin_managesubject'))

	return render_template('admin_managesubject.html',data=data)

@admin.route('/admin_viewfeedback')	
def admin_viewfeedback():
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

	return render_template('admin_viewfeedback.html',data=data)

@admin.route('admin_viewleave')	
def admin_viewleave():
	data={}
	q="SELECT * FROM `leave`"
	res=select(q)
	data['le']=res
	return render_template('admin_viewleave.html',data=data)

@admin.route('admin_viewattendance')
def admin_viewattendance():
	s=request.args['sid']
	data={}
	q="select * from attendance inner join student using (student_id) where student_id='%s' "%(s)
	res=select(q)
	data['atten']=res
	return render_template('admin_viewattendance.html',data=data)

@admin.route('admin_viewparent')	
def admin_viewparent():
	p=request.args['pid']
	data={}
	q="select * from parent where parent_id='%s'"%(p)
	res=select(q)
	data['par']=res

	return render_template('admin_viewparent.html',data=data)

@admin.route('admin_sendreply',methods=['post','get'])	
def admin_sendreply():
	

	if "reply" in request.form:
		f=request.args['fid']
		r=request.form['rep']
		q="update feedback set reply='%s'  where feedback_id='%s'"%(r,f)
		update(q)
		flash('update successfully');
		return redirect(url_for('admin.admin_viewfeedback'))
	return render_template('admin_sendreply.html')
			
	
	
	

			

	