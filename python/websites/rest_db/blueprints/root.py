from flask import Blueprint, render_template, session, request, redirect
from data import (
    create_table,
    create_user,
    delete_table,
    write_to_table,
    remove_user,
    user,
    get_users
)

from encryption import check_hash

from markdown import markdown

bp = Blueprint(
    name="rt",
    import_name=__name__,
    template_folder="../root"
)

# functions
def key(jd,kn):
    try:
        rs = jd[kn]
    except KeyError:
        return None
    return rs

# content

@bp.route('/')
def index():
    # show the markdown document in HTML format
    user_validated = False
    if key(session, 'validated') == True:
        print("User validated!")
        user_validated = True
    
    u = user(get_users(), key(session, 'email_unencoded'))
    print("USER EMAIL: %s" % session.get('email_unencoded'))
    
    if not u:
        user_validated = False # turn it back to False if their account doesn't exist.
    
    return str(markdown(open('./readme.md','r').read()) + (f'<br/><p>OOH! Looks like you have been validated and logged in. Your information:</p><p>UID: {u[0]}</p><p>First Name: {u[1]}</p><p>Last Name: {u[2]}</p><p>E-mail: {u[3]}</p><p>PW Hash: {u[4]}</p><a href="/account/delete"><button>Delete my Account</button></a>' if user_validated else ''))

@bp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = key(request.form, 'email')
        pw = key(request.form, 'password')
        
        # do some SQLite3 stuff here:
        u = user(get_users(), email=email)
        correct_info = False
        print(u)
        if u:
            print("User exists.")
            if check_hash(pw.encode(), u[4].encode()):
                print("Password correct.")
                correct_info = True
            else:
                print("Password incorrect.")
                correct_info = False
        else:
            return redirect('/login?code=%s' % "email or password is incorrect.")

        if not correct_info:
            return redirect('/login?code=%s' % "email or password is incorrect.")
        
        # session data:
        
        session["uid"] = str(u[0])
        session["name"] = f"{u[1]} {u[2]}"
        session["email"] = str(u[3])
        session["email_unencoded"] = str(email)
        session["validated"] = True
        
        # and finally redirect:
        return redirect('/')
    else:
        return render_template('login.html')

@bp.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = key(request.form, 'email')
        pw = key(request.form, 'password')
        fn = key(request.form, 'firstname')
        ln = key(request.form, 'lastname')
        
        # do some SQLite3 stuff here:
        u = user(get_users(), email=email)
        correct_info = False
        print(u)
        if u:
            print("User exists.")
            return redirect('/register?code=%s' % "account with the following details already exists.")
        else:
            correct_info = True

        if not correct_info:
            return redirect('/register?code=%s' % "account with the following details already exists.")
        
        # create the user
        uid = create_user(email, pw, fn, ln)
        
        # session data:
        
        session["uid"] = uid
        session["name"] = f"{fn} {ln}"
        session["email"] = str(email)
        session["validated"] = True
        
        # and finally redirect:
        return redirect('/')
    else:
        return render_template('register.html')

@bp.route('/whoami')
@bp.route('/whoami/')
def whoami():
    return "Hello, you are " + str(session.get('name')) + "."

@bp.route('/users/')
@bp.route('/users')
def userlistall():
    return str(get_users())

@bp.route('/account/delete')
@bp.route('/account/delete/')
def userdelete():
    # get user id from storage
    is_validated = key(session, 'validated')
    uid = key(session, 'uid')
    email = key(session, 'email_unencoded')
    u = user(get_users(), email)
    
    if not u:
        print("Account doesn't exist.")
        return "You are not allowed to access this action."
    
    if is_validated and u:
        if str(u[0]) == str(uid):
            # delete the account.
            print("Deleting the account: {} {}".format(uid, email))
            remove_user(uid)
            session.clear()
            return "Your account has been deleted and you were signed out. <a href='/'>Back to Home Page</a>"

        else:
            print("Account session isn't valid.")
            return "You are not allowed to access this action."
    else:
        print("Account session isn't valid.")
        return "You are not allowed to access this action."