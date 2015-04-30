import psycopg2
import sys
import json
from collections import deque

# Connect to Chess Database
database='cloze_bruno'
host='calamaro.exp.dc.uba.ar'
user='XXXXXXX'
password='XXXXXXX'
connectStr="dbname='"+database+"' user='"+user+"' host='"+host+"' password='"+password+"'"

try:
        conn = psycopg2.connect(connectStr)
except:
        print "I am unable to connect to the database"
        exit(0)
print "Connected to database " + database + " on host " + host + " with user " + user + "."


#statement= "SELECT * from cloze_subject"
statement= "SELECT * from cloze_subject"

cur = conn.cursor()
cur.execute(statement)

res = cur.fetchall()

for r in res:
    id_subject = r[0]
    get_trials_from_subject = 'SELECT "trialOpt_id" from cloze_trial WHERE subject_id=%s'
    cur.execute(get_trials_from_subject,(id_subject,))
    subj_trials = cur.fetchall()
    ss = sorted(list(set(map(lambda x: x[0],subj_trials))))
    print 'longitud de ss', len(ss)
    seq_original = json.loads(r[6])
    jugados = seq_original[0:len(ss)]
    if not sorted(ss)==sorted(jugados):
        print 'Mal el subject: ', r
        print 'Seq orginial: ', str(seq_original)
        print 'Seq jugados: ', str(ss)
        print 'Seq original (solo cant. jugados): ', str(jugados)
        
        sys.exit()
    print 'Sujeto ' + str(id_subject) + ' ---> Cantidad de trials respondidos: ' + str(len(subj_trials)) + ' (' + str(ss) + ')'
    #print 'Original: ' + str(r[6]) + ' ----> Trials Jugados: ' + str(ss)
    
    los_que_sobran = seq_original[len(ss):]
    
    max_listas_T0 = 16
    max_listas_T1 = max_listas_T0 +17
    max_listas_T2 = max_listas_T1 +17
    max_listas_T3 = max_listas_T2 +17
    max_listas_T4 = max_listas_T3 +17
    max_listas_T5 = max_listas_T4 +17
    max_listas_T6 = max_listas_T5 +17
    max_listas_T7 = max_listas_T6 +17

    min_listas_T0_2015 = 1000
    max_listas_T0_2015 = min_listas_T0_2015 +20
    max_listas_T1_2015 = max_listas_T0_2015 +20
    max_listas_T2_2015 = max_listas_T1_2015 +20
    max_listas_T3_2015 = max_listas_T2_2015 +20
    max_listas_T4_2015 = max_listas_T3_2015 +20
    max_listas_T5_2015 = max_listas_T4_2015 +20
    max_listas_T6_2015 = max_listas_T5_2015 +20
    max_listas_T7_2015 = max_listas_T6_2015 +20

    if len(los_que_sobran)>0: # and len(filter(lambda x: max_listas_T4<x,los_que_sobran))>0:
        print 'Sobran: ', los_que_sobran
        
        indice = los_que_sobran.index(sorted(filter(lambda x: max_listas_T7<x,los_que_sobran))[0])
        # Hasta acá llegue... basicamente busco los indices no leidos que esten entre las listas viejas
        
        
        
        #print 'Indice: ', indice , ' ----> ' , los_que_sobran[indice]
        #~ dd = deque(los_que_sobran)
        #~ dd.rotate(-indice)
        #print 'Sobran rotado: ', str(dd)

        seq_final = json.dumps(seq_original[0:len(ss)] + list(dd))
        print seq_final
        
        update_statement = "UPDATE cloze_subject SET experiment_sequence=%s WHERE id=%s"
        print update_statement % (seq_final,id_subject)
        
        cur.execute(update_statement,(seq_final,id_subject))
        conn.commit()
