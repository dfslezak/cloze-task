# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from cloze.models import *
from django.template import RequestContext,Context, loader
from django.utils import simplejson
import calendar,datetime

import re
import json

def home(request):
	form_subject = SubjectForm()
	
	t = loader.get_template('login.html')
	c=RequestContext(request,{
		'form': form_subject})
	
	return HttpResponse(t.render(c))

def trial(request):
	
	email_get = request.GET.get('email', '')
	#print 'email_get:',email_get
	
	if ( email_get==''):
		return HttpResponse("Error por mail no valido")
		
		#Seteo cookie
		#~ max_age = days_expire * 24 * 60 * 60 
		#~ expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
		#~ response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
		
	secuencia_posta= ['error','error','error','error','error','error','error',]	
	texto_final = secuencia_posta
	body = ""
	missing_words = ""
	email = email_get
	#print 'Email es', email
	
	try:
		sub = Subject.objects.get(email= email)
		#print "existe usuario"
	except Subject.DoesNotExist:
		print "NO existe usuario"
		ed = request.GET.get('edad',-1)
		gen = request.GET.get('gender','')
		ip = request.META.get('REMOTE_ADDR','0.0.0.0')
		(seq_num, gen_seq) = Subject.generate_sequence()
		seq = json.dumps(gen_seq)
		#print gen_seq
		sub = Subject(email=email,age=ed,gender=gen,original_ip=ip,experiment_sequence=seq,sequence_number=seq_num)
		sub.save()
		
	t = loader.get_template('trial.html')
	finalizado = True
	text_partition = ''
	trial = 0
	etiqueta_trial = "Finalizado"
	primer_trial=False 
	try:
		next_trial_ind = Trial.objects.filter(subject=sub).count() 
		seq = json.loads(sub.experiment_sequence)
		next_trial = TrialOption.objects.get(id=seq[next_trial_ind])
		trialOption = TrialOption.objects.filter(id=seq[next_trial_ind]).get()
		body = trialOption.text.body.split()
		missing_words = json.loads(trialOption.missing_words)
		text_partition=[]
		last_index = 0;
		for i in missing_words:
			text_partition.append(' '.join(body[last_index:i]))
			#print text_partition
			last_index = i
				
		#parto el texto en los <p> </p> para que el Djando me reconozca los párrafos sin hacer cagadas
 
		partes= []
		for textoAdentro in text_partition:
			partes.append( textoAdentro.replace("<p>", " ").split("</p>") )
		text_partition = partes
		
		text_partition.append(' '.join(body[missing_words[-1]:]))

		valor = seq[next_trial_ind]

		indice =  ([i for i,x in enumerate(seq) if x == valor][0])+1

		
		trial = seq[next_trial_ind]
		etiqueta_trial = str(indice) +' de '+str(len(seq))
		finalizado=False
		
		
		secuencia_posta = map(lambda x: body[int(x)], missing_words)
		
		
		#si estoy en el caso donde el primer input o el ultimo, son la primer o ultima palabra
		#tengo que meter un texto vacio antes y dsp

		#print "body", body
		if (secuencia_posta[0]==0): text_partition = [""] + text_partition
		#print "cuenta loca",len(body)
		if (secuencia_posta[-1]==len(body)): text_partition.append("")
		
		# Formulario  de preguntas luego del primer texto
	
		if (next_trial_ind == 0):
			primer_trial=True
			#~ t = loader.get_template('Information.html')		
			#~ form_Information=InfoForm()
			#~ d=RequestContext(request,{
				#~ 'form': form_Information,
				#~ 'usuario':sub.email,
				#~ 'etiqueta_trial':etiqueta_trial,
				#~ })
			#~ return HttpResponse(t.render(d))
	
	
	except:
		pass			
	
 	
	if (len(text_partition)==0): text_partition = ['error','error','error','error','error']
	initial_trial = request.GET.get('initial_trial', 'true')

	#~ print zip( text_partition[0:-1], range(0,len(text_partition) ))

	form_Information=InfoForm() 
	c=RequestContext(request,{
	'finalizado':finalizado,
	'texto_con_input': zip( text_partition[0:-1], range(0,len(text_partition) )),
	'texto_final':  (text_partition[-1],len(text_partition)-1),
	'usuario':sub.email,
	'trial':trial,
	'cant_pal': len(secuencia_posta)-1,
	'cant_textos': range(len(text_partition)),
	'etiqueta_trial':etiqueta_trial,
	'secuencia_posta':  zip(range(0,len(text_partition)), secuencia_posta),
	'initial_trial': initial_trial,
	'primer_trial': primer_trial,
	'form': form_Information
	})
	#print zip( text_partition[0:], range(0,len(text_partition) ))
	return HttpResponse(t.render(c))

def subir(request):
    q = request.GET
    sub = Subject.objects.get(email=q['email'])
    trialOption = TrialOption.objects.get(id=q['trial'])

    trials_llenados = Trial.objects.filter(subject=sub,trialOpt=trialOption)
    if len(trials_llenados)==0:

        #dt = datetime.datetime(q.get('initTime'))
        dt = datetime.datetime.fromtimestamp(float(q.get('initTime'))/1000.0)
        #initTime = json.loads(q.get('initTime'))
        t = q.getlist('tiempos[]')
        p = q.getlist('palabras[]')


        wt = [(p[i].encode('utf-8'),t[i]) for i in range(len(t))] 
        trial = Trial(subject=sub,trialOpt=trialOption,initial_time=dt,words=json.dumps(wt))
        trial.save()

    return HttpResponse('')

def bajar_todo(request):
    
    csv = ''
    for t in Trial.objects.all().order_by('subject','id'):
        s = t.subject
        to = t.trialOpt
        
        if s.sequence_number==None:
            seq = sorted(json.loads(s.experiment_sequence))
            filtered_ts = filter(lambda x: sorted(json.loads(x.seq)) == seq,TrialSequence.objects.all())
            seq_num = filtered_ts[0].id
        else:
            seq_num = s.sequence_number
        
        te = to.text
        mw = json.loads(to.missing_words)
               
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = t.initial_time - epoch 
        ep = long(delta.total_seconds()*1000) + 3600 * 1000 * 3 # GMT-3 correction
        
        pals = json.loads(t.words)
        c = 0
        for p,pt in pals:
            p_limpia = p.replace(',','').replace('.','').replace(';','').replace(':','').replace("'","")
            pal_original = te.body.split()[mw[c]].replace(',','').replace('.','').replace(';','').replace(':','').replace("'","")
            line = "'" + str(t.id) + "','" + str(s.id) + "','" + str(s.email) + "','" + str(seq_num) + "','" + str(to.id) + "','" + str(te.textClass) + "','" + str(te.textNumber) + "','" + str(ep) + "','" + p_limpia + "','" + pal_original + "','" + pt + "','" + str(c) + "','" + str(s.age) + "'" 
            csv = csv + (line.encode('iso-8859-1')+'\n')
            c = c + 1
    
    # generate the file
    response = HttpResponse(csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=log.csv'
    return response
