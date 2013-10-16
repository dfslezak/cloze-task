import sqlite3
# import psycopg2

f = open('textos.csv','r')

# ------------------------------------------
conn = sqlite3.connect('cloze.sqlite3')



# ------------------------------------------
#database='cloze_task'
#host='calamaro.exp.dc.uba.ar'
#user='dfslezak'
#password='????'
#connectStr="dbname='"+database+"' user='"+user+"' host='"+host+"' password='"+password+"'"

#conn = psycopg2.connect(connectStr)
# ------------------------------------------




cur = conn.cursor()

db_text = []
for l in f.readlines():
    sl = l.split(',',3)
    id = int(sl[0])
    textnum = int(sl[1])
    textclass = int(sl[2])
    text = unicode(sl[3][1:-2],'iso-8859-15')
    #print id, textnum, textclass, text
    
    db_text.append((id,textnum,textclass,text))

for i in db_text:
    print i[0]
cur.executemany('INSERT INTO cloze_text VALUES (?,?,?,?)',db_text)
#cur.executemany('INSERT INTO cloze_text VALUES (%s,%s,%s,%s)',db_text)
conn.commit()


f.close()

cur = conn.cursor()

f = open('exp.csv','r')
db_exp = []
for l in f.readlines():
    sl = l.split(',',3)
    id = int(sl[0])
    text_id = int(sl[1])
    missing = sl[2].replace(';',',')[0:-1]
    #print id, text_id, missing
    
    db_exp.append((id,text_id,missing))
    
cur.executemany('INSERT INTO cloze_trialoption VALUES (?,?,?)',db_exp)
#cur.executemany('INSERT INTO cloze_trialoption VALUES (%s,%s,%s)',db_exp)
conn.commit()

f.close()

cur = conn.cursor()

f = open('72listasdeexps.csv','r')
db_seq = []
for l in f.readlines():
    
    db_seq.append(('[' + l.strip() + ']',))

print db_seq

cur.executemany('INSERT INTO cloze_trialsequence (seq) VALUES (?)',db_seq)
#cur.executemany('INSERT INTO cloze_trialsequence (seq) VALUES (%s)',db_seq)
conn.commit()

