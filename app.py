import os

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


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/search', methods=["POST"])
def search():
    summonerName = request.form.get("summonerName")
    summoner = api_service.get_summoner(summonerName)
    return render_template('match_list.html', summoner=summoner)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')
