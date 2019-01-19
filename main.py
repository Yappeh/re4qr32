from flask import Flask, render_template, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, validators, FileField
from flask_uploads import UploadSet, configure_uploads, IMAGES


Base = declarative_base()
app = Flask(__name__)
app.secret_key = 'secret'


class BusinessInfo(Base):
    __tablename__ = "business"

    id = Column('id', Integer, primary_key=True)
    company = Column('company', String)
    companyDesc = Column('companyDesc', String)
    locationName = Column('locationName', String)
    address = Column('address', String)
    hotline = Column('hotline', Integer)
    email = Column('email', String)
    website = Column('website', String)
    operatingHours = Column('operatingHours', String)

    def __init__(self,company, companyDesc, locationName, address, hotline, email, website, operatingHours):

        self.company = company
        self.companyDesc = companyDesc
        self.locationName = locationName
        self.address = address
        self.hotline = hotline
        self.email = email
        self.website = website
        self.operatingHours = operatingHours


    def get_company(self):
        return self.company

    def get_desc(self):
        return self.companyDesc

    def get_location(self):
        return self.locationName

    def get_address(self):
        return self.address

    def get_hotline(self):
        return self.hotline

    def get_email(self):
        return self.email

    def get_website(self):
        return self.website

    def get_operating(self):
        return self.operatingHours


engine = create_engine('sqlite:///business.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
list = []


def matchdb_retrieve():
    global list
    list.clear()
    session = Session()
    business = session.query(BusinessInfo).all()
    for businesses in business:
        list.append(businesses)
    session.close()
    return len(list)





class RegisterForm(FlaskForm):
    image = FileField("Display Picture :", [validators.Required])
    company = StringField('Business Name :', [
        validators.Length(min=1, max=50),
        validators.Required()
    ])
    companyDesc = TextAreaField('Business Description :', [validators.Length(min=1, max=500), validators.Required()])
    locationName = StringField('Location Name :', [validators.Length(min=3, max=100), validators.Required()])
    address = StringField('Address :', [validators.Length(min=3, max=100), validators.Required()])
    hotline = IntegerField('Hotline :', [validators.Length(min=8, max=50), validators.Required()])
    email = StringField('Business E-mail :', [validators.Length(min=6, max=50), validators.Required()])
    website = StringField('Website URL(Optional) :')
    operatingHours = TextAreaField('Operating Hours :', [validators.Required()])
    submit = SubmitField("Create Business")


# class Business(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     filename = db.Column(db.String(500), nullable=False)
#     company = db.Column(db.String(50), nullable=False)
#     companyDesc = db.Column(db.String(500), nullable=False)
#     location = db.Column(db.String(50), nullable=False)
#     address = db.Column(db.String(100),nullable=False)
#
#     hotline = db.Column(db.String(10), nullable=True, unique=True)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     website = db.Column(db.String(100), nullable=True, unique=True)
#
#     operatingHours = db.Column(db.String(100), nullable=False)
#
#     posts = db.relationship('Posts', backref='owner')


# class Posts(db.Model):
#     id = db.Column(db.Integer, nullable=False, primary_key=True)
#     postHead = db.Column(db.String(1500), nullable=False)
#     postDesc = db.Column(db.String(1500), nullable=False)
#     owner_id = db.Column(db.Integer, db.ForeignKey('business.id'))


@app.route("/")
def main():
    return "Hello World!"


@app.route('/register', methods=['GET', 'POST'])
def form():
    form = RegisterForm(request.form)

    if request.method == 'POST':
        if form.validate() and 'photo' in request.files:
            name = form.company.data
            desc = form.companyDesc.data
            location = form.locationName.data
            address = form.address.data
            hotline = form.hotline.data
            email = form.email.data
            website = form.website.data
            operatingHours = form.operatingHours.data

            session = Session()

            session.add(BusinessInfo( name, desc, location, address, hotline, email, website, operatingHours))
            session.commit()
            session.close
            return render_template('addBusiness.html', form=form)
        else:
            flash('All fields are required.')
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('addBusiness.html', form=form)


@app.route("/<name>")
def business(name):
    global list
    listlen = matchdb_retrieve()
    return render_template('businessProf.html', name=name, list=list, id=id, listlen=listlen)


if __name__ == "__main__":
    app.run(debug=True)