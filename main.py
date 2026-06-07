from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import httpx
import os

app = FastAPI()

VERIFY_TOKEN = "middleman2024"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

AWAITING_NAME = {}
AWAITING_PROBLEM = {}
ADMIN_NUMBER = "201222682620"


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

    # Step 1 of admin flow: user just sent their name → store it, ask for problem
    if to in AWAITING_NAME:
        AWAITING_PROBLEM[to] = text_body
        await send_message(to, "من فضلك اكتب تفاصيل مشكلتك أو استفسارك.")
        del AWAITING_NAME[to]
        return

    # Step 2 of admin flow: user just sent their problem → notify admin, thank user
    elif to in AWAITING_PROBLEM:
        await send_message(
            ADMIN_NUMBER,
            f"""🚨 طلب دعم جديد

👤 اسم العميل:
{AWAITING_PROBLEM[to]}

📞 رقم العميل:
{to}

💬 المشكلة / الاستفسار:
{text_body}"""
        )
        await send_message(
            to,
            "Thank you for contacting The Middle Man Auto 🚘\nManagement will get back to you as soon as possible."
        )
        del AWAITING_PROBLEM[to]
        return

    # Default: send welcome message then the service list
    await send_message(
        to,
        "🚗 أهلًا بيك في The Middle Man Auto\n\nشكرًا لتواصلك معانا 🤝\n\nنحن شركة متخصصة في الوساطة وتسويق السيارات، ونعمل على ربط المشترين والبائعين وتسهيل إتمام الصفقات باحترافية وشفافية.\n\nيسعدنا خدمتك، برجاء اختيار الخدمة المطلوبة من القائمة التالية."
    )
    await send_list(
        to,
        "برجاء اختيار الخدمة المطلوبة:",
        [{
            "title": "خدماتنا",
            "rows": [
                {"id": "sell",    "title": "عرض عربية للبيع",    "description": ""},
                {"id": "inquire", "title": "الاستفسار عن عربية", "description": ""},
                {"id": "broker",  "title": "الانضمام كبروكر",    "description": ""},
                {"id": "admin",   "title": "التواصل مع الإدارة", "description": ""}
            ]
        }]
    )


async def handle_interactive(to, reply_id):

    # ─── عرض عربية للبيع ───────────────────────────────────────────────────────
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

⏳ مدة التسويق على العربية 15 يوم عمل، وخلال الفترة دي بنشتغل للوصول لأفضل مشتري بأسرع وقت ممكن.

وفي حالة عدم إتمام البيع خلال المدة المحددة، يحق للمالك التصرف الكامل في السيارة دون أي التزامات.

🤍 ولتحقيق أفضل نتيجة وتسويق أقوى للعربية، يُفضل إزالة أي إعلانات أخرى خلال فترة العمل لتجنب تضارب الأسعار وتشتت العملاء.

