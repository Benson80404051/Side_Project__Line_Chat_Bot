from flask import Flask
import json, os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, TemplateSendMessage, ImageMessage,
    RichMenu, ImageSendMessage, ImagemapSendMessage
)
from flask_ngrok import run_with_ngrok

app = Flask(__name__,static_url_path = "/material" , static_folder = "./material/")
run_with_ngrok(app)
#line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
#handler = WebhookHandler(os.environ['CHANNEL_SECRET'])
line_bot_api = LineBotApi('GM2rLZca9CeW3In4617DghQxcllIsiKMeRS1/H30nuYhRcr4wxaM7oKgtmr6Q9tmC3IRGS4QQIDoM86CbjL9NNQaJfryqoCpIOdup1CvWCjr6Yew8OVHs3wv198Tkxqf+gltkKtVCsmrf5KHu4EhuQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d2677cc638821a331ee8a7c950e69b21')
keywords_text = {
    '門市資訊':'實體店面不定期舉辦優惠活動，歡迎親臨本店挑選最貴的肉鬆~\n\n[桃園東勢店]\n地址: 平鎮區 福龍路一段 100號\n電話: 03-123-4567\n\n[台北公館店]\n地址: 大安區 羅斯福路四段1號\n電話: 02-2222-5252',
    '吃什麼?':'與中興大學產學合作, 飼料添加特殊菌種酵母, 比傳統飼料更營養、更容易吸收, 豬隻健康頭好壯壯不易生病!',
    '什麼狀況?':'所有豬隻健康狀況有專業的獸醫師監督。 飼育場的駐場獸醫師會定期替豬隻施打疫苗, 記錄成長狀況, 確保每隻小豬都活蹦亂跳。\n\n另外，在屠宰過程當中, 獸醫師會針對異常的屠宰肉品進行專業的分析及調查。',
    '智慧飼育場?':'採智慧養殖方式畜養小豬, 獨立的飼養空間隔絕了絕大多數的致病原。 \n飼養空間的給料、空調、清潔系統全部自動化, 不只能減少人力資源, 更能大幅減低人畜接觸傳染的問題, 提高豬隻的品質。',
    '冷運車':'冷運車引進美國製冷技術, 能讓車內氣溫穩定維持在攝氏7度以下, 讓豬肉保持新鮮',
    '生產地':'屠宰後的豬肉會立刻進行冷藏, 待冷運車運往冷儲中心',
    '冷儲':'冷儲中心為豬肉運往各地的樞紐, 依照銷售的目的地進行不同的冷藏處置, 確保肉品品質無虞',
    '店家':'冷運車將肉品送到一般店家; 貴鬆鬆肉鬆所使用的豬肉就是這樣運送的, 大家吃到的肉鬆都是用高品質的台灣豬所製成的喔~',
    '消費者':'實現 From Farm To Table 的精神, 產地直銷的肉品一樣是用冷運車配送, 品質不打折。\n\n產地直銷能讓消費者以更低的價格買到更好的肉品, 豬農也能得到較高的利潤, 避免中間剝削。',
}
keywords_query_product_text = ['減糖豬肉鬆',"蜜汁豬肉乾", "海苔豬肉鬆", "辣味牛肉乾", "黑胡椒豬肉乾", "原味豬肉絲", "辣味豬肉片", "辣味豬肉角", "原味牛肉乾", "辣味牛肉角" ]
keywords_template_menu = ['熱銷產品']
keywords_imagemap = ['產品選單']
keywords_change_rich_menu = {
    '想豬什麼':'richmenu-0d361202fb9fbc889a0cb68549abf586',
    '回主選單':'richmenu-bab739c99c82e9b143a39f19008cb933',
    '回上頁':'richmenu-0d361202fb9fbc889a0cb68549abf586',
    '住什麼?':'richmenu-e38e5046b289cd56287fe01cc46fb9bf',
    '怎麼運送?':'richmenu-532a26a74e2693df997a71cdd357b4f6'

                             }

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    message_content:str = event.message.text

    if message_content in keywords_template_menu:
        with open(message_content+'/reply.json', 'r', encoding='utf8') as f:
            reply_json = json.load(f)
        reply_send_message = TemplateSendMessage.new_from_json_dict(reply_json)
        line_bot_api.reply_message(event.reply_token, reply_send_message)
    elif message_content in keywords_query_product_text:  #之後建立好營養標示section要合併/刪除
        with open("product_info_buttun/"+message_content+'/reply.json', 'r', encoding='utf8') as f:
            reply_json = json.load(f)
        reply_send_message = TemplateSendMessage.new_from_json_dict(reply_json)
        line_bot_api.reply_message(event.reply_token, reply_send_message)

    elif message_content in keywords_text:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(keywords_text[message_content]))
    elif message_content in keywords_change_rich_menu:
        if message_content == '怎麼運送?':
            line_bot_api.reply_message(event.reply_token, TextSendMessage('冷鏈(Cold Chain)，是冷凍供應鏈，由冷凍加工、貯藏、物流運輸、銷售構成。\n\n冷鏈技術是消費者最終能否買到高品質產品重要的因素。'))
            line_bot_api.link_rich_menu_to_user(event.source.user_id, keywords_change_rich_menu[message_content])
        else:
            line_bot_api.link_rich_menu_to_user(event.source.user_id, keywords_change_rich_menu[message_content])
    elif message_content in keywords_imagemap:
        if message_content == '產品選單':
            with open(message_content + '/reply.json', 'r', encoding='utf8') as f:
                reply_json = json.load(f)
            image_message = ImagemapSendMessage.new_from_json_dict(reply_json)
            line_bot_api.reply_message(event.reply_token, image_message)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('看看選單其他功能吧'))


@handler.add(FollowEvent)
def handle_follow_message(event):
    # 取個資
    profile = line_bot_api.get_profile(event.source.user_id)

    # 存個資
    with open('user_info.text', 'a', encoding='utf8') as f:
        f.write(json.dumps(vars(profile), sort_keys=True))
        f.write('\r\n')

    # 發歡迎詞
    line_bot_api.reply_message(event.reply_token,  [
    TextSendMessage(text='感謝您關注貴貴鬆鬆肉鬆'),
    TextSendMessage(text='本店關心消費者健康\n與台灣在地豬農合作\n採用智慧養殖之豬肉\n肉品符合CAS標準\n且定期送驗SGS\n絕不含瘦肉精'),
    TextSendMessage(text='我們保證\n所有豬肉製品皆使用台灣智慧養殖豬肉\n請安心食用\n\n更多資訊請點擊圖文選單')])


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    # API get message content python
    message_content = line_bot_api.get_message_content(event.message.id)
    file_path = event.message.id + '.jpg'
    with open('./uploaded_img/'+file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    line_bot_api.reply_message(event.reply_token, TextSendMessage('已上傳'))

'''
RichMenu Section
'''




if __name__ == '__main__':
    app.run()
