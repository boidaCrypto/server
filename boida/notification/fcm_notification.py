from firebase_admin import messaging


def sent_to_firebase_cloud_messaging(fcm_token):
    message = messaging.Message(
        notification=messaging.Notification(
            title='거래소 연동이 완료되었습니다.',
            body='거래소 연동이 완료되었습니다.'
        ),
        token=fcm_token,
    )
    response = messaging.send(message)
    print("Successfully sent message", response)
