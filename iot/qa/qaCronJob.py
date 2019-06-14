from django.http.response import HttpResponse
# from django.utils import timezone
from qa.views import retrieve
from qa.webPush import pushMsg
from account.models import User
# from datetime import date
# from iot.settings import DOMAIN
# from django.urls.base import reverse
# from dateutil.relativedelta import relativedelta
# import pandas as pd

def notify(request):
#     now = timezone.now()
#     preTenMin = now - relativedelta(minutes=10)# 現在時間的10分鐘前
#     postTenMin = now + relativedelta(minutes=10)# 現在時間的10分鐘後
#     progresses = Progress.objects.filter(notifyDateTime__gte=preTenMin, notifyDateTime__lte=postTenMin, notified=False, minsNotify__gt=0)
    # 篩選出要notify的
    
    
    
    users = User.objects.filter(webPushEndpoint__isnull=False, keyword__isnull=False).exclude(keyword="")
    for user in users:
        df_ans = retrieve(user.keyword,return_num=1)
        title = ''
        url = ''
        for q in df_ans['title']:
            title = q
            url = str(df_ans[df_ans['title']==q]['url'].values[0])
        pushMsg(user, f'標題 : {title}\n網址 : {url}\n',   #開始時間 : {date.strftime(timezone.localtime(progress.startDateTime), "%Y-%m-%d %H:%M")}',
                str(df_ans[df_ans['title']==q]['url'].values[0]))
#         pushMsg(user, 'Succese!!!', 'localhost:8000/')

    return HttpResponse(True)