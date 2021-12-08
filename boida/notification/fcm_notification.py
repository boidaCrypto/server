from firebase_admin import messaging

def sent_to_firebase_cloud_messaging(fcm_token, exchange_name):
    message = messaging.Message(
        notification=messaging.Notification(
            title='{0}와 연동이 완료되었습니다.'.format(exchange_name),
            body='{0}와 연동이 완료되었습니다.'.format(exchange_name)
        ),
        token=fcm_token,
    )
    response = messaging.send(message)
    print("Successfully sent message", response)
