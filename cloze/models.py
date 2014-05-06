# -*- coding: UTF-8 -*-

from django.db import models
from django.db.models import Max, Count
from django.forms import ModelForm, CharField
from django.template import RequestContext,Context, loader
import random
import json
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit


GENDER_CHOICES = (
        ("MAS", 'Masculino'),
        ("FEM", 'Femenino'),
    )
		
LANGUAGE = (
		("Esp", 'Español'),
		("Ing", 'Inglés'),
		("Fra", 'Francés'),
		('Ale', 'Aleman'),
		('Port', 'Portugués'),
		("Otro", 'Otro')
		
	)
	
COUNTRIES = (
    ('AR', ('Argentina')),
    ('AD', ('Andorra')),
    ('AE', ('United Arab Emirates')),
    ('AF', ('Afghanistan')),
    ('AG', ('Antigua & Barbuda')),
    ('AI', ('Anguilla')),
    ('AL', ('Albania')),
    ('AM', ('Armenia')),
    ('AN', ('Netherlands Antilles')),
    ('AO', ('Angola')),
    ('AQ', ('Antarctica')),
    ('AS', ('American Samoa')),
    ('AT', ('Austria')),
    ('AU', ('Australia')),
    ('AW', ('Aruba')),
    ('AZ', ('Azerbaijan')),
    ('BA', ('Bosnia and Herzegovina')),
    ('BB', ('Barbados')),
    ('BD', ('Bangladesh')),
    ('BE', ('Belgium')),
    ('BF', ('Burkina Faso')),
    ('BG', ('Bulgaria')),
    ('BH', ('Bahrain')),
    ('BI', ('Burundi')),
    ('BJ', ('Benin')),
    ('BM', ('Bermuda')),
    ('BN', ('Brunei Darussalam')),
    ('BO', ('Bolivia')),
    ('BR', ('Brazil')),
    ('BS', ('Bahama')),
    ('BT', ('Bhutan')),
    ('BV', ('Bouvet Island')),
    ('BW', ('Botswana')),
    ('BY', ('Belarus')),
    ('BZ', ('Belize')),
    ('CA', ('Canada')),
    ('CC', ('Cocos (Keeling) Islands')),
    ('CF', ('Central African Republic')),
    ('CG', ('Congo')),
    ('CH', ('Switzerland')),
    ('CI', ('Ivory Coast')),
    ('CK', ('Cook Iislands')),
    ('CL', ('Chile')),
    ('CM', ('Cameroon')),
    ('CN', ('China')),
    ('CO', ('Colombia')),
    ('CR', ('Costa Rica')),
    ('CU', ('Cuba')),
    ('CV', ('Cape Verde')),
    ('CX', ('Christmas Island')),
    ('CY', ('Cyprus')),
    ('CZ', ('Czech Republic')),
    ('DE', ('Germany')),
    ('DJ', ('Djibouti')),
    ('DK', ('Denmark')),
    ('DM', ('Dominica')),
    ('DO', ('Dominican Republic')),
    ('DZ', ('Algeria')),
    ('EC', ('Ecuador')),
    ('EE', ('Estonia')),
    ('EG', ('Egypt')),
    ('EH', ('Western Sahara')),
    ('ER', ('Eritrea')),
    ('ES', ('Spain')),
    ('ET', ('Ethiopia')),
    ('FI', ('Finland')),
    ('FJ', ('Fiji')),
    ('FK', ('Falkland Islands (Malvinas)')),
    ('FM', ('Micronesia')),
    ('FO', ('Faroe Islands')),
    ('FR', ('France')),
    ('FX', ('France, Metropolitan')),
    ('GA', ('Gabon')),
    ('GB', ('United Kingdom (Great Britain)')),
    ('GD', ('Grenada')),
    ('GE', ('Georgia')),
    ('GF', ('French Guiana')),
    ('GH', ('Ghana')),
    ('GI', ('Gibraltar')),
    ('GL', ('Greenland')),
    ('GM', ('Gambia')),
    ('GN', ('Guinea')),
    ('GP', ('Guadeloupe')),
    ('GQ', ('Equatorial Guinea')),
    ('GR', ('Greece')),
    ('GS', ('South Georgia and the South Sandwich Islands')),
    ('GT', ('Guatemala')),
    ('GU', ('Guam')),
    ('GW', ('Guinea-Bissau')),
    ('GY', ('Guyana')),
    ('HK', ('Hong Kong')),
    ('HM', ('Heard & McDonald Islands')),
    ('HN', ('Honduras')),
    ('HR', ('Croatia')),
    ('HT', ('Haiti')),
    ('HU', ('Hungary')),
    ('ID', ('Indonesia')),
    ('IE', ('Ireland')),
    ('IL', ('Israel')),
    ('IN', ('India')),
    ('IO', ('British Indian Ocean Territory')),
    ('IQ', ('Iraq')),
    ('IR', ('Islamic Republic of Iran')),
    ('IS', ('Iceland')),
    ('IT', ('Italy')),
    ('JM', ('Jamaica')),
    ('JO', ('Jordan')),
    ('JP', ('Japan')),
    ('KE', ('Kenya')),
    ('KG', ('Kyrgyzstan')),
    ('KH', ('Cambodia')),
    ('KI', ('Kiribati')),
    ('KM', ('Comoros')),
    ('KN', ('St. Kitts and Nevis')),
    ('KP', ('Korea, Democratic People\'s Republic of')),
    ('KR', ('Korea, Republic of')),
    ('KW', ('Kuwait')),
    ('KY', ('Cayman Islands')),
    ('KZ', ('Kazakhstan')),
    ('LA', ('Lao People\'s Democratic Republic')),
    ('LB', ('Lebanon')),
    ('LC', ('Saint Lucia')),
    ('LI', ('Liechtenstein')),
    ('LK', ('Sri Lanka')),
    ('LR', ('Liberia')),
    ('LS', ('Lesotho')),
    ('LT', ('Lithuania')),
    ('LU', ('Luxembourg')),
    ('LV', ('Latvia')),
    ('LY', ('Libyan Arab Jamahiriya')),
    ('MA', ('Morocco')),
    ('MC', ('Monaco')),
    ('MD', ('Moldova, Republic of')),
    ('MG', ('Madagascar')),
    ('MH', ('Marshall Islands')),
    ('ML', ('Mali')),
    ('MN', ('Mongolia')),
    ('MM', ('Myanmar')),
    ('MO', ('Macau')),
    ('MP', ('Northern Mariana Islands')),
    ('MQ', ('Martinique')),
    ('MR', ('Mauritania')),
    ('MS', ('Monserrat')),
    ('MT', ('Malta')),
    ('MU', ('Mauritius')),
    ('MV', ('Maldives')),
    ('MW', ('Malawi')),
    ('MX', ('Mexico')),
    ('MY', ('Malaysia')),
    ('MZ', ('Mozambique')),
    ('NA', ('Namibia')),
    ('NC', ('New Caledonia')),
    ('NE', ('Niger')),
    ('NF', ('Norfolk Island')),
    ('NG', ('Nigeria')),
    ('NI', ('Nicaragua')),
    ('NL', ('Netherlands')),
    ('NO', ('Norway')),
    ('NP', ('Nepal')),
    ('NR', ('Nauru')),
    ('NU', ('Niue')),
    ('NZ', ('New Zealand')),
    ('OM', ('Oman')),
    ('PA', ('Panama')),
    ('PE', ('Peru')),
    ('PF', ('French Polynesia')),
    ('PG', ('Papua New Guinea')),
    ('PH', ('Philippines')),
    ('PK', ('Pakistan')),
    ('PL', ('Poland')),
    ('PM', ('St. Pierre & Miquelon')),
    ('PN', ('Pitcairn')),
    ('PR', ('Puerto Rico')),
    ('PT', ('Portugal')),
    ('PW', ('Palau')),
    ('PY', ('Paraguay')),
    ('QA', ('Qatar')),
    ('RE', ('Reunion')),
    ('RO', ('Romania')),
    ('RU', ('Russian Federation')),
    ('RW', ('Rwanda')),
    ('SA', ('Saudi Arabia')),
    ('SB', ('Solomon Islands')),
    ('SC', ('Seychelles')),
    ('SD', ('Sudan')),
    ('SE', ('Sweden')),
    ('SG', ('Singapore')),
    ('SH', ('St. Helena')),
    ('SI', ('Slovenia')),
    ('SJ', ('Svalbard & Jan Mayen Islands')),
    ('SK', ('Slovakia')),
    ('SL', ('Sierra Leone')),
    ('SM', ('San Marino')),
    ('SN', ('Senegal')),
    ('SO', ('Somalia')),
    ('SR', ('Suriname')),
    ('ST', ('Sao Tome & Principe')),
    ('SV', ('El Salvador')),
    ('SY', ('Syrian Arab Republic')),
    ('SZ', ('Swaziland')),
    ('TC', ('Turks & Caicos Islands')),
    ('TD', ('Chad')),
    ('TF', ('French Southern Territories')),
    ('TG', ('Togo')),
    ('TH', ('Thailand')),
    ('TJ', ('Tajikistan')),
    ('TK', ('Tokelau')),
    ('TM', ('Turkmenistan')),
    ('TN', ('Tunisia')),
    ('TO', ('Tonga')),
    ('TP', ('East Timor')),
    ('TR', ('Turkey')),
    ('TT', ('Trinidad & Tobago')),
    ('TV', ('Tuvalu')),
    ('TW', ('Taiwan, Province of China')),
    ('TZ', ('Tanzania, United Republic of')),
    ('UA', ('Ukraine')),
    ('UG', ('Uganda')),
    ('UM', ('United States Minor Outlying Islands')),
    ('US', ('United States of America')),
    ('UY', ('Uruguay')),
    ('UZ', ('Uzbekistan')),
    ('VA', ('Vatican City State (Holy See)')),
    ('VC', ('St. Vincent & the Grenadines')),
    ('VE', ('Venezuela')),
    ('VG', ('British Virgin Islands')),
    ('VI', ('United States Virgin Islands')),
    ('VN', ('Viet Nam')),
    ('VU', ('Vanuatu')),
    ('WF', ('Wallis & Futuna Islands')),
    ('WS', ('Samoa')),
    ('YE', ('Yemen')),
    ('YT', ('Mayotte')),
    ('YU', ('Yugoslavia')),
    ('ZA', ('South Africa')),
    ('ZM', ('Zambia')),
    ('ZR', ('Zaire')),
    ('ZW', ('Zimbabwe')),
    ('ZZ', ('Unknown or unspecified country')))

