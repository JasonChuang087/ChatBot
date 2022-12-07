from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage, StickerSendMessage

from opencc import OpenCC

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
cc = OpenCC('t2s')


@csrf_exempt
def callback(request):

    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.type == "text":
                    msg = cc.convert(event.message.text)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )
                elif event.message.type == "sticker":  # 傳貼圖
                    line_bot_api.reply_message(
                        event.reply_token, StickerSendMessage(package_id=1, sticker_id=2))
                elif event.message.type == "image":  # 傳貼圖
                    line_bot_api.reply_message(
                        event.reply_token, ImageSendMessage(original_content_url='https://i.imgur.com/P6M9s9H.jpeg', preview_image_url='https://i.imgur.com/P6M9s9H.jpeg'))  # 原圖/縮圖
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
