from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, ImageSendMessage, StickerSendMessage
from Linebot.functions import Chat

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
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.type == "text":
                    msg = Chat(event.message.text)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )
                elif event.message.type == "sticker":  # 傳貼圖
                    reply_arr = []
                    reply_arr.append(TextSendMessage(text="我不知道您想表達什麼..."))
                    reply_arr.append(StickerSendMessage(
                        package_id=11539, sticker_id=52114110))
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        reply_arr
                    )
                elif event.message.type == "image":  # 傳圖片
                    line_bot_api.reply_message(
                        event.reply_token, ImageSendMessage(original_content_url='https://i.imgur.com/P6M9s9H.jpeg', preview_image_url='https://i.imgur.com/P6M9s9H.jpeg'))  # 原圖/縮圖
                else:  # 其他
                    line_bot_api.reply_message(
                        event.reply_token, ImageSendMessage(original_content_url='https://i.imgur.com/34MoctZ.jpg', preview_image_url='https://i.imgur.com/34MoctZ.jpg'))  # 原圖/縮圖
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
