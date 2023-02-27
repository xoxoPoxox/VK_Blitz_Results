from flask import Flask
import pandas as pd
import pretty_html_table
import requests
app = Flask(__name__)

@app.route("/<int:game_id>")
def results(game_id):
    return getResults(game_id)
def getResults(game_id):
    results = requests.get('https://ma.martin-vk.ru/api/getResults/?game_id=' + str(game_id), auth=('user', 'pass')).json()
    title = requests.get('https://ma.martin-vk.ru/api/getGameTitle/?game_id=' + str(game_id), auth=('user', 'pass')).json()
    k = 1
    for x in results:
        x['#'] = x.pop('user_id')
        x['Имя'] = requests.get('https://ma.martin-vk.ru/api/getUserName/?user_id=' + str(x['#']), auth=('user', 'pass')).json()['fullName']
        x['Место'] = k
        k += 1
        x['Баллы'] = x.pop('points')
        x['Правильные ответы'] = x.pop('corrects')
    df = pd.DataFrame.from_dict(results)
    html = f"<h1 style = \"font-family: Century Gothic, sans-serif;color: #305496;\">{title['title']}</h1><h2 style = \"font-family: Century Gothic, sans-serif;color: #305496;\">Тестирование №{game_id}</h2>"
    html += pretty_html_table.build_table(df, 'blue_light', text_align='center',  width_dict=['20%', '20%', '20%', '20%', '20%'])
    return html