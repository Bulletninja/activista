import yaml
import sendgrid
from smtpapi import SMTPAPIHeader
from sqlalchemy import *

class Sender():
    dbconfig = {}
    user = ''
    userPwd = ''
    address = ''
    db = ''
    connect_str = 'mysql+mysqlconnector://'+user+':'+userPwd+'@'+address+'/'+db
    config = []#nombre, correo, teléfono
    #https://docs.python.org/3/library/csv.html
	with open('cfg.csv') as csvfile:
		#personas = csv.reader(csvfile, delimiter=' ', quotechar='|')
        personas = csv.DictReader(csvfile)
        for persona in personas:
            config.append(persona)
#sendgrid API
	client = sendgrid.SendGridClient(config['mail']['key'])
	message = sendgrid.Mail()

	message.set_from(config['mail']['from_transaction'])
	message.set_from_name(config['mail']['from_transaction_name'])

	message.add_category('Reminder')
	message.add_filter('templates', 'enable', '1')
	message.add_filter('templates', 'template_id', 'db8bcf66-5c0c-4f54-ab40-60f1f92fd9a1')

	message.add_to('')
	message.add_to('luis.valenzuela@mustache.mx')
    message.add_to('-email-')
    message.set_replyto('hola@activistadigital')#reply_to email goes here
	message.set_subject('Hola -name-, este es un recordatorio de Clinicamia')
	message.set_html('<h2>Hola -name-,</h2></br>Este es un recordatorio para que .')

	def set_data(self, data):
		self.message.add_substitution('-name-', data['name'])
		print(data['name'])

    def send(self):
		status, msg = self.client.send(self.message)
		print(status, msg)

    def send_all(self):
        engine = create_engine(self.connect_str, echo=False)
        for persona in self.config:
            self.message.add_substitution('-name-', persona['nombre'])
            self.message.add_substitution('-email-', persona['email'])
            status, msg = self.client.send(self.message)
            ins_str = """
            INSERT INTO amigosq (nombre, email, telefono) VALUES ({}, {}, {})
            """.format(persona['nombre'], persona['email'], persona['telefono'])
            engine.execute(ins_str)
            print(status, msg)
