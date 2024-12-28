#!/usr/bin/env python
# coding: utf-8

# In[12]:


import inspect, pro, pickle, os
from appJar import gui



a1=None
if os.path.isfile('note.bin'): #vérifie si un fichier existe
    pass
else:
    fichier=open('note.bin',"w") #crée le fichier si il n'existe pas 
    fichier.close()
    
if os.stat('note.bin').st_size == 0: #si le fichier est vide, crée l'objet liste de note 
    a1=pro.liste_notes()
else:
    with open('note.bin', 'rb') as f: # sinon ouvre le fichier et charge l'objet liste de note
        a1 = pickle.load(f)

if os.path.isfile('profil.bin'): #vérifie si un fichier existe
    pass
else:
    fichier=open('profil.bin',"w") #crée le fichier si il n'existe pas
    fichier.close()
    
if os.stat('profil.bin').st_size == 0:  #si le fichier est vide, crée l'objet personne
    e1=pro.personne('Bernard','2m1',[1,1,1900],a1)
else:
    with open('profil.bin', 'rb') as f2: # sinon ouvre le fichier et charge l'objet liste de note
        e1 = pickle.load(f2)
u=gui()


mat=''
no=''
bra=''



u.addLabel('l1','Notes Chamblandes',3,0)
u.setLabelFont('l1', size=30, family="Times", weight='bold')
u.setSize('Fullscreen')
u.setBg('white')



def save():
    
    with open('note.bin','wb') as f: #utile pour le bouton sauvegarder, sauvegarde la liste de note a1 et la personne e1 dans deux fichiers
        pickle.dump(a1,f)
        
    with open('profil.bin','wb') as g:
        pickle.dump(e1,g)
        

        
def quit():
    
    u.stop()

def launch_subwindow(q):
    
    u.showSubWindow(q)
    
    
    
def page_matieres(a1):
    
    k=1
    
    for i in inspect.getmembers(a1):

        if not i[0].startswith('_') and not inspect.ismethod(i[1]): 
            u.startSubWindow(i[0])
            
            for j in i[1]:
                u.addLabel(j.matiere + j.sujet,j)

            q=f'moyenne de {i[0]}: '
            r=f'\nMoyenne de {i[0]}: ' + str(a1.moyennes_arrondies()[i[0]]) + '\n\n'
            
            u.addLabel(q,r,100)
            
            u.stopSubWindow()

            u.addButton(i[0],launch_subwindow,k,0)
            
            k+=1
            
            
            
def sub_ajouternote(name):
    """ajoute une note a la liste de note et met a jour la liste de note dans le profile -> la personne"""
    
    global a1, e1
    
    if name=='Soumettre': 
        
        matiere=u.getOptionBox('Matières1')
        sujet=u.getEntry('Sujet')
        resultat=float(u.getEntry('Résultat (x.y)'))
        coef=float(u.getEntry('Coefficient (x.y)'))
        type_note=u.getOptionBox('Type')
        

        date1=u.getDatePicker('Date du test')
        date=[int(str(date1)[8:10]),int(str(date1)[5:7]),int(str(date1)[0:4])]

        
        current_grade = pro.notes(matiere, sujet, resultat, coef, type_note, date)      
        
        a1.ajouter_note(current_grade)
        e1.notes=a1
        
        update_subwin_mat(matiere)
        update_subwin()
        
        u.hideSubWindow('Ajouter une note')
    
        
        
    else:
        
        u.clearEntry('Sujet')
        u.clearEntry('Résultat (x.y)')
        u.clearEntry('Coefficient (x.y)')
        u.setFocus('Sujet')     
o=0    

def update_subwin_mat(matiere):
 
    u.destroySubWindow(matiere)
    
    u.startSubWindow(matiere)
    
    for j in getattr(a1,matiere):
        u.addLabel(j.matiere + j.sujet,j)

    q=f'moyenne de {matiere}: '
    r=f'\nMoyenne de {matiere}: ' + str(a1.moyennes_arrondies()[matiere]) + '\n\n'

    u.addLabel(q,r)
    
    u.stopSubWindow()
        

def update_subwin():
    
    u.openSubWindow('Afficher le bulletin actuel')
    u.setLabel('bulletin',e1.bulletin())
    
    u.openSubWindow('Ajouter une note')
    u.changeOptionBox('Matières1',a1.matieres())
    
    u.openSubWindow('Supprimer une matière')
    u.changeOptionBox('Matières possibles',a1.matieres(),0,0)
    
    u.openSubWindow('Supprimer une note') 
    u.changeOptionBox("Matieres",a1.matieres(),0,0)
    u.setButton('afficher les notes',sub)
    

def ajo():
    global a1, e1, o
    
    no=u.getEntry('Nom de la matière')
    a1.ajouter_matiere(no)
    e1.notes=a1
    u.clearEntry('Nom de la matière',callFunction=True)
    u.hideSubWindow('Ajouter une matière')
    
    u.startSubWindow(no)
    u.addLabel('Aucune note' + str(o),'Aucune note')
    o+=1
    u.stopSubWindow()
    u.addButton(no,launch_subwindow,4,3)
    
    update_subwin()
    
    
