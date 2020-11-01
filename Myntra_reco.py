import json
import firebase_admin
from firebase_admin import credentials, firestore

'''
Filters for different types of garments
Tshirt : sleeve(1 for full, or 0 for half), pattern (3 for solid, 2 for striped, 1 for printed or 0 for block), collar (3 for polo neck, 2 for vneck, 1 for round neck, or 0 for other)
Shirt : sleeve(1 for full, or 0 for half), pattern (3 for solid, 2 for striped, 1 for printed or 0 for checks), occasion (1 for formal, 0 for casual)
winter : type(2 for jacket, 1 for sweater, or 0 for sweatshirt), fit(1 for baggie, 0 for slim), neck (2 for round neck, 1 for Henley, 0 for hooded)
suit : type(1 for single breasted or 0 for double breasted), pattern (2 for stripes, 1 for solid, 0 for other), lapel (2 for peak, 1 for notch or 0 for other)
'''

def new_rank(garment_db):
  garment_db = {k: v for k, v in sorted(garment_db.items(), key=lambda item: item[1])}
  i = 1
  for key in garment_db:
    garment_db[key] = i
    i+= 1
  return garment_db
def weight_matrix(garment_counter):
  a ={}
  for key in garment_counter:
      a[key] = max(garment_counter[key])  
  total =0
  for key in a:
      total += a[key]
  for key in a:
      a[key] = a[key]/total
  return a
def function_score_estimator(garment_database,key,garment_type,garment_counter):
     # print(key)
      if (garment_type == "winter"):
        #type
       # print(garment_database[key])
        if (garment_database[key][0] == "jacket"):
          garment_counter["type"][0] += 1
        elif (garment_database[key][0] == "sweater"):
          garment_counter["type"][1] += 1
        else:
          garment_counter["type"][2] += 1

        if (garment_database[key][1] == "baggie"):
         garment_counter["fit"][0] += 1
        else:
         garment_counter["fit"][1] += 1

        if (garment_database[key][2] == "round"):
         garment_counter["neck"][0]+= 1
        elif (garment_database[key][2] == "henley"):
          garment_counter["neck"][1]+= 1
        else:
          garment_counter["neck"][2]+= 1

      #below for suits
      elif (garment_type == "suit"):
        if (garment_database[key][0] == "single-breasted"):
          garment_counter["type"][0] += 1
        else:
          garment_counter["type"][1] += 1

        if (garment_database[key][1] == "stripes"):
          garment_counter["pattern"][0] += 1
        elif (garment_database[key][1] == "solid"):
          garment_counter["pattern"][1] += 1
        else:
          garment_counter["pattern"][2] += 1

        if (garment_database[key][2] == "peak"):
          garment_counter["lapel"][0] += 1

        elif (garment_database[key][2] == "notch"):
          garment_counter["lapel"][1] += 1

        else:
          garment_counter["lapel"][2] += 1

      #Below for shirts   
      elif (garment_type == "shirt"):
        if (garment_database[key][0] == "full"):
          garment_counter["sleeves"][0] += 1
        else:
          garment_counter["sleeves"][1] += 1

        if (garment_database[key][1] == "solid"):
          garment_counter["pattern"][0] += 1
        elif (garment_database[key][1] == "stripes"):
          garment_counter["pattern"][1] += 1
        elif (garment_database[key][1] == "printed"):
          garment_counter["pattern"][2] += 1
        else:
          garment_counter["pattern"][3] += 1
          
        if (garment_database[key][2] == "formal"):
          garment_counter["occasion"][0] += 1
        else:
          garment_counter["occasion"][1] += 1
      
      #tshirt    
      else:
        if (garment_database[key][0] == "full"):
          garment_counter["sleeves"][0] += 1
        else:
          garment_counter["sleeves"][1] += 1

        if (garment_database[key][1] == "solid"):
          garment_counter["pattern"][0] += 1
        elif (garment_database[key][1] == "stripes"):
          garment_counter["pattern"][1] += 1
        elif (garment_database[key][1] == "printed"):
          garment_counter["pattern"][2] += 1
        else:
          garment_counter["pattern"][3] += 1

        if (garment_database[key][2] == "polo-neck"):
          garment_counter["collar"][0] += 1
        elif (garment_database[key][2] == "v-neck"):
          garment_counter["collar"][1] += 1  
        elif (garment_database[key][2] == "round-neck"):
          garment_counter["collar"][2] += 1 
        else:
          garment_counter["collar"][3] += 1 
        
      return garment_counter

userid='JIbQxBGVCxPu803klzNJcqqkWIu1'
mentshirtlist=dict()
menshirtlist=dict()
menwinterlist=dict()
mensuitlist=dict()
usermtshirtlist=list()
usermshirtlist=list()
usermwinterlist=list()
usermsuitlist=list()
try:
    app = firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate('myntra-match-66bca-firebase-adminsdk-scdbn-0cba3513f5.json')
    firebase_admin.initialize_app(cred)
