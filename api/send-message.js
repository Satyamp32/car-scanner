// Vercel Serverless Function to route alerts to Telegram Bot for 100% free masking

export default async function handler(req, res) {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
    res.setHeader(
        'Access-Control-Allow-Headers',
        'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
    );

    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    try {
        const { type, message, location, callbackPhone } = req.body;

        // Basic validation
        if (!type) {
            return res.status(400).json({ error: 'Alert type is required' });
        }

        const botToken = process.env.TELEGRAM_BOT_TOKEN;
        const chatId = process.env.TELEGRAM_CHAT_ID;

        // Dev mode check / Fallback if env vars aren't set
        if (!botToken || !chatId) {
            console.warn("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is missing.");
            return res.status(200).json({
                success: true,
                warning: "Developer Mode: Message received but Telegram variables not configured in Vercel settings.",
                loggedData: { type, message, location, callbackPhone }
            });
        }

        // 1. Construct Telegram text
        let telegramText = `🚗 <b>VEHICLE OWNER ALERT</b>\n`;
        telegramText += `-----------------------------------------\n`;
        telegramText += `⚠️ <b>Alert Type:</b> ${type}\n`;
        
        if (message) {
            telegramText += `💬 <b>Message:</b> <i>"${message}"</i>\n`;
        }
        
        if (callbackPhone) {
            telegramText += `📞 <b>Callback Phone:</b> <code>${callbackPhone}</code>\n`;
        }
        
        if (location && location.latitude && location.longitude) {
            const mapsUrl = `https://maps.google.com/?q=${location.latitude},${location.longitude}`;
            telegramText += `📍 <b>Incident Location:</b> <a href="${mapsUrl}">View on Google Maps</a>\n`;
        }

        telegramText += `-----------------------------------------\n`;
        
        // 2. Add quick reply links for the owner
        if (callbackPhone) {
            const cleanPhone = callbackPhone.replace(/[^\d+]/g, ''); // sanitize for link
            telegramText += `⚡ <b>Quick Actions:</b>\n`;
            telegramText += `• <a href="tel:${cleanPhone}">Call Visitor Now</a>\n`;
            
            // Standard pre-filled reply text for the owner
            const ownerReply = `Hello, I received your vehicle contact alert. I'm on my way.`;
            const waLink = `https://wa.me/${cleanPhone.replace('+', '')}?text=${encodeURIComponent(ownerReply)}`;
            telegramText += `• <a href="${waLink}">WhatsApp Visitor Now</a>\n`;
        }

        // Send to Telegram
        const telegramUrl = `https://api.telegram.org/bot${botToken}/sendMessage`;
        const response = await fetch(telegramUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: chatId,
                text: telegramText,
                parse_mode: 'HTML',
                disable_web_page_preview: false
            })
        });

        const data = await response.json();
        
        if (!data.ok) {
            console.error('Telegram API responded with error:', data);
            return res.status(500).json({ error: 'Failed to send message via Telegram' });
        }

        return res.status(200).json({ success: true });

    } catch (error) {
        console.error('Server error forwarding alert:', error);
        return res.status(500).json({ error: 'Internal Server Error' });
    }
}
