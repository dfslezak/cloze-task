from django.db import models
from django.db.models import Max, Count
import random
import json

# Create your models here.
class Subject(models.Model):
    email = models.EmailField()
    age = models.IntegerField(null=True)
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
        seq_base0 = map(lambda x: x-1,seq_base1)
        random.shuffle(seq_base0)
        return (ts.id,seq_base0)       

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
    