db=firestore.client()
products=db.collection('PRODUCTS')
menprod=products.document('men')
womenprod=products.document('women')
#Get the User data
swipes=db.collection('SWIPES')
user=swipes.document(userid)
tshirts=user.collection(u'men__tShirt').stream()
#Store only right swiped stuff
for tshirt in tshirts:
    if (tshirt.to_dict()['swipe']=="right"):
      usermtshirtlist.append(f'{tshirt.id}')
shirts=user.collection(u'men__shirt').stream()
for shirt in shirts:
    if (shirt.to_dict()['swipe']=="right"):
      usermshirtlist.append(f'{shirt.id}')
winters=user.collection(u'men__winter').stream()
for winter in winters:
    if (winter.to_dict()['swipe']=="right"):
      usermwinterlist.append(f'{winter.id}')
suits=user.collection(u'men__suits').stream()
for suit in suits:
    if (suit.to_dict()['swipe']=="right"):
      usermsuitlist.append(f'{suit.id}')
#print(usermsuitlist)

#Get the products data
#Features data still to be added
tshirts=menprod.collection(u'men__tShirt').stream()
for tshirt in tshirts:
    mentshirtlist[f'{tshirt.id}']=[tshirt.to_dict()["sleeves"],tshirt.to_dict()["pattern"],tshirt.to_dict()["collar"]]
shirts=menprod.collection(u'men__shirt').stream()
for shirt in shirts:
    menshirtlist[f'{shirt.id}']=[shirt.to_dict()["Sleeve"],shirt.to_dict()["Pattern"],shirt.to_dict()["Occasion"]]
winters=menprod.collection(u'men__winter').stream()
for winter in winters:
    menwinterlist[f'{winter.id}']=[winter.to_dict()["type"],winter.to_dict()["fit"],winter.to_dict()["neck"]]
suits=menprod.collection(u'men__suits').stream()
for suit in suits:
    mensuitlist[f'{suit.id}']=[suit.to_dict()["type"],suit.to_dict()["pattern"],suit.to_dict()["lapel"]]

'''
Filters for different types of garments
Tshirt : sleeve(1 for full, or 0 for half), pattern (3 for solid, 2 for striped, 1 for printed or 0 for block), collar (3 for polo neck, 2 for vneck, 1 for round neck, or 0 for other)
Shirt : sleeve(1 for full, or 0 for half), pattern (3 for solid, 2 for striped, 1 for printed or 0 for checks), occasion (1 for formal, 0 for casual)
winter : type(2 for jacket, 1 for sweater, or 0 for sweatshirt), fit(1 for baggie, 0 for slim), neck (2 for round neck, 1 for Henley, 0 for hooded)
suit : type(1 for single breasted or 0 for double breasted), pattern (2 for stripes, 1 for solid, 0 for other), lapel (2 for peak, 1 for notch or 0 for other)
'''

