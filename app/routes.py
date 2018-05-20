from flask import render_template, redirect, url_for
from app import app, db
from app.forms import LoginForm, NewHost, NewOrganization
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Host, Organization

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=current_user, posts=posts)


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
    form = NewHost()
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
    form = NewOrganization()
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
