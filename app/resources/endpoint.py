from flask import Response, request
from flask_restful import Resource
from app import app, db
from app.common.util import s3_upload
from app.persist.models import Message


class Endpoint(Resource):
    def post(self):
        message_sid = request.values.get('MessageSid', None)
        account_sid = request.values.get('AccountSid', None)
        api_version = request.values.get('ApiVersion', None)
        body = request.values.get('Body', None)
        from_ = request.values.get('From', None)
        to = request.values.get('To', None)
        media_url = request.values.get('MediaUrl0', None)

        if account_sid in app.config['TWILIO_ACCOUNT_SIDS_CSV'].split(','):
            if media_url:
                s3_upload(media_url)

            message = Message(message_sid, account_sid, api_version,
                              body, from_, to, media_url)
            db.session.add(message)
            db.session.commit()

            return Response(status=204)