def suppr_mat():
    global a1, e1
    
    m=u.getOptionBox('Matieres2')
    a1.supprimer_matiere(m)
    e1.notes=a1
    u.hideSubWindow('Supprimer une matière')
    u.hideButton(m)
    
    update_subwin()
    
def definir_subwindows():
    global e1, a1
    
    
    #1
    u.startSubWindow("Ajouter une note")

    u.setBg('green')
    u.setFg('white')
    u.setFont(16)
    u.addLabel('Nouvelle note','Nouvelle note')

    u.addOptionBox('Matières1',a1.matieres())
    u.addLabelEntry('Sujet')
    u.addLabelEntry('Résultat (x.y)')
    u.addLabelEntry('Coefficient (x.y)')
    u.addOptionBox('Type',['TE','TA','Voc','Oral'])
    u.addDatePicker('Date du test')
    u.setDatePickerRange("Date du test", 2015, 2021)

    u.addButtons(['Soumettre', 'Recommencer'],sub_ajouternote)
    u.stopSubWindow()


    #2
    u.startSubWindow('Supprimer une note')
    u.addOptionBox("Matieres2",a1.matieres(),0,0)
    u.addButton('afficher les notes',sub,0,1)
    u.stopSubWindow()


    #3
    u.startSubWindow('Afficher le bulletin actuel')
    u.addLabel('bulletin',e1.bulletin())
    u.stopSubWindow()
    
    
    u.startSubWindow('Ajouter une matière')
    u.addLabelEntry('Nom de la matière',0,0)
    u.addButton('Ajouter',ajo,0,1)
    u.stopSubWindow()


    u.startSubWindow('Supprimer une matière')
    u.addOptionBox('Matières possibles',a1.matieres(),0,0)
    u.addButton('Supprimer la matière',suppr_mat,0,1)
    u.stopSubWindow()
       
    
    
def changeTab(tabName):
    print("Changing to: ", tabName)
    u.setTabbedFrameSelectedTab("Tabs", tabName)
    print("done")

    
    
def supprimerlanote():
    global a1, e1
    
    mat=u.getOptionBox('Matières')
    note=u.getOptionBox('Notes')
    w=getattr(a1,mat)
    

    a1.supprimer_note(mat,note)
    e1.notes=a1
    u.hideSubWindow('Supprimer une note')
    
    uptdate_subwin(mat)

    update_subwin()
    
def sub():
    
    global mat

    mat=u.getOptionBox('Matieres2')
   
    notes=[]

    for i in inspect.getmembers(a1):
        if not i[0].startswith('_') and i[0].startswith(mat):
            for j in i[1]:
                notes.append(j.sujet)
                
    u.openSubWindow('Supprimer une note')
    u.addOptionBox("Notes",notes,1,0)
    u.addButton('supprimer la note',supprimerlanote,1,1)


    
def tab_matieres():
    
    page_matieres(a1)
    u.addLabel('Matières:','Matières:',0,0)
    u.addButton("Ajouter une note", launch_subwindow,0,1)
    u.addButton('Afficher le bulletin actuel',launch_subwindow,4,1)
    u.addButton('Supprimer une note',launch_subwindow,1,1)
    u.addButton('Ajouter une matière',launch_subwindow,2,1)
    u.addButton('Supprimer une matière',launch_subwindow,3,1)
    u.addButton('Sauvegarder', save, 0, 3)
    u.addButton('Quitter',quit,1,3)

    

def update_profile():
    
    global e1
    
    nom=u.getEntry('Prénom et nom')
    classe=u.getEntry('Classe')
    date_nais=u.getDatePicker('Date de naissance')
    date_nais=[int(str(date_nais)[8:10]),int(str(date_nais)[5:7]),int(str(date_nais)[:4])]
    u.infoBox('Succès','Profil mis à jour')
    e1=pro.personne(nom, classe, date_nais,a1)
    u.setLabel('Profil actuel',str(e1))
    
    update_subwin()
    
    
def tab_profil():   

    u.addLabelEntry('Prénom et nom')
    u.addLabelEntry('Classe')
    
    u.addDatePicker('Date de naissance')
    u.setDatePickerRange('Date de naissance', 1950, 2021)
    u.setDatePicker('Date de naissance')
    
    u.addButton('Enregistrer le profil', update_profile)
    u.addLabel('Profil actuel',str(e1))
    #u.addLabel('Statut',e1.exigences()) #apparemment exigences ne fonctionne pas, pour une raison inconnue... elle marche parfois, et c'est dommage de perdre cette option mais bon...
    
    
with u.tabbedFrame("Tabs"):
              
    with u.tab("Matières"):
        tab_matieres()

    with u.tab("Profil"):
        tab_profil()
    


if __name__=='__main__':
    
    definir_subwindows()

    u.addMenuList("Pages", ["Matières", "Profil"], changeTab)

    u.go()

