__author__ = 'Adward'

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from django.template import Template
from django.http import HttpResponseRedirect
from django.core.files import File
import re
import os
from django.template.context import RequestContext
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,Permission
from django.views.decorators.csrf import csrf_protect, csrf_exempt