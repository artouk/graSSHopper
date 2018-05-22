from flask import render_template, redirect, url_for
from app import app, db
from app.forms import LoginForm, SignUpForm, NewHostForm, NewOrganizationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Host, Organization


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            #flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/hosts/new', methods=['GET', 'POST'])
@login_required
def new_host():
    orgs = [(o.id, o.orgname) for o in Organization.query.order_by('orgname')]
    form = NewHostForm()
    form.org_id.choices = orgs
    if form.validate_on_submit():
        o = Organization.query.get(form.org_id.data)
        h = Host(creator_id=current_user.id,
                 hostorg=o,
                 host=form.host.data,
                 address=form.address.data,
                 description=form.description.data,
                 sysuser=form.sysuser.data,
                 port=form.port.data)
        db.session.add(h)
        db.session.commit()
        return redirect(url_for('hosts'))
    return render_template('newhost.html', title='New Host', form=form)


@app.route('/hosts', methods=['GET', 'POST'])
@login_required
def hosts():
    hostlist = Host.query.join(Organization, Organization.id == Host.org_id).all()
    return render_template('hosts.html', title='Hosts', hosts=hostlist)


@app.route('/organizations/new', methods=['GET', 'POST'])
@login_required
def new_organization():
    form = NewOrganizationForm()
    if form.validate_on_submit():
        o = Organization(creator_id=current_user.id,
                 orgname=form.orgname.data,
                 description=form.description.data)
        db.session.add(o)
        db.session.commit()
        return redirect(url_for('organizations'))
    return render_template('neworg.html', title='New Organization', form=form)


@app.route('/organizations', methods=['GET', 'POST'])
@login_required
def organizations():
    orglist = Organization.query.all()
    return render_template('organizations.html', title='Organizations', orgs=orglist)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    hostlist = Host.query.all()
    return


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('signup_success'))
    return render_template('signup.html', title='Sign In', form=form)


@app.route('/signup/success', methods=['GET', 'POST'])
def signup_success():
    return render_template('signup_success.html')