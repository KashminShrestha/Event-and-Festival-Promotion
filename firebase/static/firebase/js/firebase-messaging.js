import { initializeApp } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-app.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/11.2.0/firebase-messaging.js";

const firebaseConfig = {
    apiKey: "AIzaSyChnGrWhCVkzeyuLZZ52gkIdRpQ7Oa32mc",
    authDomain: "django-test-98569.firebaseapp.com",
    databaseURL: "https://django-test-98569-default-rtdb.firebaseio.com",
    projectId: "django-test-98569",
    storageBucket: "django-test-98569.firebasestorage.app",
    messagingSenderId: "587177278681",
    appId: "1:587177278681:web:aaa97ac6ae228eb3a152c8",
    measurementId: "G-2SEZT98T6Y"
};

const VAPID_KEY = "YOUR_VAPID_KEY";

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

async function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        try {
            const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js');
            console.log('Service Worker registered:', registration.scope);
        } catch (err) {
            console.error('Service Worker registration failed:', err);
        }
    }
}

async function requestNotificationPermission() {
    try {
        const permission = await Notification.requestPermission();
        if (permission !== 'granted') {
            console.warn('Notification permission denied');
            return null;
        }
        return permission;
    } catch (err) {
        console.error('Permission request error:', err);
        return null;
    }
}

async function getFcmToken() {
    try {
        const token = await getToken(messaging, { vapidKey: VAPID_KEY });
        if (token) {
            console.log('FCM Token:', token);
            await sendTokenToServer(token);
        } else {
            console.warn('No FCM registration token available');
        }
    } catch (err) {
        console.error('Error getting FCM token:', err);
    }
}

async function sendTokenToServer(token) {
    try {
        const response = await fetch('/save-token/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token }),
        });
        if (!response.ok) throw new Error(`Server error: ${response.status}`);
        console.log('Token saved on server');
    } catch (err) {
        console.error('Failed to send token to server:', err);
    }
}

function setupOnMessageListener() {
    onMessage(messaging, (payload) => {
        console.log('Message received:', payload);
        const { title, body, icon } = payload.notification || {};
        if (title) {
            new Notification(title, { body, icon });
        }
    });
}

window.addEventListener('load', async () => {
    await registerServiceWorker();
    setupOnMessageListener();
});

document.getElementById('request-permission').addEventListener('click', async () => {
    const permission = await requestNotificationPermission();
    if (permission === 'granted') {
        await getFcmToken();
    }
});
