import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Message

def login(request):
    return render(request, 'simplechat/login.html')

def chat(request):
    try:
      author = request.session["nickname"]
      message_list = Message.objects.all()
      context = {'message_list': message_list, "nickname": author}
      return render(request, 'simplechat/chat.html', context)
    except KeyError:
      return HttpResponseRedirect(reverse('login'))

def post_message(request):
    try:
      text = request.POST["text"]
      author = request.session["nickname"]
      new_message = Message(text = text, author = author, created_at = timezone.now())
      new_message.save()
      return HttpResponseRedirect(reverse('chat'))
    except KeyError:
      return HttpResponseRedirect(reverse('login'))

def set_nickname(request):
    request.session["nickname"] = request.POST["nickname"]
    return HttpResponseRedirect(reverse('chat'))

def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('login'))
