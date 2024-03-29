import pika
import faker
from models import Contacts
import connect


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='contacts')

    
def produce_contacts(num_contacts):
    fake = faker.Faker()
    for _ in range(num_contacts):
        full_name = fake.name()
        email = fake.email()
        contact = Contacts(full_name=full_name, email=email)
        contact.save()
        channel.basic_publish(exchange='', routing_key='contacts', body=str(contact.id))


if __name__ == '__main__':
    produce_contacts(10)