# -*- coding: utf-8 -*-
from IMS.models import Admin_user

__author__ = 'xyh' #...

from head import *
from djcode import settings
import os
import logging
from django.http import Http404

all_log_fileName = os.path.join(settings.LOGGING_DIR, "all.log")
error_log_fileName = os.path.join(settings.LOGGING_DIR, "error.log")
# request_log_fileName = os.path.join(settings.LOGGING_DIR, "request.log")

logger = logging.getLogger("IMS")
LEN_OF_ADMIN_ID = 3


@login_required()
def all_log(request):
    user_name = str(request.user)  # user Id
    user_name_len = user_name.__len__()
    if user_name_len != LEN_OF_ADMIN_ID:
        logger.warning(user_name + " tried to access all_log method without permission")
        return render(request, 'AccessFault.html')
    elif user_name_len == LEN_OF_ADMIN_ID:
        usrInfo = Admin_user.objects.get(id=user_name)
        if usrInfo.college != "all":
            logger.warning(user_name + " tried to access all_log method without permission")
            return render(request, 'AccessFault.html')
        else: # user permission
            all_logFile = open(all_log_fileName, "r")

            error_logFile = open(error_log_fileName, "r")
            all_the_text = ""
            try:
                all_the_text = all_logFile.readlines()
            except Exception,e:
                logger.error(e)
            finally:
                all_logFile.close()

            error_the_text = ""
            try:
                error_the_text = error_logFile.readlines()
            except Exception,e:
                logger.error(e)
            finally:
                error_logFile.close()
            # print error_the_text
            return render_to_response("log.html", {"alllogs": all_the_text, "errorlogs": error_the_text })

@login_required()
def delete_all_log(request):
    all_log_file = open(all_log_fileName, "w")
    try:
        all_log_file.truncate()
    except Exception,e:
        logger.ERROR(e)
    finally:
        all_log_file.close()

    error_log_file = open(error_log_fileName, "w")
    try:
        error_log_file.truncate()
    except Exception,e:
        logger.ERROR(e)
    finally:
        error_log_file.close()

    # request_log_file = open(request_log_fileName, "w")
    # try:
    #     request_log_file.truncate()
    # except Exception,e:
    #     logger.ERROR(e)
    # finally:
    #     request_log_file.close()


    return HttpResponseRedirect("../../log")