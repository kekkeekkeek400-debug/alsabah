require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const Groq = require('groq-sdk');
const fs = require('fs');

if (!process.env.GROQ_API_KEY) {
    console.error("❌ خطأ: لم يتم العثور على مفتاح GROQ_API_KEY في ملف .env!");
    process.exit(1);
}

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

let systemPrompt = "أنت مساعد ذكي ولطيف.";
try {
    systemPrompt = fs.readFileSync('prompt.txt', 'utf8');
} catch (err) {
    console.log("⚠️ لم يتم العثور على ملف prompt.txt، سيتم استخدام التعليمات الافتراضية.");
}

const chatMemory = new Map();

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', (qr) => {
    console.log('\n\n📱 يرجى مسح هذا الباركود باستخدام تطبيق الواتساب في هاتفك (الأجهزة المرتبطة):');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('✅ تم تسجيل الدخول بنجاح! البوت متصل برقمك الشخصي ويعمل عبر ذكاء Groq اللحظي.');
});

client.on('message', async msg => {
    if (msg.isGroupMsg || msg.isStatus) return;

    const userText = msg.body;
    const userId = msg.from;

    console.log(`📩 رسالة جديدة من ${userId}: ${userText}`);

    if (!chatMemory.has(userId)) {
        chatMemory.set(userId, [
            { role: "system", content: systemPrompt }
        ]);
    }
    const history = chatMemory.get(userId);

    try {
        const chat = await msg.getChat();
        await chat.sendStateTyping();

        history.push({ role: "user", content: userText });

        const chatCompletion = await groq.chat.completions.create({
            messages: history,
            model: "llama3-70b-8192",
            temperature: 0.2,
        });

        const replyText = chatCompletion.choices[0]?.message?.content || "عذراً لم أفهم.";

        history.push({ role: "assistant", content: replyText });

        if (history.length > 20) history.splice(1, 2);

        await chat.clearState();
        msg.reply(replyText);
        console.log(`🤖 الرد: ${replyText}`);

    } catch (error) {
        console.error('❌ خطأ في الذكاء الاصطناعي:', error.message);
        msg.reply('عذراً، أواجه صعوبة في التركيز حالياً.');
    }
});

client.initialize();
