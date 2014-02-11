# -*- coding: UTF-8 -*-
from django.http import HttpResponse
from cloze.models import *
from django.template import RequestContext,Context, loader
from django.utils import simplejson
import calendar,datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

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
		#~ print gen_seq
		sub = Subject(email=email,age=ed,gender=gen,original_ip=ip,experiment_sequence=seq,sequence_number=seq_num)
		sub.save()
		
		
	t = loader.get_template('trial.html')
	finalizado = True
	text_partition = ''
	trial = 0
	etiqueta_trial = "Finalizado"
	primer_trial=False 
	#~ info = Information(native_lenguaje='native_lenguaje',country='country', schooling='schooling',reading_lenguaje='reading_lenguaje',books='books',work_reading='work_reading',computer_reading='computer_reading',dexterity='dexterity',source='source', other_experiments='other_experiments')
	#~ info.save()
	
	try:
		seq = json.loads(sub.experiment_sequence)
		todos_los_trials= list(Trial.objects.all())
		trialOpt_sub = []
		for j in todos_los_trials:
			if j.subject == sub:
				trialOpt_sub.append(j.trialOpt_id)

		indices = []
		if not trialOpt_sub:
			next_trial_ind = 0
		else:
			trialOpt_sub_unique = set(trialOpt_sub)		
			for i in trialOpt_sub_unique:
				ind = seq.index(i)
				indices.append(ind)
			max_ind = max(indices)
			next_trial_ind = max_ind + 1
				
		
		
		next_trial = TrialOption.objects.get(id=seq[next_trial_ind])
		trialOption = TrialOption.objects.filter(id=seq[next_trial_ind]).get()
		body = trialOption.text.body.split()
		missing_words = json.loads(trialOption.missing_words)
		text_partition=[]
		last_index = 0;
		
		# Agrega todas las partes a text_partition
		for i in missing_words:
			text_partition.append(' '.join(body[last_index:i]))
			last_index = i

		# Agrega la última parte partes a text_partition	
		text_partition.append(' '.join(body[missing_words[-1]:]))
		
		#parto el texto en los <p> </p> para que el Djando me reconozca los párrafos sin hacer cagadas		
		partes= []
		for textoAdentro in text_partition:
			partes.append( textoAdentro.replace("<p>", " ").split("</p>") )
		text_partition = partes

				
		valor = seq[next_trial_ind]

		indice =  ([i for i,x in enumerate(seq) if x == valor][0])+1

		
		trial = seq[next_trial_ind]
		etiqueta_trial = str(indice-1) +' de '+str(len(seq))
		finalizado=False
		
		
		secuencia_posta = map(lambda x: body[int(x)], missing_words)
	
		
		#si estoy en el caso donde el primer input o el ultimo, son la primer o ultima palabra
		#tengo que meter un texto vacio antes y dsp

		#~ print "body", body
		if (secuencia_posta[0]==0): text_partition = [""] + text_partition
		#print "cuenta loca",len(body)
		if (secuencia_posta[-1]==len(body)): text_partition.append("")
		
		
		# Formulario  de preguntas luego del primer texto
		if (next_trial_ind == 0):
			primer_trial=True
		else:
			primer_trial=False
		
	except:
		pass			
	
 	if (len(text_partition)==0): text_partition = ['error','error','error','error','error']
	initial_trial = request.GET.get('initial_trial', 'true')

	#~ print zip( text_partition[0:-1], range(0,len(text_partition) ))

	form_Information=InfoForm() 
	c=RequestContext(request,{
	'finalizado':finalizado,
	'texto_con_input': zip( text_partition[0:-1], range(0,len(text_partition))),
	'texto_final':  (text_partition[-1],len(text_partition)-1),
	'usuario':sub.email,
	'trial':trial,
	'cant_pal': len(secuencia_posta)-1,
	'cant_textos': range(len(text_partition)),
	'etiqueta_trial':etiqueta_trial,
	'secuencia_posta':  zip(range(0,len(text_partition)), secuencia_posta),
	'initial_trial': initial_trial,
	'primer_trial': primer_trial,
	'form': form_Information,
	'missing_words': missing_words,
	#~ 'native_lenguaje': {{native_lenguaje}}
	})
	return HttpResponse(t.render(c))

def subir(request):
	q = request.GET
	sub = Subject.objects.get(email=q['email'])
	trialOption = TrialOption.objects.get(id=q['trial'])

	trials_llenados = Trial.objects.filter(subject=sub,trialOpt=trialOption)


	#dt = datetime.datetime(q.get('initTime'))
	dt = datetime.datetime.fromtimestamp(float(q.get('initTime'))/1000.0)
	#initTime = json.loads(q.get('initTime'))
	t = q.getlist('tiempos[]')
	p = q.getlist('palabras[]')


	wt = [(p[i].encode('utf-8'),t[i]) for i in range(len(t))] 
	trial = Trial(subject=sub,trialOpt=trialOption,initial_time=dt,words=json.dumps(wt))
	trial.save()

	return HttpResponse('')

def subirInformation(request):
    q = request.GET
    sub = Subject.objects.get(email=q['email'])
    #~ print 'sujeto', sub

    infos = Information.objects.filter(subject=sub)
    #~ print 'infos', infos

    if len(infos)==0:

        nat_lang = q['native_language']
        country=q['country']
        schooling=q['schooling']
        books=q['books']
        read_lan=q['reading_language']
        work_reading=q['work_reading']
        work_read_lan=q['work_reading_language']
        comp_read=q['computer_reading']
        dex=q['dexterity']
        source=q['source']
        other_exp=q['other_experiments']
        
        info = Information(subject=sub, native_language=nat_lang, country=country,schooling=schooling,books=books,work_reading=work_reading,reading_language=read_lan,work_reading_language=work_read_lan,computer_reading=comp_read,dexterity=dex,source=source,other_experiments=other_exp)
        info.save()

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
               
        epoch = timezone.make_aware(datetime.datetime.utcfromtimestamp(0), timezone.get_default_timezone())
        print t.initial_time
        print epoch
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

def bajar_sujetos(request):
    
    csv = ''
    for s in Subject.objects.all():
        
        try:
            line = "'" + str(s.email) + "','" + str(s.age) + "','" + str(s.gender) + "','" + str(s.information.native_language) + "','" +    str(s.information.reading_language) + "','" + str(s.information.work_reading_language) + "','" + str(s.information.country) + "','" +            str(s.information.schooling) + "','" + str(s.information.books) + "','" + str(s.information.work_reading) + "','" +            str(s.information.computer_reading) + "','" + str(s.information.dexterity) + "','" + str(s.information.source) + "','" + str(s.information.other_experiments) + "'" 
            csv = csv + (line.encode('iso-8859-1')+'\n')
        except ObjectDoesNotExist:
            print 'User incomplete: ' + str(s.email)
        #c = c + 1
    

    # generate the file
    response = HttpResponse(csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=subject_log.csv'
    return response
