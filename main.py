import csv

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


def time_validator(form, field):
    if field.data[-2:] != 'AM' and field.data[-2:] != 'PM':
        raise ValueError('Supposed to be AM or PM after the number')


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[DataRequired(), URL()])
    open_time = StringField('Open time e.g. 8AM', validators=[DataRequired(), time_validator])
    close_time = StringField('Close time e.g. 9PM', validators=[DataRequired(), time_validator])
    coffee = SelectField('Coffee level', validators=[DataRequired()], choices=['✘', '☕️', '☕️☕️', '☕️☕️☕️',
                                                                               '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'])
    wifi = SelectField('Wi-Fi level', validators=[DataRequired()], choices=['✘', '💪', '💪💪', '💪💪💪',
                                                                            '💪💪💪💪', '💪💪💪💪💪'])
    power = SelectField('Power level', validators=[DataRequired()], choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌',
                                                                             '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding='utf-8') as file:
            file.write(f"\n{form.cafe.data},"
                       f"{form.location.data},"
                       f"{form.open_time.data},"
                       f"{form.close_time.data},"
                       f"{form.coffee.data},"
                       f"{form.wifi.data},"
                       f"{form.power.data}")
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
