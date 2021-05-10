from django.shortcuts import render

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, grants!")


def detail(request, application_id):
    return HttpResponse("You're looking at question %s." % application_id)


def results(request, application_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % application_id)


def vote(request, applicationquestion_id):
    return HttpResponse("You're voting on question %s." % applicationquestion_id)
