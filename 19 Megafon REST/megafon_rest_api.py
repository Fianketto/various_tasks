from flask import Flask, jsonify
from megafon_sqlite import *

app = Flask(__name__)


@app.route("/users/<int:user_id>")
def get_user_info(user_id):
    """Получение агрегированных данных по абоненту {user_id}"""
    rows = select_user_ids(connection)
    user_ids = [row[0] for row in rows]
    if user_id not in user_ids:
        return f'No user with id {user_id}', 404
    df_gr_user = df_gr[df_gr['user_id'] == user_id]
    df_gr_user = df_gr_user[['day', 'serv_01_vol', 'serv_02_vol', 'serv_03_vol']]
    df_gr_user.rename(columns={'day': 'Дата',
                               'serv_01_vol': 'Потрачено минут',
                               'serv_02_vol': 'Потрачено смс',
                               'serv_03_vol': 'Потрачено трафика'},
                      inplace=True)
    resp_data = {'Абонент': user_id, "Данные": df_gr_user.to_dict('records')}
    return jsonify(resp_data)


app.run(debug=True)
