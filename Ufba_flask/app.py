from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/goesp/Vs_codes/Search_UFBA/Ufba_flask/data/db.sqlite3?charset=iso-8859-1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


collegiate_week_subject = db.Table( 
    "association_week_colegiate",
    db.Column('Collegiate_row_id', db.Integer, db.ForeignKey('Collegiate.Row_id')),
    db.Column('week_subject_id', db.Integer, db.ForeignKey('Week_subject.Subject_id'))
)


class Collegiate(db.Model):
    __tablename__ = 'Collegiate'
    row_id = db.Column("Row_id", db.Integer, primary_key=True)
    collegiate = db.Column("Collegiate", db.Integer)
    subject = db.Column('Subject', db.String)
    classes = db.Column('Classroom', db.Integer)
    offered = db.Column('Offered', db.Integer)
    demand = db.Column('Demand', db.Integer)
    available = db.Column('Available', db.Integer)
    week = db.relationship('Week_subject', secondary=collegiate_week_subject, backref='demand_offert')
    
    def __repr__(self):
        return f'Row ID: {self.row_id}, Collegiate: {self.collegiate}, Subject: {self.subject}, Class: {self.classes}'


class Week_subject(db.Model):
    __tablename__ = 'Week_subject'
    id = db.Column('Subject_id', db.Integer, primary_key=True)
    code = db.Column('Subject', db.String)
    subject_name = db.Column('Subject_name', db.String)
    classes = db.Column('Classes', db.String)
    day_of_week = db.Column('Day_of_week', db.String)
    schedule = db.Column('Schedule', db.String)
    professor = db.Column('Professor', db.String)

    def __repr__(self):
        return f'<id: {self.id}> <code: {self.code}> <subject_name: {self.subject_name}> <classes: {self.classes}> <day_of_week: {self.day_of_week}> <schedule: {self.schedule}> <professor:  {self.professor}>'



@app.route('/search', methods=['POST', 'GET'])
def search_data_subject():
    if request.method == 'POST':
        subject_search = request.form['subject'].upper()
        return redirect(url_for('show_data_subject', subject_in_box=subject_search))
    elif request.method == 'GET':
        return render_template(r'base.html')

        


@app.route('/search/<string:subject_in_box>', methods=['POST', 'GET'])
def show_data_subject(subject_in_box):
    if request.method == 'POST':
        subject_in_box = request.form['subject'].upper()
        search_by_subject = Collegiate.query.filter_by(subject=subject_in_box).order_by(Collegiate.available.desc()).all()
        return render_template(r'show_data.html', data=search_by_subject, subject_search=subject_in_box)
    elif request.method == 'GET':
        search_by_subject = Collegiate.query.filter_by(subject=subject_in_box).order_by(Collegiate.available.desc()).all()
        return render_template(r'show_data.html', data=search_by_subject, subject_search=subject_in_box)


@app.route('/search/<string:subject_in_box>/<int:row_id>')
def modal_popup(row_id, subject_in_box):
    search_by_subject = Collegiate.query.filter_by(subject=subject_in_box).order_by(Collegiate.available.desc()).all()
    row_selected = Collegiate.query.filter_by(row_id=row_id).first()
    return render_template('modal.html', data=search_by_subject, subject_search=subject_in_box, row_selected=row_selected)
    
if __name__ == '__main__':
    app.run(debug=True)
