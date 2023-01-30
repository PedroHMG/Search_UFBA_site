from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base


app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/goesp/Vs_codes/Search_UFBA/Ufba_flask/data/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Collegiate(db.Model):
    row_id = db.Column("Row_id", db.Integer, primary_key=True)
    collegiate = db.Column("Collegiate", db.Integer)
    subject = db.Column('Subject', db.String)
    classes = db.Column('Classroom', db.Integer)
    offered = db.Column('Offered', db.Integer)
    demand = db.Column('Demand', db.Integer)
    available = db.Column('Available', db.Integer)

    def __repr__(self):
        return f'Row ID: {self.row_id}, Collegiate: {self.collegiate}, Subject: {self.subject}, Class: {self.classes}'


@app.route('/search', methods=['POST', 'GET'])
def search_data_subject():
    if request.method == 'POST':
        subject_search = request.form['subject'].upper()
        search_by_subject = Collegiate.query.filter_by(subject=subject_search).order_by(Collegiate.available.desc()).all()
        return render_template(r'search_data/show_data.html', data=search_by_subject)
    elif request.method == 'GET':
        return render_template(r'search_data/show_data.html')

    
if __name__ == '__main__':
    app.run(debug=True)
