from celery import shared_task
from django.shortcuts import get_object_or_404


@shared_task
def save_person(person_id):
    from basxconnect.core import models

    person = get_object_or_404(models.Person, pk=person_id)
    person.save()
