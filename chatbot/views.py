from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_POST
def chatbot_api(request):
    """Endpoint que responde a los mensajes del chat."""
    try:
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('message', '').lower()
    except Exception:
        return JsonResponse({'reply': 'Lo siento, ocurrió un error procesando tu mensaje.'})

    # Lógica sencilla de respuestas
    respuesta = "No entendí muy bien tu consulta. ¿Puedes escribirla de otra forma?"

    if 'fertilizante' in question or 'abono' in question:
        respuesta = ("Para fertilizantes contamos con productos para maíz, arroz y hortalizas. "
                     "Indica el cultivo y te doy una recomendación básica 😊.")
    elif 'horario' in question or 'abren' in question or 'atienden' in question:
        respuesta = ("Nuestro horario de atención es de lunes a viernes de 8:00 a 18:00 "
                     "y sábados de 8:00 a 13:00.")
    elif 'envío' in question or 'delivery' in question:
        respuesta = ("Realizamos envíos a nivel local. El costo de envío depende de la zona "
                     "y se calcula al momento de la compra.")
    elif 'plaga' in question or 'insecto' in question:
        respuesta = ("Si tienes problemas de plagas, cuéntame el cultivo y el tipo de plaga "
                     "para sugerirte un producto disponible en la tienda.")
    elif 'hola' in question or 'buenas' in question:
        respuesta = ("¡Hola! Soy Lena, tu asistente agrónoma virtual. "
                     "Puedo ayudarte con productos, horarios o envíos.")

    return JsonResponse({'reply': respuesta})
