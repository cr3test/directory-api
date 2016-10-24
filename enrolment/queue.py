import gc
import logging
import uuid

from psycopg2.errorcodes import UNIQUE_VIOLATION
from rest_framework.serializers import ValidationError
from notifications_python_client.notifications import NotificationsAPIClient

from django.db import IntegrityError
from django.conf import settings

from enrolment import serializers
from enrolment.utils import ExitSignalReceiver, QueueService

logger = logging.getLogger(__name__)


class Enrolment(QueueService):
    """SQS queue service for enrolment"""
    queue_name = settings.SQS_ENROLMENT_QUEUE_NAME


class InvalidEnrolment(QueueService):
    """SQS queue service for invalid enrolment"""
    queue_name = settings.SQS_INVALID_ENROLMENT_QUEUE_NAME


class Worker:
    """Enrolment queue worker

    Attributes:
        exit_signal_receiver (ExitSignalReceiver): Handles SIGTERM and SIGINT
        enrolment_queue (enrolment.queue.Enrolment): Enrolment
            SQS queue service

        invalid_enrolment_queue (enrolment.queue.InvalidEnrolment):
            Invalid enrolment SQS queue service

    """
    def __init__(self):
        self.enrolment_queue = Enrolment()
        self.invalid_enrolment_queue = InvalidEnrolment()
        self.exit_signal_receiver = ExitSignalReceiver()

    @property
    def exit_signal_received(self):
        """Returns True if exit signal was received"""
        if self.exit_signal_receiver.received:
            logger.warning(
                "Exit signal received: {}".format(", ".join([
                    str(sig) for sig in self.exit_signal_receiver.received
                ]))
            )
            return True
        else:
            return False

    def run(self):
        """Runs worker until SIGTERM or SIGINT is received"""
        while not self.exit_signal_received:
            logger.info(
                "Retrieving messages from '{}' queue".format(
                    self.enrolment_queue.queue_name
                )
            )
            messages = self.enrolment_queue.receive()

            for message in messages:
                self.process_message(message)

                # exit cleanly when exit signal is received, unprocessed
                # messages will return to the enrolment queue
                if self.exit_signal_received:
                    return

            # Run a full garbage collection, as this is a long running process
            gc.collect()

    @staticmethod
    def is_valid_enrolment(message_body):
        """Returns True if message body is valid models.Enrolment

        Args:
            message_body (SQS.Message.body): SQS message body

        Returns:
            boolean: True if valid, False if not
        """
        serializer = serializers.EnrolmentSerializer(
            data={'data': message_body}
        )
        return serializer.is_valid()

    def process_message(self, message):
        """Creates new models.Enrolment if message body is a valid
        enrolment, otherwise sends it to the invalid enrolments queue

        Args:
            message (SQS.Message): message to process
        """
        logger.debug(
            "Processing message '{}'".format(message.message_id)
        )
        if self.is_valid_enrolment(message.body):
            try:
                self.process_enrolment(
                    json_payload=message.body,
                    sqs_message_id=message.message_id,
                )
            except ValidationError:
                logging.exception("Failed to process enrolment")
            except IntegrityError as exc:
                if self.is_postgres_unique_violation_error(exc):
                    logging.warning(
                        "Message '{}' has already been processed".format(
                            message.message_id,
                        )
                    )
                else:
                    raise
        else:
            logger.error(
                "Message '{}' body is not a valid enrolment, sending it to "
                "invalid messages queue".format(
                    message.message_id
                )
            )
            self.invalid_enrolment_queue.send(data=message.body)

        message.delete()

    @staticmethod
    def is_postgres_unique_violation_error(exception):
        """Returns true if exception is psycopg2 UNIQUE_VIOLATION error

        Args:
            exception (Exception): exception to check

        Returns:
            bool: True if exception is psycopg2 UNIQUE_VIOLATION error
        """
        return (
            hasattr(exception, 'pgcode') and
            exception.pgcode == UNIQUE_VIOLATION
        )

    def process_enrolment(self, sqs_message_id, json_payload):
        """Persis the message in enrolment.models.Enrolment
        # If there's an exception during email sending, the db
        # transaction should complete and the exception should be logged
        try:
            self.send_confirmation_email(user)
        except:
            logger.exception("Error sending confirmation email to %s",
                             payload['company_email'])

        Args:
            sqs_message_id (str): SQS message ID
            json_payload (str): The message body. A JSON payload.
        """
        logger.debug(
            "Saving new enrolment from message '{}'".format(sqs_message_id)
        )

        serializer = serializers.EnrolmentSerializer(data={
            'sqs_message_id': sqs_message_id,
            'data': json_payload,
        })

        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def send_confirmation_email(self, user):
        service_id = settings.GOV_NOTIFY_SERVICE_ID
        api_key = settings.GOV_NOTIFY_API_KEY
        template_id = settings.CONFIRMATION_EMAIL_TEMPLATE_ID
        user.confirmation_code = str(uuid.uuid4())
        user.save()
        notifications_client = NotificationsAPIClient(
            service_id=service_id, api_key=api_key)
        url = settings.CONFIRMATION_URL_TEMPLATE % user.confirmation_code
        notifications_client.send_email_notification(
            user.company_email, template_id,
            personalisation={'confirmation url': url})
