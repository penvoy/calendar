import datetime

from server.celery import app
from .models import Events


@app.task
def create_future_events(event):
    # получаем следующую дату из перода
    next_event = datetime.datetime.fromtimestamp(event.get("date_start")) + datetime.timedelta(days=event.get("period"))

    # получаем дату конца периода 
    date_end = datetime.datetime(2035, 1, 1)

    # получаем инстанс начальной записи, чтобы записать в parent
    event_instance = Events.objects.filter(id=event.get("id")).first()
    if event_instance:
        parent_id = event_instance
    else:
        parent_id = None

    # создаём записи, пока не достигнем конечной даты
    while next_event < date_end:
        created = Events.objects.create(
            name=event.get("name"),
            date_start=next_event.timestamp(),
            period=event.get("period"),
            parent = parent_id
        )
        parent_id = created
        next_event += datetime.timedelta(days=event.get("period"))
    