SCHOOLING = (
		('Pri_Inc', 'Primario Incompleto'),
		('Pri_Com', 'Primario Completo'),
		('Sec_Inc', 'Secundario Incompleto'),
		('Sec_Com', 'Secundario Completo'),
		('Ter_Inc', 'Terciario Incompleto'),
		('Ter_Com', 'Terciario Completo'),
		('Uni_Inc', 'Universitario Incompleto'),
		('Uni_Com', 'Universitario Completo')
	)

QUANTITY = (
		('-5', 'Menos de 5'),
		('5-10', 'Entre 5 y 10'),
		('+10', 'Más de 10')
		
	)

YES_NO = (
		('Yes', 'Sí'),
		('No','No')
	)

DEXTERITY = (
		('Right','Diestro/a'),
		('Left','Zurdo/a')
	)

SOURCE = (
		('FB_Labo','Por la página de Facebook del Laboratorio'),
		('FB_amigo','Por otro Facebook'),
		('Twitter','Por Twitter'),
		('mail','Por e-mail')
	)

# Create your models here.
class Subject(models.Model):
	email = models.EmailField()
	age = models.IntegerField(blank=False, null=False)
	gender = models.CharField(max_length=3, blank=False, null=False)
	original_ip = models.GenericIPAddressField()
	sequence_number = models.IntegerField(null=True)
	experiment_sequence = models.CharField(max_length=2550)
	

	def __unicode__(self):
		return (self.email)
			
	@staticmethod
	def generate_sequence():
		#d = Text.objects.values('textNumber').annotate(Count('textNumber'))
		#max_text_number = int(Text.objects.all().aggregate(Max('textNumber'))['textNumber__max']) + 1
		#max_text_class = int(Text.objects.all().aggregate(Max('textClass'))['textClass__max'])
		#seq = [ random.choice(TrialOption.objects.filter(text__textNumber=x).filter(text__textClass=random.randint(0, max_text_class))).id for x in range(0,max_text_number)]
		
		ts_num = ( Subject.objects.count() % TrialSequence.objects.count() )
		ts = TrialSequence.objects.all().order_by('id')[ts_num]
		seq_base1 = json.loads(ts.seq)
		#seq_base0 = map(lambda x: x-1,seq_base1)
		# Disable randomize chosen sequence.
		#random.shuffle(seq_base0)
		
		# Si se quiere cambiar el orden de los textos o eliminar un texto, se cambia desde acá. 
		# Cada elemento de seq_base1 es un experimento variable pero siempre del mismo texto. 
		seq_base0 = seq_base1[5:]
		seq_base0.append(seq_base1[0]) # Pongo el 1º texto al final
		seq_base0.append(seq_base1[1]) # Pongo el 2º texto al final
		seq_base0.append(seq_base1[2]) # Pongo el 3º texto al final
		seq_base0.append(seq_base1[3]) # Pongo el 4º texto al final
		seq_base0.append(seq_base1[4]) # Pongo el 5º texto al final
		
		return (ts.id,seq_base0)       