شكرًا لثقتكم بـ The Middle Man Auto
https://docs.google.com/forms/d/e/1FAIpQLSeqe27IbdYay1PK-TGjbsoqok7CVEe9E7D4ZdxGUw_Qiwr5Dw/viewform?usp=publish-editor""")

    # ─── الاستفسار عن عربية ────────────────────────────────────────────────────
    elif reply_id == "inquire":
        await send_message(to, """شكرًا لتواصلك معانا 🚘
من فضلك املى الفورم التالي عشان فريق المبيعات يقدر يتواصل معاك ويساعدك بشكل أسرع:

https://docs.google.com/forms/d/e/1FAIpQLSdwrf3jnt-QIqm1cS1qb4WHjLr1i68HjoY71s4GJRGESEb6Uw/viewform?usp=publish-editor""")

    # ─── الانضمام كبروكر ───────────────────────────────────────────────────────
    elif reply_id == "broker":
        await send_message(to, """مرحبًا بيك في
The Middle Man Auto 🚘

إحنا شغالين بنظام Brokerage & Sales Network، يعني شغل حر قائم على العمولات بدون مرتب ثابت أو مواعيد حضور.

نظام العمولات:
• نسبة العمولة تبدأ من 0.5%
• الحد الأدنى للعمولة 5,000 جنيه
• كل بروكر بيستلم عمولته فور إتمام البيع
• كل عميل بيتسجل باسم البروكر داخل السيستم لضمان حفظ الحقوق
• مع زيادة النشاط والمبيعات، فيه فرص لزيادة نسبة العمولة وتحقيق دخل أعلى

دورك كبروكر:
• تسويق السيارات
• نشر الإعلانات
• جلب العملاء المهتمين

أما الإدارة فهي المسؤولة عن:
• التواصل مع مالك السيارة
• إدارة المعاينات
• التفاوض والاتفاق النهائي
• إنهاء البيع بالكامل

وده بيخليك تركز على البيع والتسويق فقط بدون ضغط المعاينات أو التفاوض.

مميزات الشغل معانا:
• تشتغل من أي مكان وفي أي وقت
• بدون حضور معاينات
• بدون التعامل المباشر مع المالك
• كل عميل بيتسجل باسمك وحقك محفوظ
• عمولات مجزية مع فرص نمو أكبر للمميزين

⚠️ جميع العملاء والمتابعات بتتم من خلال سيستم CRM مخصص لتنظيم الشغل وحفظ حقوق كل بروكر داخل الشركة.""")
        await send_buttons(to, "هل توافق على الانضمام لفريقنا؟",
            [{"id": "broker_yes1", "title": "✅ موافق"}, {"id": "broker_no", "title": "❌ غير موافق"}])

    # ─── موافق على الانضمام → عرض اللائحة ────────────────────────────────────
    elif reply_id == "broker_yes1":
        await send_message(to, """📋 لائحة بروكرز The Middle Man Auto

فيما يلي لائحة العمل الخاصة ببروكرز The Middle Man Auto، ويُعتبر العمل مع الشركة موافقةً كاملةً على جميع البنود التالية:

أولاً: شروط الانضمام
1. الالتزام الكامل بسياسات الشركة وأنظمة العمل.
2. التعامل باحترام واحترافية مع العملاء والزملاء.
3. الحفاظ على سمعة الشركة وعدم الإضرار بها بأي شكل من الأشكال.
4. الالتزام بالمصداقية والدقة في عرض معلومات السيارات.

ثانياً: قواعد العمل
1. جميع السيارات والعملاء المسجَّلين لدى الشركة يتم التعامل معهم من خلالها فقط.
2. يُمنع تقديم أي معلومات غير صحيحة أو مضللة للعملاء.
3. يجب تحديث حالة العملاء والمتابعات بشكل مستمر.
4. الالتزام بالأسعار والمعلومات المعتمدة من الإدارة.
5. أي عميل أو مالك سيارة أو بيانات يتم الحصول عليها من خلال الشركة أو إعلاناتها أو جروباتها أو أنظمتها تُعتبر من أصول الشركة، ويُمنع استغلالها أو التعامل عليها خارج إطارها بأي شكل من الأشكال.

ثالثاً: الإعلانات والتسويق
1. يحق للبروكر نشر إعلانات السيارات المعتمدة من الشركة.
2. يحق للبروكر استخدام رقمه الشخصي في الإعلانات.
3. يُمنع نشر أي إعلان بمعلومات أو أسعار غير معتمدة.
4. يجب الحفاظ على الهوية الاحترافية للشركة في جميع الإعلانات.

رابعاً: التعامل مع العملاء
1. الرد على العملاء بسرعة واحترافية.
2. الحفاظ على سرية بيانات العملاء والمالكين.
3. عدم الإساءة أو الدخول في أي خلافات مع العملاء.
4. رفع أي مشكلة أو شكوى إلى الإدارة فورًا.
5. يُمنع تحويل أي عميل أو مالك سيارة للتعامل الشخصي أو لصالح أي جهة أخرى دون موافقة الإدارة.

خامساً: العمولات
1. يتم احتساب العمولة طبقًا للنظام المعتمد من الشركة.
2. تستحق العمولة بعد إتمام البيع بنجاح واستلام الشركة لمستحقاتها.
3. أي مخالفة لنظام العمل قد تؤدي إلى إيقاف العمولة أو إنهاء التعاون.

سادساً: المخالفات
يحق للإدارة اتخاذ الإجراءات المناسبة في الحالات التالية:
• نشر معلومات أو أسعار غير صحيحة.
• الإضرار بسمعة الشركة.
• إساءة التعامل مع العملاء.
• مخالفة سياسات العمل المعتمدة.
• استغلال بيانات العملاء أو المالكين خارج إطار الشركة.
• إتمام أي عملية بيع أو شراء تخص الشركة دون علم الإدارة.

الإقرار والموافقة
تُرسل هذه اللائحة إلى جميع البروكرز العاملين مع The Middle Man Auto، ويُعتبر البقاء داخل جروب العمل بعد الاطلاع على هذه الرسالة موافقةً صريحةً وكاملةً على جميع الشروط والأحكام الواردة بها.

في حال عدم الموافقة على أي بند من البنود المذكورة، يحق للبروكر مغادرة الجروب والتوقف عن العمل مع الشركة، ولن يُسمح بالاستمرار ضمن فريق العمل إلا بعد الموافقة الكاملة على هذه اللائحة.

استمرار التواجد داخل الجروب أو ممارسة أي نشاط متعلق بالشركة يُعد إقرارًا بالالتزام بجميع السياسات والأنظمة المذكورة أعلاه.

مع تمنياتنا للجميع بالتوفيق والنجاح.

— إدارة The Middle Man Auto 🤝🚘""")
        await send_buttons(to, "هل توافق على اللائحة وشروط العمل؟",
            [{"id": "broker_yes2", "title": "✅ موافق"}, {"id": "broker_no", "title": "❌ غير موافق"}])

    # ─── موافق على اللائحة → إرسال دليل البروكر كاملاً (رسالتين) ────────────
    elif reply_id == "broker_yes2":

        # ── الرسالة الأولى: دليل البروكر مع الروابط ──
        await send_message(to, """🚗 The Middle Man Auto | Broker Guide & Important Links 🚗

أهلًا يا شباب 👋

عشان الشغل يبقى منظم وكل المعلومات تكون في مكان واحد، دي أهم الأنظمة والروابط المطلوبة لكل Broker:

لينك الانضمام الي الجروب الخاص بالبروكرز:
https://chat.whatsapp.com/Lvy9XjHVZlS0j3pGlabDyR?mode=gi_t

━━━━━━━━━━━━━━━

📌 1- Stock Sheet
الشيت الخاص بالاستوك المتاح حاليًا، وبيحتوي على العربيات المتوفرة وتفاصيل كل عربية لتسهيل عرضها على العملاء ومتابعة المتاح.

🔗 Link:
https://docs.google.com/spreadsheets/d/1UT9TfXTWJBENO-sCxxiqv_Q1ZpQowOeUVrLB8aZcL-s/edit?usp=sharing

⚠️ الشيت للاستخدام الداخلي فقط وممنوع مشاركته خارج الشركة.

━━━━━━━━━━━━━━━

📌 2- Leads Sheet
أي Lead جاي من إعلانات الشركة هينزل تلقائي داخل الشيت ويتم توزيعه بشكل عشوائي على البروكرز.

مسؤولية البروكر:
• التواصل السريع مع العميل
• تحديد موعد المعاينة
• متابعة العميل بالكامل
• ملء الفورم بعد الاتفاق

بعد ذلك الشركة تتولى باقي الإجراءات حتى إتمام العملية.

🔗 Link:
https://docs.google.com/spreadsheets/d/1k98AiRt9uT7VZByFMuRRy1Bfc7DQlBARqnUm4CwkQ1U/edit?usp=sharing

⚠️ ممنوع التعامل مع Leads مخصصة لبروكر آخر.

━━━━━━━━━━━━━━━

📌 3- Payment Information Form
برجاء تسجيل وسيلة استلام العمولة الخاصة بك (InstaPay أو محفظة) وإدخال البيانات المطلوبة لضمان سرعة إجراءات الدفع.

🔗 Link:
https://docs.google.com/forms/d/e/1FAIpQLSfB5HS8UGc7LYb95A1NZBlEbxEauGRuPaI41e-0160s7WraJQ/viewform?usp=dialog

━━━━━━━━━━━━━━━

📌 4- Client Follow-Up Sheet
شيت متابعة العملاء، ويحتوي على آخر التحديثات الخاصة بكل عميل من خلال خانة Feedback.

🔗 Link:
https://docs.google.com/spreadsheets/d/1s94GjI7vo4DscVWYgzzd3KGUE_gqFapuFvU8lGf6u9o/edit?usp=drivesdk

⚠️ الشيت Viewer Only للحفاظ على البيانات ومنع أي تعديل أو حذف.

━━━━━━━━━━━━━━━

📌 5- Inspection Form (مهم جدًا)
الفورم الرسمي لتسجيل بيانات العملاء والمعاينات.

يجب إدخال:
• اسم العميل
• رقم الهاتف
• نوع السيارة
• السعر المتفق عليه
• اسم البروكر

ويمكن إضافة:
• السعر المقترح من المشتري
• تاريخ ووقت المعاينة
• أي ملاحظات إضافية

🔗 Link:
https://docs.google.com/forms/d/e/1FAIpQLSdq_oA6sOtWVsNB8XYIteIDRAAAHQPI_LCGC_MATILoDYMHew/viewform?usp=header

⚠️ أي معاينة لن يتم تسجيلها من خلال الفورم الرسمي قد يتم إلغاؤها، والفورم هو الوسيلة المعتمدة الوحيدة لتسجيل العملاء والمعاينات.

━━━━━━━━━━━━━━━""")

        # ── الرسالة الثانية: التنويه المهم ──
        await send_message(to, """📢 تنويه مهم لجميع البروكرز

أي استفسار يخص عربية، معاينة، تسعير، أو أي نقطة خاصة بالشغل، يرجى التواصل مباشرة مع:

📞 هشام: 01015099623
📞 عبدالله: 01000446883

⚠️ بخصوص العملاء المهتمين بالشراء:

❌ ممنوع تمامًا وغير مقبول مشاركة بيانات أي عميل مهتم بالشراء أو تحويله لأي بروكر آخر، بما في ذلك هشام وعبدالله.

❌ ممنوع إرسال أرقام أو بيانات العملاء داخل الجروب أو لأي شخص آخر.

✅ أي عميل دخل باسم بروكر معين أو تواصل معه بشكل مباشر، يظل العميل تابعًا لهذا البروكر فقط، وهو المسؤول عن متابعته حتى إتمام الصفقة.

✅ العمولة تكون من حق البروكر صاحب العميل فقط.

📋 في حالة وجود أي استفسار أو احتياج للمساعدة، يمكن الرجوع لهشام أو عبدالله للدعم والإرشاد فقط، وليس لاستلام أو متابعة العملاء أو التواصل معهم.

وذلك لحين إشعار آخر.

نشكر الجميع على الالتزام بالنظام حفاظًا على حقوق جميع أعضاء الفريق وتنظيم سير العمل.

🤝🚘 The Middle Man Auto""")

    # ─── غير مهتم / غير موافق ──────────────────────────────────────────────────
    elif reply_id == "broker_no":
        await send_message(to, "شكراً لاهتمامك بـ The Middle Man Auto 🙏\nنتمنى نشوفك معانا في وقت تاني 😊")

    # ─── التواصل مع الإدارة → طلب الاسم أولاً ────────────────────────────────
    elif reply_id == "admin":
        AWAITING_NAME[to] = True
        await send_message(to, "من فضلك اكتب اسمك بالكامل.")


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
