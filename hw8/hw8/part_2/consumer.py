import pika
from models import Contacts
import connect

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='contacts')


# Функція-заглушка для надсилання повідомлення по email
def send_email(contact_id):
    print(f"Sending email to contact with ID: {contact_id}")
    # Додайте ваш код для надсилання повідомлення по email


# Обробка повідомлень з черги RabbitMQ
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contacts.objects(id=contact_id).first()
    if contact:
        send_email(contact_id)
        contact.sent = True
        contact.save()
        print(f"Contact {contact_id} processed and email sent.")
    else:
        print(f"Contact with ID {contact_id} not found.")

# Встановлення функції зворотнього виклику для обробки повідомлень з черги
channel.basic_consume(queue='contacts', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()