class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ['email','age','gender','original_ip']
	
class Information(models.Model):
    subject = models.OneToOneField(Subject, primary_key=True)
    native_language = models.CharField(max_length=200, choices=LANGUAGE, blank=False, null=False)
    reading_language = models.CharField(max_length=200, choices=LANGUAGE, blank=False, null=False)
    work_reading_language = models.CharField(max_length=200, choices=LANGUAGE, blank=False, null=True)
    country = models.CharField(max_length=200, choices=COUNTRIES, blank=False, null=False)
    schooling = models.CharField(max_length=200, choices=SCHOOLING, blank=False, null=False)
    books = models.CharField(max_length=200, choices=QUANTITY, blank=False, null=False)
    work_reading = models.CharField(max_length=200, choices=YES_NO, blank=False, null=False)
    computer_reading=models.CharField(max_length=200, choices=YES_NO, blank=False, null=False)
    dexterity=models.CharField(max_length=200, choices=DEXTERITY, blank=False, null=False)
    source=models.CharField(max_length=200, choices=SOURCE, blank=False, null=False)
    other_experiments=models.CharField(max_length=200, choices=YES_NO, blank=False, null=False)



class InfoForm(ModelForm):
    class Meta:
        model = Information
        fields = ['subject','native_language','country', 'schooling','books','reading_language','work_reading','work_reading_language','computer_reading','dexterity','source', 'other_experiments']

class TrialSequence(models.Model):
    seq = models.CommaSeparatedIntegerField(max_length=10000)

class Text(models.Model):
    textNumber = models.IntegerField()
    textClass = models.IntegerField()
    body = models.CharField(max_length=100000)
    
    def __unicode__(self):
		return (self.body)
    
class TrialOption(models.Model):
    text = models.ForeignKey(Text)
    missing_words = models.CharField(max_length=10000) # JSON encoded list of integers.

class Trial(models.Model):
    subject = models.ForeignKey(Subject)
    trialOpt = models.ForeignKey(TrialOption)
    timestamp = models.DateTimeField(auto_now=True)
    initial_time = models.DateTimeField()
    words = models.CharField(max_length=10000) # JSON-encoded list of words.
    

