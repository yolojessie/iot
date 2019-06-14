from pywebpush import webpush, WebPushException
from django.http.response import HttpResponse
# import datetime
import json


def subscription(request):
    data = request.GET.get('data')
    print(data)
    user = request.user
    if data != 'null':
        jsonData = json.loads(data)
        print(jsonData)
        print(jsonData['endpoint'])
        print(jsonData['keys']['p256dh'])
        print(jsonData['keys']['auth'])
        user.webPushEndpoint = jsonData['endpoint']
        user.webPushP256dh = jsonData['keys']['p256dh']
        user.webPushAuth = jsonData['keys']['auth']
    else:
        user.webPushEndpoint = None
        user.webPushP256dh = None
        user.webPushAuth = None
    user.save()
    print(user.webPushEndpoint)
    
    return HttpResponse(True)


def pushMsg(user, msg, url):
    # endpoint是user註冊通知時的瀏覽器or裝置資訊
    # p256dh & auth是用來加密推播出去的訊息
    try:
        webpush(
            subscription_info={
                "endpoint": user.webPushEndpoint,
                "keys": {
                    "p256dh": user.webPushP256dh,
                    "auth": user.webPushAuth
                }},
            data=json.dumps({'msg':msg, 'url':url}, ensure_ascii=False),
            vapid_private_key="2IH9egUDh7MrF9OHQhPC9PVCrQc-YxtTQl4yWt1V-gI",#"JuPocmyJjcg85LpvGFcI4AFb-OMRRskHQ13qm1VjDlA",# 找自己的
            vapid_claims={
                    "sub": "mailto:jessie840904@gmail.com"
                },
            ttl=60 * 1,
        )
    except WebPushException as e:
        print('error:', repr(e))
        # Mozilla returns additional information in the body of the response.
        if e.response and e.response.json():
            extra = e.response.json()
            print("Remote service replied with a {}:{}, {}",
                  extra.code,
                  extra.errno,
                  extra.message
                  )
    return HttpResponse(True)