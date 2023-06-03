from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
# initialize the app with the extension
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    desc = db.Column(db.String(500))
    time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"

#db.init_app(app)
@app.route('/', methods=['GET','POST'])
def home():
    if request.method =='POST':
        todo_title = request.form['title']
        desc_todo = request.form['desc']
        data = Todo(title = todo_title, desc=desc_todo)
        db.session.add(data)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == 'POST':
        todo_title = request.form['title']
        desc_todo = request.form['desc']
        data = Todo.query.filter_by(sno=sno).first()
        data.title = todo_title
        data.desc = desc_todo
        db.session.add(data)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    #print(todo)
    db.session.delete(todo)
    db.session.commit()
    
    return redirect("/")



if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)