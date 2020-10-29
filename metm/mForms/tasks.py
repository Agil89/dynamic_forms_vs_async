from celery import shared_task
from mForms.models import SendList
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import time
import asyncio

# @shared_task





