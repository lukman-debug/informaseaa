from django.shortcuts import render

# Create your views here.
import requests
from django.http import JsonResponse

def chatgpt_api_view(request):
    if request.method == 'GET':
        # Ambil parameter dari request GET
        text = request.GET.get('text', 'default_text')
        prompt = request.GET.get('prompt', 'default_prompt')
        
        # URL API
        url = f"https://api.ryzendesu.vip/api/ai/chatgpt?text={text}&prompt={prompt}"
        
        # Header untuk request
        headers = {
            'accept': 'application/json',
        }
        
        try:
            # Kirim permintaan ke API
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            # Return response API ke frontend
            return JsonResponse({
                "success": response_data.get('success', False),
                "response": response_data.get('response', 'No response received'),
            }, status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Handle error jika API gagal dipanggil
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)
    
def chatgpt(request):
    return render(request, 'chatgpt.html')