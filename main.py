import requests
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

api_key = 'k_ynnm9x00'
url = 'https://imdb-api.com/en/API'

options = ['None', 'Search', 'SearchTitle', 'SearchMovie', 'SearchSeries', 'SearchName', 'SearchEpisode', 'SearchCompany',
           'SearchKeyword', 'SearchAll']
options2 = ['None', 'Top250Movies', 'Top250TVs', 'MostPopularMovies', 'MostPopularTVs', 'InTheaters', 'ComingSoon', 'BoxOffice',
            'BoxOfficeAllTime']


class Search(FlaskForm):
    option = SelectField('Type of Search', choices=options, validators=[DataRequired()])
    search = StringField('Search Word', validators=[DataRequired()])
    submit = SubmitField("Search")


class Other(FlaskForm):
    option = SelectField("Type of Search", choices=options2, validators=[DataRequired()])
    submit = SubmitField("Search")


app = Flask(__name__)
app.config['SECRET_KEY'] = "TopSecret"
Bootstrap(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/SearchAPIs', methods=['GET', 'POST'])
def search():
    form = Search()
    if form.validate_on_submit():
        if form.option.data == "None":
            flash("You need to choose an option.")
            return redirect(url_for('search'))
        response = requests.get(url=f"{url}/{form.option.data}/{api_key}/{form.search.data}")
        response.raise_for_status()
        data = [response.json()['results'][0]]
        return render_template("search_result.html", data=data)
    return render_template("search.html", form=form)


@app.route('/OtherAPIs', methods=['GET', 'POST'])
def other():
    form = Other()
    if form.validate_on_submit():
        if form.option.data == "None":
            flash("You need to choose an option.")
            return redirect(url_for('other'))
        response = requests.get(url=f"{url}/{form.option.data}/{api_key}")
        response.raise_for_status()
        data = response.json()['items']
        return render_template("search_result.html", data=data)
    return render_template("search.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5004)
