from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import httpx
import os

app = FastAPI()

VERIFY_TOKEN = "middleman2024"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

AWAITING_PROBLEM = {}

async def send_message(to, text):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": text}}
    async with httpx.AsyncClient() as client:
        await client.post(API_URL, json=payload, headers=headers)

async def send_buttons(to, body, buttons):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    btn_list = [{"type": "reply", "reply": {"id": b["id"], "title": b["title"]}} for b in buttons]
    payload = {
        "messaging_product": "whatsapp", "to": to, "type": "interactive",
        "interactive": {"type": "button", "body": {"text": body}, "action": {"buttons": btn_list}}
    }
    async with httpx.AsyncClient() as client:
        await client.post(API_URL, json=payload, headers=headers)

async def send_list(to, body, sections):
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp", "to": to, "type": "interactive",
        "interactive": {
            "type": "list", "body": {"text": body},
            "action": {"button": "اختر الخدمة", "sections": sections}
        }
    }
    async with httpx.AsyncClient() as client:
        await client.post(API_URL, json=payload, headers=headers)

async def handle_message(to, text_body):
   async def handle_message(to, text_body):
    await send_message(to, "اهلا بيك")
async def handle_interactive(to, reply_id):
    if reply_id == "sell":
        await send_message(to, """مرحبًا بيك في The Middle Man Auto 🚘

نحن شركة متخصصة في تسهيل بيع السيارات المستعملة بشكل احترافي، وهدفنا نبيع عربيتك بأفضل سعر ممكن بدون ما تشيل هم المكالمات أو التفاوض أو تضييع الوقت.

إحنا بنتولى:
• تسويق العربية بشكل احترافي
• تشغيل الإعلانات واستهداف العملاء الجادين
• الرد على المكالمات والرسائل والمتابعة
• تنظيم المعاينات والتفاوض مع المشترين
• المساعدة في إجراءات البيع ونقل الملكية

💰 نظام الشغل بعمولة 2% بحد أدنى 30,000 جنيه، ويتم الدفع فقط بعد إتمام البيع بنجاح.

⏳ مدة التسويق 15 يوم عمل.

لتسجيل عربيتك، برجاء ملء الفورم:
https://docs.google.com/forms/d/e/1FAIpQLSeqe27IbdYay1PK-TGjbsoqok7CVEe9E7D4ZdxGUw_Qiwr5Dw/viewform?usp=publish-editor""")

    elif reply_id == "inquire":
        await send_message(to, """شكرًا لتواصلك معانا 🚘
من فضلك املى الفورم التالي عشان فريق المبيعات يقدر يتواصل معاك ويساعدك بشكل أسرع:

https://docs.google.com/forms/d/e/1FAIpQLSdwrf3jnt-QIqm1cS1qb4WHjLr1i68HjoY71s4GJRGESEb6Uw/viewform?usp=publish-editor""")

    elif reply_id == "broker_yes1":
        await send_message(to, """لائحة بروكرز The Middle Man Auto 📋

أولاً: شروط الانضمام
1. الالتزام الكامل بسياسات الشركة
2. التعامل باحترام واحترافية
3. الحفاظ على سمعة الشركة
4. الالتزام بالمصداقية والدقة

ثانياً: قواعد العمل
1. جميع العملاء يتم التعامل عليهم من خلال الشركة فقط
2. يمنع تقديم معلومات غير صحيحة
3. يجب تحديث حالة العملاء بشكل مستمر
4. الالتزام بالأسعار المعتمدة من الإدارة

خامساً: العمولات
1. تستحق العمولة بعد إتمام البيع بنجاح
2. أي مخالفة قد تؤدي إلى إيقاف العمولة

يُعتبر الاستمرار موافقة كاملة على جميع البنود.""")
        await send_buttons(to, "هل توافق على اللائحة وشروط العمل؟",
            [{"id": "broker_yes2", "title": "✅ موافق"}, {"id": "broker_no", "title": "❌ غير موافق"}])

    elif reply_id == "broker_yes2":
        await send_message(to, """أهلًا بيك في فريق The Middle Man Auto 🎉

🔗 لينك جروب الفريق:
https://chat.whatsapp.com/Lvy9XjHVZlS0j3pGlabDyR?mode=gi_t

━━━━━━━━━━━━━━━
📌 Stock Sheet:
https://docs.google.com/spreadsheets/d/1UT9TfXTWJBENO-sCxxiqv_Q1ZpQowOeUVrLB8aZcL-s/edit?usp=sharing

📌 Leads Sheet:
https://docs.google.com/spreadsheets/d/1k98AiRt9uT7VZByFMuRRy1Bfc7DQlBARqnUm4CwkQ1U/edit?usp=sharing

📌 Payment Form:
https://docs.google.com/forms/d/e/1FAIpQLSfB5HS8UGc7LYb95A1NZBlEbxEauGRuPaI41e-0160s7WraJQ/viewform?usp=dialog

📌 Client Follow-Up Sheet:
https://docs.google.com/spreadsheets/d/1s94GjI7vo4DscVWYgzzd3KGUE_gqFapuFvU8lGf6u9o/edit?usp=drivesdk

📌 Inspection Form:
https://docs.google.com/forms/d/e/1FAIpQLSdq_oA6sOtWVsNB8XYIteIDRAAAHQPI_LCGC_MATILoDYMHew/viewform?usp=header

━━━━━━━━━━━━━━━
📞 التيم ليدرز:
هشام: 01015099623
عبدالله: 01000446883

بالتوفيق وإن شاء الله تحقق مبيعات قوية 🚘🤝""")

    elif reply_id == "broker_no":
        await send_message(to, "شكراً لاهتمامك بـ The Middle Man Auto 🙏\nنتمنى نشوفك معانا في وقت تاني 😊")

    elif reply_id == "admin":
        AWAITING_PROBLEM[to] = True
        await send_message(to, "من فضلك اكتب مشكلتك أو استفسارك وهيرد عليك أحد من فريقنا في أقرب وقت 🙏")

    elif reply_id == "broker":
        await send_message(to, """مرحبًا بيك في The Middle Man Auto 🚘

إحنا شغالين بنظام Brokerage & Sales Network، يعني شغل حر قائم على العمولات بدون مرتب ثابت أو مواعيد حضور.

نظام العمولات:
• نسبة العمولة تبدأ من 0.5%
• الحد الأدنى للعمولة 5,000 جنيه
• كل بروكر بيستلم عمولته فور إتمام البيع

دورك كبروكر:
• تسويق السيارات
• نشر الإعلانات
• جلب العملاء المهتمين

مميزات الشغل معانا:
• تشتغل من أي مكان وفي أي وقت
• بدون حضور معاينات
• عمولات مجزية مع فرص نمو""")
        await send_buttons(to, "هل أنت مهتم بالانضمام لفريقنا؟",
            [{"id": "broker_yes1", "title": "✅ مهتم"}, {"id": "broker_no", "title": "❌ مش مهتم"}])

@app.get("/webhook")
async def verify(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN and params.get("hub.mode") == "subscribe":
        return PlainTextResponse(params["hub.challenge"])
    return JSONResponse(content={"error": "Invalid token"}, status_code=403)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])
                for msg in messages:
                    to = msg["from"]
                    if msg["type"] == "text":
                        await handle_message(to, msg["text"]["body"])
                    elif msg["type"] == "interactive":
                        itype = msg["interactive"]["type"]
                        if itype == "button_reply":
                            await handle_interactive(to, msg["interactive"]["button_reply"]["id"])
                        elif itype == "list_reply":
                            await handle_interactive(to, msg["interactive"]["list_reply"]["id"])
    except Exception as e:
        print(f"Error: {e}")
    return JSONResponse(content={"status": "ok"})
