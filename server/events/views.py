import datetime
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import EventSerializer, Events
from .tasks import create_future_events

class EventViewSet(viewsets.ViewSet):

    def create(self, request):
        """
        Функция для создания события
        """
        # сериализуем данные
        serializer = EventSerializer(data=request.data)

        # если успешно, то сохраняем
        if serializer.is_valid():
            event = serializer.save()

            # в случае, если передан период - отправляем в отложенную задачу и создаем события
            if event.period:
                create_future_events.delay(serializer.data)
            return Response({'id': event.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id, year, month, day):
        """
        Функция для удаления конкретного события
        """
        try:
            event = Events.objects.get(id=id)
            # архивируем, чтобы не сломать связи
            event.archive = True
            event.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy_next(self, request, id, year, month, day):
        """
        Функция для удаления цепочки событий
        """
        try:
            event = Events.objects.get(id=id)
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, id, year, month, day):
        """
        Функция для обновления события
        """
        name = request.data.get("name")
        try:
            event = Events.objects.get(id=id)
            if name:
                event.name = name
                event.save()
                return Response({'id': event.id, 'name': event.name},status=status.HTTP_202_ACCEPTED)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request, year, month, day):
        """
        Функция для вывода событий
        """
        # получаем дату в дататайм формате
        date_start = datetime.datetime(year, month, day)

        # получаем дату следующего дня
        date_finish = date_start + datetime.timedelta(days=1)

        # отбираем неархивированные записи, которые входят в интервал между date_start и date_finish
        events = Events.objects.filter(archive=False, date_start__gte=date_start.timestamp(), date_start__lt=date_finish.timestamp())
        response_data = [{'id': event.id, 'name': event.name} for event in events]
        return Response(response_data)