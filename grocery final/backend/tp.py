'''
@app.route("/userfirstpg")
def userfirstpg():
    return render_template('userfirstpg.html')
'''
'''
@app.route("/user")
def user():
    return render_template('user.html')
'''

class user_pass(db.Model):
    __tablename__ = 'user_pass'
    sr = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(120))
    
    def __repr__(self):
        return '<user_pass %r>' % self.sr


# Function to add a new user to the database
def add_user(username, password):
    try:
        new_user = user_pass(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        print("Error adding user:", e)
        db.session.rollback()
        return False


# Route for the sign-in page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    logged_in = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the submitted username exists in the database
        user = user_pass.query.filter_by(username=username).first()
        # If the user exists and the password matches, set logged_in to True
        if user and user.password == password:
            logged_in = True
    return render_template('signin.html', logged_in=logged_in)

'''
# Route for the login page
@app.route('/user')
def user():
    return render_template('user.html')




# Dummy route for logging out (replace this with your actual logout logic)
@app.route('/logout')
def logout():
    # Clear the session or perform any other logout actions
    return render_template('logout.html')
'''
