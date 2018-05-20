from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    added = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    hosts = db.relationship('Host', backref='hostcreator', lazy='dynamic')
    orgs = db.relationship('Organization', backref='orgcreator', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    host = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(255))
    sysuser = db.Column(db.String(64))
    port = db.Column(db.Integer)
    added = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    localforwards = db.relationship('HostLocalForward', backref='localforwards', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.hostname)


class HostLocalForward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'))
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(255))
    local_port = db.Column(db.Integer, index=True, unique=True)
    remote_port = db.Column(db.Integer)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    orgname = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(255))
    hosts = db.relationship('Host', backref='hostorg', lazy='dynamic')
    added = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.orgname)
