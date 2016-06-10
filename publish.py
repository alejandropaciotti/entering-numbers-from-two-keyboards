import remodel.utils
import remodel.connection
from remodel.models import Model
import datetime
import pytz
from pytz import timezone


remodel.connection.pool.configure(db="databaseName")

class Codes(Model):
    pass


def publish(code, key):
    code = Codes.create(port=key,
                        code=code,
                        timestamp=datetime.datetime.now(timezone('America/Argentina/Cordoba')))

    code.save()
