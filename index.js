require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const Groq = require('groq-sdk');
const fs = require('fs');
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

if (!process.env.GROQ_API_KEY) {
    console.error("❌ خطأ: لم يتم العثور على مفتاح GROQ_API_KEY في ملف .env!");
    process.exit(1);
}

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
const chatMemory = new Map();
let systemPrompt = "أنت مساعد ذكي ولطيف.";

// إعداد خادم الويب والاتصال الحي
const app = express();
app.use(cors());
app.use(express.json());
const server = http.createServer(app);
const io = new Server(server, {
    cors: { origin: "*" }
});

let whatsappClient = null;
let isReady = false;

io.on('connection', (socket) => {
    console.log('🔗 واجهة التحكم متصلة بالسيرفر!');
    
    // إرسال الحالة الحالية للوحة التحكم
    socket.emit('status', isReady ? 'ready' : 'waiting');

    socket.on('start_bot', (data) => {
        if (data && data.prompt) {
            systemPrompt = data.prompt;
            console.log('📝 تم تحديث تعليمات البوت من اللوحة:', systemPrompt);
        }

        if (whatsappClient) {
            socket.emit('message', 'البوت قيد التشغيل بالفعل.');
            return;
        }

        console.log('🚀 جاري بدء تشغيل بوت الواتساب...');
        socket.emit('status', 'initializing');

        whatsappClient = new Client({
            authStrategy: new LocalAuth(),
            puppeteer: {
                headless: true,
                args: [
                    '--no-sandbox', 
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--single-process',
                    '--disable-gpu',
                    '--js-flags="--max-old-space-size=250"',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process'
                ]
            }
        });

        whatsappClient.on('qr', (qr) => {
            console.log('📱 تم إنشاء الباركود، يتم إرساله للوحة التحكم...');
            // طباعة للكونسول للاحتياط
            qrcode.generate(qr, { small: true });
            // إرسال الكود للوحة التحكم ليتم رسمه هناك
            socket.emit('qr', qr);
            socket.emit('status', 'qr_ready');
        });

        whatsappClient.on('ready', () => {
            console.log('✅ تم تسجيل الدخول بنجاح!');
            isReady = true;
            socket.emit('status', 'ready');
            socket.emit('ready', '✅ البوت جاهز ويعمل الآن!');
        });

        whatsappClient.on('message', async msg => {
            if (msg.isGroupMsg || msg.isStatus) return;

            const userText = msg.body || '[رسالة غير نصية]';
            const userId = msg.from;

            console.log(`📩 رسالة جديدة من ${userId}: ${userText}`);
            socket.emit('message', `📩 رسالة استلمتها من ${userId.split('@')[0]}: ${userText}`);

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
                    model: "llama3-8b-8192",
                    temperature: 0.2,
                });

                const replyText = chatCompletion.choices[0]?.message?.content || "عذراً لم أفهم.";

                history.push({ role: "assistant", content: replyText });

                if (history.length > 20) history.splice(1, 2);

                await chat.clearState();
                msg.reply(replyText);
                
                console.log(`🤖 الرد: ${replyText}`);
                socket.emit('message', `🤖 البوت رد: ${replyText}`);

            } catch (error) {
                console.error('❌ خطأ في الذكاء الاصطناعي:', error.message);
                socket.emit('message', `❌ خطأ داخلي: ${error.message}`);
                msg.reply('عذراً، أواجه صعوبة في التركيز حالياً.');
            }
        });

        whatsappClient.on('disconnected', (reason) => {
            console.log('❌ تم قطع الاتصال بالواتساب', reason);
            isReady = false;
            socket.emit('status', 'disconnected');
            whatsappClient.destroy();
            whatsappClient = null;
        });

        whatsappClient.initialize();
    });
});

app.get('/', (req, res) => {
    res.send('WhatsApp Bot Backend is Running!');
});

const PORT = process.env.PORT || 10000;
server.listen(PORT, () => {
    console.log(`🌐 خادم البوت يعمل على المنفذ ${PORT}`);
});
