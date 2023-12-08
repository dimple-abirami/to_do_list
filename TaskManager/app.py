from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'b88fc9d4cd3d56ab8879d4d951c2e1cc0f8cc4265c0704a9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.debug = True
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database within the app context
with app.app_context():
    db.create_all()

# Routes to render templates
@app.route('/')
def index():
    tasks = Task.query.all()  
    return render_template('index.html', tasks=tasks)

from datetime import datetime

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        if title:
            new_task = Task(title=title)
            new_task.date = datetime.utcnow()  # Set the date here
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Title cannot be empty!', 'error')
    return render_template('add.html')



@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', task_id=task.id, title=task.title)

@app.route('/delete/<int:task_id>', methods=['GET', 'POST'])
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
