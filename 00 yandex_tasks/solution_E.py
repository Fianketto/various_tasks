import sqlite3


params = []
for i in range(4):
    params.append(input().strip())

database, condition1, condition2, order_col = params

connection = sqlite3.connect(database)
cursor = connection.cursor()
sql_req = f"SELECT condition FROM Talks WHERE {condition1} AND {condition2} order by {order_col}"
cursor.execute(sql_req)
rows = cursor.fetchall()

for row in rows:
    print(row[0])

'''
conversations.db
1 = 1
1 = 1
id

discussion.db
suitable = 1
level_of_trust > 10
author
'''
