import os,json,re,requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Hospital

RED=['chest pain','unconscious','severe bleeding','difficulty breathing','stroke','बेहोश','सीने में तेज दर्द','सांस लेने में कठिनाई','खून बहना']

def local_triage(s):
 t=s.lower()
 flags=[x for x in RED if x in t]
 if flags:return {'priority':'RED','recommendation':'Immediate emergency evaluation','reasoning':'Potential high-risk symptoms detected.','red_flags':flags}
 return {'priority':'YELLOW','recommendation':'Prompt clinical assessment','reasoning':'No automatic critical red flag detected; AI/clinician assessment recommended.','red_flags':[]}

@csrf_exempt
def triage(request):
 if request.method!='POST': return JsonResponse({'detail':'POST required'},status=405)
 data=json.loads(request.body or '{}'); symptoms=data.get('symptoms','')
 result=local_triage(symptoms)
 # Optional Groq call. Falls back safely to deterministic red-flag screening.
 key=os.getenv('GROQ_API_KEY')
 if key:
  try:
   prompt=f'''Classify emergency triage for India. Return JSON only with priority RED/YELLOW/GREEN, recommendation, reasoning, red_flags. Symptoms: {symptoms}'''
   r=requests.post('https://api.groq.com/openai/v1/chat/completions',headers={'Authorization':f'Bearer {key}'},json={'model':os.getenv('GROQ_MODEL','llama-3.1-8b-instant'),'messages':[{'role':'user','content':prompt}],'temperature':0.1},timeout=2)
   content=r.json()['choices'][0]['message']['content']
   result=json.loads(re.sub(r'^```json|```$','',content.strip()))
  except Exception: pass
 hs=Hospital.objects.filter(emergency_available=True).order_by('-icu_beds')[:5]
 result['nearest_hospitals']=[{'id':h.id,'name':h.name,'available_beds':h.available_beds(),'capabilities':h.capabilities} for h in hs]
 return JsonResponse(result)

def hospitals(request):
 hs=Hospital.objects.all()
 return JsonResponse({'results':[{'id':h.id,'name':h.name,'city':h.city,'available_beds':h.available_beds(),'capabilities':h.capabilities} for h in hs]})
