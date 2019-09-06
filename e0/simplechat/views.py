import json
import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage

from .models import Message

def login(request):
    return render(request, 'simplechat/login.html')

def chat(request):
    try:
      author = request.session["nickname"]
      message_list = Message.objects.all().order_by('-created_at')[:100]
      pages = Paginator(message_list, 5)
      page_number = request.GET.get("page")
      if page_number:
        try:
          messages = pages.page(page_number)
        except EmptyPage:
          return HttpResponseRedirect(reverse('chat'))
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
  
def post_quote(request):
    try:
      api_response = requests.get('https://api.quotable.io/random')
      api_json = api_response.json()
      quote = api_json["content"]
      quote_author = api_json["author"]
      text = f"'{quote}' - {quote_author}"
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
