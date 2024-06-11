from flask import Flask,Blueprint,render_template,request,redirect,url_for,session,flash
from database import*

public=Blueprint('public',__name__)

@public.route('/')
def publichome():
	return render_template('public_home.html')
@public.route('/public_login',methods=['post','get'])	
def public_login():
	if "login" in request.form:
		u=request.form['uname']
		p=request.form['pwd']
		q="select * from login where username='%s' and password='%s'"%(u,p)
		res=select(q)
		print(q)

		if res:
			session['lid']=res[0]['login_id']
			print(session['lid'])

			if res[0]['usertype']=="admin":
				return redirect(url_for('admin.admin_home'))

			elif res[0]['usertype']=="parent":
				return redirect(url_for('parent.parent_home'))
			elif res[0]['usertype']=="staff":

				q="select * from staff where login_id='%s'"%(session['lid'])
				res=select(q)
				if res:
					session['sid']=res[0]['staff_id']

				return redirect(url_for('staff.staff_home'))
			elif res[0]['usertype']=="student":
				q="select * from student where login_id='%s'"%(session['lid'])
				res=select(q)
				if res:
					session['stid']=res[0]['student_id']
				return redirect(url_for('student.student_home'))
			elif res[0]['usertype']=="parent":

				q="select * from parent where login_id='%s'"%(session['lid'])
				res=select(q)
				if res:
					session['ppid']=res[0]['parent_id']
					print(session['ppid'])


				return redirect(url_for('parent.parent_home'))
		else:

			flash('invalid username and password')	
				
				
					
	return render_template('public_login.html')
	
@public.route('/parent_registration',methods=['post','get'])
def parent_registration():
	if "registration" in request.form:
		f=request.form['fname']
		l=request.form['lname']
		p=request.form['place']
		ph=request.form['phone']
		e=request.form['email']
		u=request.form['uname']
		p=request.form['pwd']
		q="select * from login where username='%s' and password='%s'"%(u,p)
		res=select(q)
		if res:
			flash('already exist')
		else:
			
			q="insert into login values(null,'%s','%s','parent')"%(u,p)
			id=insert(q)
			q="insert into parent values(null,'%s','%s','%s','%s','%s','%s')"%(id,f,l,p,ph,e)
			insert(q)
			flash('insert successfully');
			return redirect(url_for('public.parent_registration'))

	return render_template('parent_registration.html')
			
	
	