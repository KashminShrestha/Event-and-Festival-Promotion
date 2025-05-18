from django.urls import path
from .views import save_fcm_token, index, showFirebaseJS


urlpatterns = [

    path('firebase-messaging-sw.js',showFirebaseJS,name="show_firebase_js"),
    path('save-token/',save_fcm_token, name='save_fcm_token'),
    path('',index),

]