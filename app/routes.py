from flask import render_template, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, SignUpForm, NewHostForm, NewOrganizationForm, UserSettingsForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Host, Organization, UserSettings


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
    user_settings = UserSettings.query.filter(UserSettings.user_id == current_user.id).first()
    form = UserSettingsForm()
    proxy_hosts = [(h.id, h.host) for h in Host.query.order_by('host')]
    form.proxy_host.choices = proxy_hosts

    if form.validate_on_submit():
        user_settings.default_sys_username = form.default_sys_username.data
        user_settings.force_proxy = form.force_proxy.data
        user_settings.proxy_host = form.proxy_host.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.default_sys_username.data = user_settings.default_sys_username
        form.force_proxy.data = user_settings.force_proxy
        form.proxy_host.data = user_settings.proxy_host

    return render_template('settings.html', title='User Settings', form=form)


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
        user = User.query.filter(User.username == form.username.data).first()
        user_settings = UserSettings(user=user)
        db.session.add(user_settings)
        db.session.commit()
        return redirect(url_for('signup_success'))
    return render_template('signup.html', title='Sign In', form=form)


@app.route('/signup/success', methods=['GET', 'POST'])
def signup_success():
    return render_template('signup_success.html')


@app.route('/build', methods=['GET'])
@login_required
def build():
    hosts = Host.query.order_by('host')
    return render_template('config', hosts=hosts)