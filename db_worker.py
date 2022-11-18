from sqlalchemy import create_engine, text, select
from datetime import date
from time import time

engine = create_engine('sqlite:///db_2.sqlite')


def listcat(tuser_id):
    s = text('SELECT cat_name FROM category WHERE tuser_id == :tuser_id')
    d = {'tuser_id': tuser_id}
    cat_list = []
    with engine.begin() as conn:
        for row in conn.execute(s, d):
            cat_list.append(row[0])
    return cat_list


def setcat(cat_name, tuser_id):
    # first we get the list of existing categories to check if user tries to set already existing category
    cat_list = listcat(tuser_id)
    if cat_name not in cat_list:
        s = text('INSERT INTO category (cat_name, tuser_id) VALUES (:cat_name, :tuser_id)')
        d = {'cat_name': cat_name, 'tuser_id': tuser_id}
        with engine.begin() as conn:
            conn.execute(s, d)
        return True
    else:
        return False


# TODO when you delete cat the records of it should be also deleted from time_track
def delcat(cat_name, tuser_id):
    cat_list = listcat(tuser_id)
    if cat_name in cat_list:
        s = text('DELETE FROM category WHERE cat_name == :cat_name AND tuser_id == :tuser_id')
        d = {'cat_name': cat_name, 'tuser_id': tuser_id}
        with engine.begin() as conn:
            conn.execute(s, d)
        return f'{cat_name} deleted'
    else:
        return 'There is no such category.\nUse /list to see all your categories.'


def startcat(cat_name, tuser_id):
    # first we get cat_id from category table. Probably it can be done in one statement together with the next one
    s = text('SELECT id FROM category WHERE cat_name == :cat_name AND tuser_id == :tuser_id')
    d = {'cat_name': cat_name, 'tuser_id': tuser_id}
    with engine.begin() as conn:
        for row in conn.execute(s, d):
            cat_id = row[0]
    # now we write the start time
    if cat_id:
        s = text('INSERT INTO time_track (cat_id, start_date, start_time) VALUES (:cat_id, :start_date, :start_time)')
        d = {'cat_id': cat_id, 'start_date': date.today(), 'start_time': time()}
        with engine.begin() as conn:
            conn.execute(s, d)
        return f'{cat_name} started. To stop it use\n\n/end {cat_name}'
    else:
        return 'No such category. Use /list to see all your categories.'


def stopcat(cat_name, tuser_id):
    stop_time = time()
    # first we get id of the category we want to stop
    s = text('SELECT id FROM category WHERE cat_name==:cat_name AND tuser_id==:tuser_id')
    d = {'cat_name': cat_name, 'tuser_id': tuser_id}
    with engine.begin() as conn:
        for row in conn.execute(s, d):
            cat_id = row[0]

    # then we get id of the record in time tracking table, id of the last record of the category in question
    s = text('SELECT id FROM time_track WHERE cat_id==:cat_id ORDER BY id DESC')
    with engine.begin() as conn:
        rec_id = conn.execute(s, {'cat_id': cat_id}).fetchone()[0]

    # now we get the start time to calculate time delta
    s = text('SELECT start_time FROM time_track WHERE id==:rec_id')
    with engine.begin() as conn:
        start_time = conn.execute(s, {'rec_id': rec_id}).fetchone()[0]
    time_delta = stop_time - start_time

    # now we update our record
    stop_date = date.today()
    s = text('UPDATE time_track '
             'SET stop_date=:stop_date, stop_time=:stop_time, time_delta=:time_delta '
             'WHERE id==:rec_id')
    d = {'stop_date': stop_date, 'stop_time': stop_time, 'time_delta': time_delta, 'rec_id': rec_id}
    with engine.begin() as conn:
        conn.execute(s, d)