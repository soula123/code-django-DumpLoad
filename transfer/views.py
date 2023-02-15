from django.shortcuts import render
# views.py
from django.shortcuts import render, redirect
import mysql.connector
import json
from django.http import JsonResponse, HttpResponse

def copy_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        source_db = data['source_db']
        target_db = data['target_db']

        source_conn = mysql.connector.connect(
            user=source_db['user'],
            password=source_db['password'],
            host=source_db['host'],
            database=source_db['database']
        )

        target_conn = mysql.connector.connect(
            user=target_db['user'],
            password=target_db['password'],
            host=target_db['host'],
            database=target_db['database']
        )

        source_cursor = source_conn.cursor()
        target_cursor = target_conn.cursor()

        source_cursor.execute("SHOW TABLES")
        tables = [row[0] for row in source_cursor.fetchall()]

        for table in tables:
            source_cursor.execute(f"SELECT * FROM {table}")
            rows = source_cursor.fetchall()

            target_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (LIKE {table} INCLUDING ALL)")

            for row in rows:
                target_cursor.execute(f"INSERT INTO {table} VALUES {row}")
                target_conn.commit()

        source_conn.close()
        target_conn.close()

        return JsonResponse({"message": "Data copied successfully"})

# urls.py

