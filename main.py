from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL()])
    opening = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffeeR = SelectField('Coffee Rating',choices=[('☕'),('☕☕'),('☕☕☕'),('☕☕☕☕'),('☕☕☕☕☕☕')])
    wifiR = SelectField('Wifi Rating', choices=[('✘'), ('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪')])
    powerR = SelectField('Power Socket Availability', choices=[('✘'), ('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌')])
    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open('cafe-data.csv',mode='a',newline='',encoding='utf-8') as csv_file:
            csv_file.write(f"{form.cafe.data},{form.location.data},{form.opening.data},{form.closing.data}"
                           f"{form.coffeeR.data},{form.wifiR.data},{form.powerR.data}")
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
