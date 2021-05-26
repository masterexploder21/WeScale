import os

from cassiopeia import Queue, Champion
from flask import Flask, render_template, request

# Accessing data repository

# from data_repository import DataRepository
#
# key = os.getenv("AZURE_KEY")
# data_repository = DataRepository(database_name="we_scale",
#                                  endpoint_address="https://we-scale.documents.azure.com:443/",
#                                  private_access_key=key,
#                                  static_data_container_name="we_scale_static",
#                                  history_data_container_name="we_scale_history")
# print(data_repository.get_static_data())

# Acessing api service

from api_service import ApiService

riot_api_key = os.getenv("RIOT_API_KEY")
api_service = ApiService(riot_api_key=riot_api_key, settings={
    "version_from_match": "latest",
    "default_region": "EUNE"
})

app = Flask(__name__)


def get_queue_name(value):
    return value.name.capitalize().replace('_', ' ')


def get_champ_name(value, name):
    participant = next(filter(lambda x: x.summoner.name == name, value.participants))
    return participant.champion.name


def get_champ_image(value, name):
    participant = next(filter(lambda x: x.summoner.name == name, value.participants))
    return participant.champion.image.url


def get_stats(value, name):
    participant = next(filter(lambda x: x.summoner.name == name, value.participants))
    return f'{participant.stats.kills}/{participant.stats.deaths}/{participant.stats.assists}'


def get_cs(value, name):
    participant = next(filter(lambda x: x.summoner.name == name, value.participants))
    return participant.stats.total_minions_killed + participant.stats.neutral_minions_killed


app.jinja_env.filters['get_queue_name'] = get_queue_name
app.jinja_env.filters['get_champ_name'] = get_champ_name
app.jinja_env.filters['get_champ_image'] = get_champ_image
app.jinja_env.filters['get_stats'] = get_stats
app.jinja_env.filters['get_cs'] = get_cs


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/search', methods=["POST"])
def search():
    submitted_action = request.form.get("submit_button")
    summoner_name = request.form.get("summonerName")
    page = 0 if request.form.get("page") is None else int(request.form.get("page"))
    begin_index = 0
    end_index = 0

    if submitted_action == 'search':
        begin_index = 0
        end_index = 5
        page = 1
    elif submitted_action == 'search_next':
        begin_index = 5*page
        end_index = 5*page+5
        page += 1
    elif submitted_action == 'search_prev':
        begin_index = 5*page-5
        end_index = 5*page
        page -= 1

    matches_dict = api_service.get_match_list(name=summoner_name, begin_index=begin_index, end_index=end_index)

    return render_template('match_list.html', matches=matches_dict, summoner_name=summoner_name, page=page)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