if __name__ == '__main__':
      garments = {}
      counter = 0
      usermshirtlist = [] #delete later
      for key in mensuitlist:
        usermsuitlist.append(key)
        counter +=1
        if (counter == 4):
          break
      counter = 0
      for key in menwinterlist:
        usermwinterlist.append(key)
        counter +=1
        if (counter == 4):
          break
      counter = 0
      for key in menshirtlist:
        usermshirtlist.append(key)
        counter +=1
        if (counter == 4):
          break    
      for key in mentshirtlist:
        usermtshirtlist.append(key)
        counter +=1
        if (counter == 4):
          break     
      garments["winter"] = usermwinterlist  #contains keys of all the products that the user swiped on in the winter sections
      garments["suit"] =  usermsuitlist
      garments["tshirt"] = usermtshirtlist
      garments["shirt"] = usermshirtlist
      #print("yes")
      #finding the user preference of category. In the final output we will display 5 of most desirable class, 3 of second most and 2 of the third most desirable
      garments_new = sorted(garments, key=lambda k: len(garments[k]), reverse=True)
      #print(garments)
      #counter list to keep track of the number of filters that have been swiped right on
      winter_counter = {}
      winter_preference = {"type": {"jacket" : 0, "sweater" : 0, "sweatshirt":0}, "fit":{"baggie" : 0,"slim" : 0}, "neck":{"round": 0,"henley" : 0 , "hooded": 0}}
      winter_counter["type"] = [0,0,0] #3 elements each keeping count of a different type
      winter_counter["fit"] = [0,0]
      winter_counter["neck"] = [0,0,0]

      Tshirt_counter = {}
      Tshirt_preference = {"sleeves": {"full" : 0, "half" : 0}, "pattern":{"solid" : 0,"stripes" : 0,"printed" : 0,"block" : 0}, "collar":{"polo-neck": 0,"round-neck" : 0 , "v-neck": 0,"other": 0}}
      Tshirt_counter["sleeves"] = [0,0]
      Tshirt_counter["pattern"] = [0,0,0,0]
      Tshirt_counter["collar"] = [0,0,0,0]

      shirt_counter = {}
      shirt_preference = {"sleeves": {"full" : 0, "half" : 0}, "pattern":{"solid" : 0,"stripes" : 0,"printed" : 0,"checks" : 0}, "occasion":{"formal": 0,"casual" : 0 }}
      shirt_counter["sleeves"] = [0,0]
      shirt_counter["pattern"] = [0,0,0,0]
      shirt_counter["occasion"] = [0,0]

      #add more filters for suits
      suit_counter = {}
      suit_preference = {"type":{"single-breasted":0,"double-breasted":0},"pattern": {"stripes":0,"solid":0,"other":0},"lapel":{"peak":0,"notch":0,"other":0}}
      suit_counter["type"] = [0,0]
      suit_counter["pattern"] = [0,0,0]
      suit_counter["lapel"] = [0,0,0]
     
      for key in garments:
        #print(key)
        if (key == "winter"):
          for i in range(len(garments[key])):
            
            temp = garments[key][i]
            winter_counter = function_score_estimator(menwinterlist,temp,key,winter_counter)
            #print(winter_counter)
        elif (key == "suit"):
          for i in range(len(garments[key])):
            temp = garments[key][i]
            suit_counter = function_score_estimator(mensuitlist,temp,key,suit_counter)
        elif (key == "tshirt"):
          for i in range(len(garments[key])):
            temp = garments[key][i]
            if (temp == ' iWokhVENSIzzAfnMEzST'):
              temp = 'iWokhVENSIzzAfnMEzST'
            Tshirt_counter = function_score_estimator(mentshirtlist,str(temp),key,Tshirt_counter)
        else:
          for i in range(len(garments[key])):
            temp = garments[key][i]
            if (temp == ' QmmsDgYrdYIeLw4TVt0B'):
              temp = 'QmmsDgYrdYIeLw4TVt0B'
            shirt_counter = function_score_estimator(menshirtlist,temp,key,shirt_counter)
  
      #code for finding out the top 2 filters based on user preference 
      counter = 0
      for key in winter_preference:
        i =0
        for key1 in winter_preference[key]:
          winter_preference[key][key1] = winter_counter[key][i]
          i += 1
        winter_preference[key] = new_rank(winter_preference[key]) 
      for key in shirt_preference:
        i =0
        for key1 in shirt_preference[key]:
          shirt_preference[key][key1] = shirt_counter[key][i]
          i += 1
        shirt_preference[key] = new_rank(shirt_preference[key])
      for key in Tshirt_preference:
        i =0
        for key1 in Tshirt_preference[key]:
          Tshirt_preference[key][key1] = Tshirt_counter[key][i]
          i += 1
        Tshirt_preference[key] = new_rank(Tshirt_preference[key])
      for key in suit_preference:
        i =0
        for key1 in suit_preference[key]:
          suit_preference[key][key1] = suit_counter[key][i]
          i += 1
        suit_preference[key] = new_rank(suit_preference[key]) 

      
      #######################    
      T = 2
      display_lst = []
      for key in garments_new:
        if (key == "winter"):
          w0 = weight_matrix(winter_counter)
          
          for key1 in menwinterlist:
            temp_type = menwinterlist[key1][0]
            temp_fit = menwinterlist[key1][1]
            temp_neck = menwinterlist[key1][2]

            fin_val = (winter_preference["type"][temp_type]*w0["type"]) + (winter_preference["fit"][temp_fit]*w0["fit"]) + (winter_preference["neck"][temp_neck]*w0["neck"])
            
            if (fin_val > T):
              display_lst.append(key1)
        elif (key == "tshirt"):
          w1 = weight_matrix(Tshirt_counter)
          
          for key1 in mentshirtlist:
            temp_sleeve = mentshirtlist[key1][0]
            temp_pattern = mentshirtlist[key1][1]
            temp_collar = mentshirtlist[key1][2]

            fin_val = (Tshirt_preference["sleeves"][temp_sleeve]*w1["sleeves"]) + (Tshirt_preference["pattern"][temp_pattern]*w1["pattern"]) + (Tshirt_preference["collar"][temp_collar]*w1["collar"])
           
            if (fin_val > T):
              display_lst.append(key1)
        elif (key == "shirt"):
          w2 = weight_matrix(shirt_counter)
    
          for key1 in menshirtlist:
            temp_sleeve = menshirtlist[key1][0]
            temp_pattern = menshirtlist[key1][1]
            temp_occasion = menshirtlist[key1][2]

            fin_val = (shirt_preference["sleeves"][temp_sleeve]*w2["sleeves"]) + (shirt_preference["pattern"][temp_pattern]*w2["pattern"]) + (shirt_preference["occasion"][temp_occasion]*w2["occasion"])
            
            if (fin_val > T):
              display_lst.append(key1)
        else:
          w3 = weight_matrix(suit_counter)  
           
          for key1 in mensuitlist:
            temp_type = mensuitlist[key1][0]
            temp_pattern = mensuitlist[key1][1]
            temp_lapel = mensuitlist[key1][2]
            fin_val = (suit_preference["type"][temp_type]*w3["type"]) + (suit_preference["pattern"][temp_pattern]*w3["pattern"]) + (suit_preference["lapel"][temp_lapel]*w3["lapel"])
            
            if (fin_val > T):
              display_lst.append(key1)
      print("The list is : ")
      print(display_lst)                                                                                                                                    

