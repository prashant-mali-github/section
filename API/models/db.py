
from app import db

class Sections(db.Model):
    __tablename__='sections'
    section_id = db.Column(db.Integer,primary_key=True)
    section_title = db.Column(db.String(255),nullable=False)
    section_description = db.Column(db.String(255),nullable=False)
    is_active = db.Column(db.Boolean)
    operations = db.relationship("Operations",backref=db.backref("sections"))

    def __init__(self,section_title, section_description, is_active):
        self.section_title = section_title
        self.section_description = section_description
        self.is_active = is_active


class Operations(db.Model):

    __tablename__='operations'
    operation_id = db.Column(db.Integer,primary_key=True)
    section_id = db.Column(db.Integer(), db.ForeignKey('sections.section_id', ondelete='CASCADE'))
    operation_title = db.Column(db.String(255), nullable=False)
    operation_description = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean)


    def __init__(self,section_id,
        operation_title, operation_description, is_active):
        self.section_id = section_id
        self.operation_title = operation_title
        self.operation_description = operation_description
        self.is_active = is_active

class RoleConfig(db.Model):
    __tablename__='roleconfig'
    role_config_id = db.Column(db.Integer,primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.role_id', ondelete='CASCADE'))
    operation_id = db.Column(db.Integer(), db.ForeignKey('operations.operation_id', ondelete='CASCADE'))
    is_active = db.Column(db.Boolean)
    role = db.relationship("Roles",backref=db.backref("roleconfig"))
    operation = db.relationship("Operations",backref=db.backref("roles"))

    def __init__(self, role_id,
        operation_id, is_active):
        self.role_id = role_id
        self.operation_id = operation_id
        self.is_active = is_active

class Roles(db.Model):
    __tablename__='roles'
    role_id = db.Column(db.Integer,primary_key=True)
    role_title = db.Column(db.String(255),nullable=False)
    role_description = db.Column(db.String(255),nullable=False)
    is_active = db.Column(db.Boolean)

    def __init__(self,role_title,
        role_description, is_active):
        self.role_title = role_title
        self.role_description = role_description
        self.is_active = is_active
