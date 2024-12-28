#!/usr/bin/env python
# coding: utf-8

# In[43]:


import inspect, math


calendrier_mois=[None, 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin','Juillet','Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']


class notes:

    """
    
    La classe notes est celle qui organise chaque note individuellement. Elle prend pour attributs:
    -la matière de la note en question (str)
    -son sujet (str)
    -sa valeur (float)
    -son coefficient (float)
    -son type (TE, TA, oral ou voc)
    -sa date (liste [jj,mm,aaaa])
    
    """
    
    def __init__(self, matiere, sujet, valeur, coefficient, type_note, date):
       
        self.matiere=matiere
        self.sujet=sujet
        self.valeur=valeur
        self.coef=coefficient
        self.type_note=type_note
        self.date=date
        
    
    def __repr__(self):
        
        return  f"{self.matiere}, {self.sujet}, {self.valeur}, coef {self.coef}, {self.date[0]}/{self.date[1]}/{self.date[2]}\n"


    def __str__(self):

        date = f'{self.date[0]} ' + f'{calendrier_mois[self.date[1]]} ' + f'{self.date[2]}'

        a=''

        a+='{:<25}{:>15}'.format('Test de:', self.matiere) + '\n'
        a+='{:<25}{:>15}'.format('À propos de:', self.sujet) + '\n'
        a+='{:<25}{:>15}'.format('Résultat:', self.valeur) + '\n'
        a+='{:<25}{:>15}'.format('Coefficient:',self.coef) + '\n'
        a+='{:<25}{:>15}'.format('Type de note:', self.type_note) + '\n'
        a+='{:<25}{:>15}'.format('Date:', date)

        return a

    
    def tripardate(obj):
        """cette fonction sert à attribuer une valeur numérque aux dates dans le but de pouvoir ensuite les trier plus tard, dans la fonction __str__ de la classe liste_notes
        elle prend donc en fonction un objet et en utilise son attribut date"""
        return obj.date[0] + obj.date[1]*100 + obj.date[2]*10000
    
    
    def arrondi_multiple_0_5(a):
        """cette fonction sert à arrondir n'importe quel nombre à un multiple de 0.5, selon les règles des notes, c'est-à-dire 4.25 -> 4.5
        elle prend en paramètre n'importe quel nombre, qui n'est même pas forcément un attribut"""
    
        if (a/0.25)%4==1: #correction d'une erreur
            a+=0.1

        return round(a/0.5)*0.5
    


class liste_notes:
    
    """la classe liste_notes sert à rassembler toutes les notes d'un élève, c'est ainsi une sorte de 'trousseau de notes'. On remarquera qu'elle ne possède pas d'init, et c'est parce qu'à sa création, elle n'a pas d'attribut: il est donc possible de créer une classe liste_notes sans y ajouter du même coup des notes ou des matières
    ses attributs seront donc chaque matière de l'élève, qui eux-mêmes seronts des listes comprenant chaque note, issue de la classe précédente"""
        
    def __str__(self):
        """évidemment, son str, qui indique comment l'afficher en cas de print"""
          
        w=''

        for i in self.matieres():
            w+= str(i) + ':\n\n'

            liste_notesde_i=[]
            
            for j in getattr(self,i):
                liste_notesde_i.append(j)

            liste_notesde_i.sort(key=notes.tripardate)

            for k in liste_notesde_i:
                w+=str(k) + '\n\n'

            w+='\n'

        return w
        
        
    def ajouter_matiere(self, matiere):
        """ainsi, la fonciton ajouter_matiere sert justement à ajouter des matières à cette fameuse classe, c'est-à-dire des attributs, classes encore vides, portant le nom de la branche
        elle prend donc un paramètre, qui deviendra le nom du nouvel attribut"""
        
        setattr(self,matiere,[])
    
    
    def supprimer_matiere(self,matiere):
    
        """symétriquement, il est aussi possible de supprimer des branches de la classe. le paramètre indiquera donc de quelle branche on parle"""
        
        delattr(self,matiere)
        
        
    def ajouter_note(self,note):
        """cette méthode permet d'ajouter une note à une branche. on remarquera qu'elle ne prend qu'un paramètre, la note, car soit la branche existe déjà, auquel cas on puisera dans l'attribut 'branche' de la note pour savoir où la placer dans liste_note, ou bien on créera un attribut selon la même méthode"""
        
        b=getattr(note,'matiere')
        
        if hasattr(self,b)==False:
            
            self.ajouter_matiere(b)
            
        a=getattr(self,b)
        a.append(note)


    def supprimer_note(self,matiere,nom):
        """cette méthode permet d'effacer une certaine branche, appelée nom et issue de la matière"""
        
        a=getattr(self,matiere)
        
        for i in a:
            if i.sujet==nom:
                a.remove(i)
                
                
    def matieres(self):
        """la fonction matieres retourne la liste de toutes les matières de l'objet de la classe liste_notes"""
        
        matieres=[]

        for i in inspect.getmembers(self):
            if not i[0].startswith('_') and not inspect.ismethod(i[1]): 
                matieres.append(i[0])

        return matieres
    
    
    def moyennes(self):
        """la méthode moyennes calcule chaque moyenne et renvoie un dictionnaire composé de chaque moyenne, dont la clé est le nom de la matière"""
        
        moyennes={}
        
        for i in self.matieres():
                    
            somme_ponderations=0
            somme_coefs=0
            
            somme_ta=0
            nombre_ta=0
            
            somme_oral=0
            nombre_oral=0
            
            somme_voc=0
            nombre_voc=0
            
            for j in getattr(self,i):
                
                if j.type_note== 'TA':
                    somme_ta+=j.valeur
                    nombre_ta+=1
                    
                elif j.type_note=='Oral':
                    somme_oral+=j.valeur
                    nombre_oral+=1
                    
                elif j.type_note=='Voc':
                    somme_voc+=j.valeur
                    nombre_voc+=1
                
                else:
                    somme_coefs+=j.coef
                    ponderation=j.valeur*j.coef
                    somme_ponderations+=ponderation
                
            if nombre_ta!=0:
                moyenne_ta=notes.arrondi_multiple_0_5(somme_ta/nombre_ta)
                somme_coefs+=1
                somme_ponderations+=moyenne_ta
                
            if nombre_oral!=0:
                moyenne_oral=notes.arrondi_multiple_0_5(somme_oral/nombre_oral)
                somme_coefs+=1
                somme_ponderations+=moyenne_oral
                
            if nombre_voc!=0:
                moyenne_voc=notes.arrondi_multiple_0_5(somme_voc/nombre_voc)
                somme_coefs+=1
                somme_ponderations+=moyenne_voc
            
            if somme_coefs!=0:
                moyenne_i=somme_ponderations/somme_coefs
                
                moyennes[i]=moyenne_i
                
            else:
                moyennes[i]=0
    
        return moyennes
   
    
    def moyennes_arrondies(self):
        """la méthode moyennes_arrondies reprend le dictionnaire de moyennes, mais cette fois arrondit chaque valeur et retourne un nouveau dictionnaire"""
        
        moy_arr={}
        
        total=0
        
        for i in self.moyennes():
            
            moy_arr[i]=notes.arrondi_multiple_0_5(self.moyennes()[i])
            total+=moy_arr[i]
            
        moy_arr['Total']=total
            
        return moy_arr
              


class personne:
    """et finalement, la troisième classe, la classe personne. Celle-ci prend en attributs un nom, une classe, une date de naissance et une série de notes, qui, elle, est issue de la classe précédente liste_notes"""
    
    def __init__(self,nom,classe,date_naissance,notes):
    
        
        self.nom=nom
        self.classe=classe
        self.date_naissance=date_naissance
        self.notes=notes
    
    
    def __str__(self):
    
        date12 = f'{self.date_naissance[0]} ' + f'{calendrier_mois[self.date_naissance[1]]} ' + f'{self.date_naissance[2]}'
    
        a=''
    
        a+='{:<25}{:>15}'.format('Prénom et nom:', self.nom) + '\n'
        a+='{:<25}{:>15}'.format('Classe:', self.classe) + '\n'
        a+='{:<25}{:>15}'.format('Date de naissance:', date12) + '\n'
        
        
        return a
    
    
    def bulletin(self):
        """la méthode bulletin affiche le bulletin de la personne qui possède toutes ces notes. c'est donc une méthode de la classe personne, qui retourne du texte"""
        
        total=0
        
        text=''
        
        for i in self.notes.moyennes_arrondies():
            
            moy=self.notes.moyennes_arrondies()[i]
            
            total+=moy
                        
            text+='{:<15}{:>20}'.format(i,moy) + '\n'
        
        text+='\n{:<15}{:>20}'.format('Total',total)
        
                  
        return text 
       
        
                  
    def double_compensation(self):
              
        somme_ecarts_4=0
        
        for i in self.notes.moyennes_arrondies():
                  
            moy=self.notes.moyennes_arrondies()[i]
                  
            if moy<4:
                  somme_ecarts_4+=4-moy
                  
        total_determinant=self.notes.moyennes_arrondies()['Total']-somme_ecarts_4
                  
        if total_determinant<4*14:
            return False
                
        else:
            return True 
                  
    
    def panier(self):
        
        moy=0
        
        moy+=self.notes.moyennes_arrondies['math']
        moy+=self.notes.moyennes_arrondies['francais']
        moy+=self.notes.moyennes_arrondies['os']
        
        moy_lang=1/2*(self.notes.moyennes_arrondies['anglais']+self.notes.moyennes_arrondies['allemand'])
        
        moy+=moy_lang
        
        if moy<4*4:
            return False
        
        else:
            return True
        
        
    def exigences(self):
        
        reussite=1
        
        if self.classe[0]=='3':
            
            if self.double_compensation():
                reussite*=1
            
            else:    
                reussite*=0
             
        else:
            
            if self.notes.panier():
                reussite*=1
            
            else:
                reussite*=0
                
        if self.notes.moyennes_arrondies()['Total']<4*len(self.notes.matieres()):
            reussite*=0            
        else:
            reussite*=1
        
        if reussite == 0:
        
            a="Statut de l'année: échec"
        
        else: 
        
            a="Statut de l'année: succès"
    
            
        return a
