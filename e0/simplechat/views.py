import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Message

def login(request):
    return render(request, 'simplechat/login.html')

def chat(request):
    try:
      author = request.session["nickname"]
      message_list = Message.objects.all().order_by('-created_at')
      pages = Paginator(message_list, 5)
      page_number = request.GET.get("page")
      if page_number:
        try:
          messages = pages.page(page_number)
        except InvalidPage:
          messages = pages.page(1)
      else:
        messages = pages.page(1)
      context = {'messages': messages, "nickname": author}
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
