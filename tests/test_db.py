from flaskr.db import get_db
import sqlite3
import pytest


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e)

def init_db_command(runner , monkeypatch):
    class Recorder(object):
        called = False
    
    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db' , fake_init_db)
    result = runner.invoke(['init_db'])
    assert 'initialized' in result.output
    assert Recorder.called
