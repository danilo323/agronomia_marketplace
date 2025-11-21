from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def _contiene(question, *palabras):
    """Helper para simplificar los if."""
    return any(p in question for p in palabras)

@csrf_exempt
@require_POST
def chatbot_api(request):
    """Endpoint que responde a los mensajes del chat."""
    try:
        data = json.loads(request.body.decode('utf-8'))
        question = data.get('message', '').lower()
    except Exception:
        return JsonResponse({'reply': 'Lo siento, ocurrió un error procesando tu mensaje.'})

    # Respuesta por defecto
    respuesta = (
        "No entendí muy bien tu consulta. 😅\n"
        "Puedes preguntarme sobre productos (acuícolas, pesqueros, ganaderos, vegetales), "
        "horarios, envíos, precios o cómo comprar."
    )

    # SALUDO / PRESENTACIÓN
    if _contiene(question, 'hola', 'buenas', 'buenos días', 'buenas tardes', 'buenas noches', 'hey','como estas','un gusto'):
        respuesta = (
            "¡Hola! 👋 Soy **Lena**, tu asistente agrónoma virtual de AgroMarket.\n\n"
            "Puedo ayudarte con:\n"
            "• Información de productos acuícolas, pesqueros, ganaderos y vegetales 🐟🥩🥕\n"
            "• Horarios de atención 🕗\n"
            "• Envíos y costos 🚚\n"
            "• Cómo comprar o registrarte en la web 🛒"
        )

    elif _contiene(question, 'quién eres', 'quien eres', 'qué eres', 'que eres', 'qué puedes hacer', 'ayuda'):
        respuesta = (
            "Soy **Lena**, el chatbot de AgroMarket 🌱.\n"
            "Estoy diseñada para orientarte sobre los productos de la página, horarios, envíos, "
            "recomendaciones básicas y dudas generales sobre la tienda."
        )

    # INFORMACIÓN GENERAL DE PRODUCTOS / CATEGORÍAS
    elif _contiene(question, 'qué venden', 'que venden', 'productos', 'catálogo', 'catalogo'):
        respuesta = (
            "En AgroMarket ofrecemos productos frescos directamente del campo y del mar:\n\n"
            "• **Productos Acuícolas**: Tilapia, camarón de cultivo, trucha arcoíris 🐟\n"
            "• **Productos Pesqueros**: Atún fresco, langosta, calamar 🦞\n"
            "• **Productos Ganaderos**: Carne de res premium, leche fresca, queso artesanal 🥩🥛🧀\n"
            "• **Productos Vegetales**: Zanahorias orgánicas, tomates de invernadero, lechuga hidropónica 🥕🍅🥬\n\n"
            "Si quieres, pregúntame por una categoría o un producto específico 😉."
        )

    # CATEGORÍA ACUÍCOLA
    elif _contiene(question, 'acuícola', 'acuicola', 'tilapia', 'camarón', 'camaron', 'trucha'):
        if _contiene(question, 'precio', 'cuánto cuesta', 'cuanto cuesta', 'valor'):
            # Precio específico si menciona un producto
            if 'tilapia' in question:
                respuesta = "La **tilapia fresca** tiene un precio de **$5.50 por kg** en nuestra tienda acuícola. 🐟"
            elif 'camarón' in question or 'camaron' in question:
                respuesta = "El **camarón de cultivo** tiene un precio de **$12.00 por kg**. 🦐"
            elif 'trucha' in question:
                respuesta = "La **trucha arcoíris** tiene un precio de **$8.00 por kg**. 🐟"
            else:
                respuesta = (
                    "En productos acuícolas manejamos precios aproximados entre **$5.50 y $12.00 por kg**, "
                    "dependiendo si es tilapia, camarón o trucha."
                )
        else:
            respuesta = (
                "En la sección de **Productos Acuícolas** encontrarás:\n"
                "• Tilapia fresca (cultivo sostenible, $5.50/kg)\n"
                "• Camarón de cultivo libre de antibióticos ($12.00/kg)\n"
                "• Trucha arcoíris de agua dulce ($8.00/kg)\n\n"
                "Todos criados bajo estándares de calidad y control de agua."
            )

    # CATEGORÍA PESQUERA
    elif _contiene(question, 'pesquero', 'pesquera', 'pescado', 'marisco', 'atún', 'atun', 'langosta', 'calamar'):
        if _contiene(question, 'precio', 'cuánto cuesta', 'cuanto cuesta', 'valor'):
            if 'atún' in question or 'atun' in question:
                respuesta = "El **atún fresco** tiene un precio de **$15.00 por kg**. 🐟"
            elif 'langosta' in question:
                respuesta = "La **langosta** tiene un precio de **$25.00 por kg**. 🦞"
            elif 'calamar' in question:
                respuesta = "El **calamar** tiene un precio de **$7.50 por kg**. 🦑"
            else:
                respuesta = (
                    "En productos pesqueros los precios van desde **$7.50 hasta $25.00 por kg**, "
                    "dependiendo si es calamar, atún o langosta."
                )
        else:
            respuesta = (
                "En **Productos Pesqueros** contamos con:\n"
                "• Atún fresco de pesca responsable ($15.00/kg)\n"
                "• Langosta del Pacífico capturada artesanalmente ($25.00/kg)\n"
                "• Calamar fresco de pesca diaria ($7.50/kg)\n\n"
                "Todos obtenidos con técnicas sostenibles y de calidad."
            )

    # CATEGORÍA GANADERA
    elif _contiene(question, 'ganadero', 'ganadera', 'carne', 'res', 'leche', 'queso'):
        if _contiene(question, 'precio', 'cuánto cuesta', 'cuanto cuesta', 'valor'):
            if 'carne' in question or 'res' in question:
                respuesta = "La **carne de res premium** tiene un precio de **$9.00 por kg**. 🥩"
            elif 'leche' in question:
                respuesta = "La **leche fresca** tiene un precio de **$1.20 por litro**. 🥛"
            elif 'queso' in question:
                respuesta = "El **queso artesanal** tiene un precio de **$6.50 por kg**. 🧀"
            else:
                respuesta = (
                    "En productos ganaderos manejamos precios desde **$1.20 por litro** (leche) "
                    "hasta **$9.00 por kg** (carne de res premium)."
                )
        else:
            respuesta = (
                "En **Productos Ganaderos** ofrecemos:\n"
                "• Carne de res premium grass-fed ($9.00/kg)\n"
                "• Leche fresca pasteurizada ($1.20/litro)\n"
                "• Queso artesanal tradicional ($6.50/kg)\n\n"
                "Procedentes de ganado en pastoreo libre y manejo responsable."
            )

    # CATEGORÍA VEGETAL
    elif _contiene(question, 'vegetal', 'vegetales', 'hortalizas', 'zanahoria', 'zanahorias', 'tomate', 'tomates', 'lechuga'):
        if _contiene(question, 'precio', 'cuánto cuesta', 'cuanto cuesta', 'valor'):
            if 'zanahoria' in question or 'zanahorias' in question:
                respuesta = "Las **zanahorias orgánicas** tienen un precio de **$2.00 por kg**. 🥕"
            elif 'tomate' in question or 'tomates' in question:
                respuesta = "Los **tomates de invernadero** tienen un precio de **$2.50 por kg**. 🍅"
            elif 'lechuga' in question:
                respuesta = "La **lechuga hidropónica** tiene un precio de **$1.80 por unidad**. 🥬"
            else:
                respuesta = (
                    "En productos vegetales los precios van desde **$1.80 por unidad** (lechuga hidropónica) "
                    "hasta **$2.50 por kg** (tomate de invernadero)."
                )
        else:
            respuesta = (
                "En **Productos Vegetales** tenemos:\n"
                "• Zanahorias orgánicas sin pesticidas ($2.00/kg)\n"
                "• Tomates de invernadero con riego por goteo ($2.50/kg)\n"
                "• Lechuga hidropónica ultra limpia ($1.80/unidad)\n\n"
                "Cultivados con técnicas sostenibles y controladas."
            )

    # HORARIOS
    elif _contiene(question, 'horario', 'abren', 'atienden', 'hora de atención', 'hora de atencion'):
        respuesta = (
            "Nuestro **horario de atención** es:\n"
            "• Lunes a viernes: **08:00 a 18:00**\n"
            "• Sábados: **08:00 a 13:00**\n"
            "Domingos y feriados solo atendemos pedidos en línea. 🕗"
        )

    # ENVÍOS / DELIVERY
    elif _contiene(question, 'envío', 'envios', 'envío', 'delivery', 'envian', 'envío a domicilio', 'envio a domicilio'):
        respuesta = (
            "Realizamos **envíos a nivel local** 🚚.\n\n"
            "• El costo de envío depende de la zona.\n"
            "• Se calcula al momento de la compra.\n"
            "• Los productos se envían en condiciones de frío y empaque adecuados "
            "para mantener la frescura."
        )

    # CÓMO COMPRAR / CARRITO / SIMULACIÓN
    elif _contiene(question, 'cómo comprar', 'como comprar', 'comprar', 'hacer un pedido', 'hacer mi pedido', 'añadir', 'agregar al carrito', 'simular compra'):
        respuesta = (
            "Para comprar en AgroMarket sigue estos pasos 🛒:\n\n"
            "1️⃣ En la página principal, busca la tarjeta del producto que te interese.\n"
            "2️⃣ Haz clic en el botón **“Agregar”** de ese producto.\n"
            "3️⃣ Completa tus datos y la información de envío.\n"
            "4️⃣ Confirma el pedido y el sistema calculará el costo de envío.\n\n"
            "Si solo es una simulación, puedes usar el botón de compra como prueba sin finalizar el pago."
        )

    # REGISTRO / INICIO DE SESIÓN
    elif _contiene(question, 'registrar', 'registrarme', 'crear cuenta', 'registro', 'sign up', 'signup'):
        respuesta = (
            "Para **registrarte** en AgroMarket:\n\n"
            "1️⃣ En la parte superior derecha haz clic en **“Registrarse”**.\n"
            "2️⃣ Completa tus datos (nombre, correo, contraseña).\n"
            "3️⃣ Confirma el registro y luego podrás iniciar sesión y hacer pedidos.\n"
        )

    elif _contiene(question, 'iniciar sesión', 'iniciar sesion', 'login', 'entrar a mi cuenta', 'no puedo entrar'):
        respuesta = (
            "Para **iniciar sesión**:\n\n"
            "1️⃣ En la parte superior derecha haz clic en **“Iniciar Sesión”**.\n"
            "2️⃣ Ingresa tu correo y contraseña.\n"
            "3️⃣ Si olvidaste tu contraseña, puedes solicitar una recuperación desde esa misma sección."
        )

    # CONTACTO
    elif _contiene(question, 'contacto', 'contactarlos', 'teléfono', 'telefono', 'whatsapp', 'correo', 'email'):
        respuesta = (
            "Nuestros datos de **contacto** son:\n\n"
            "• 📧 Correo: **info@agromarket.ec**\n"
            "• 📱 Teléfono/WhatsApp: **+593 99 123 4567**\n\n"
            "También puedes escribirnos por el formulario de la página o por redes sociales."
        )

    # UBICACIÓN / DÓNDE ESTÁN
    elif _contiene(question, 'dónde están', 'donde estan', 'ubicados', 'ubicación', 'ubicacion'):
        respuesta = (
            "Somos un marketplace que conecta productores locales con clientes. 🌱\n"
            "Atendemos principalmente a nivel local, y los envíos se coordinan según la zona.\n"
            "Para más detalles, puedes escribirnos por WhatsApp o correo."
        )

    # PREGUNTAS AGRONÓMICAS BÁSICAS: FERTILIZANTES / PLAGAS
    elif _contiene(question, 'fertilizante', 'abono'):
        respuesta = (
            "Sobre **fertilizantes** puedo darte una recomendación general.\n\n"
            "Indícame:\n"
            "• El **cultivo** (por ejemplo: maíz, arroz, tomate, lechuga)\n"
            "• La **etapa** (siembra, crecimiento, floración, cosecha)\n\n"
            "y te doy una orientación básica 😊 (recuerda que siempre es ideal consultar a un agrónomo de forma presencial)."
        )

    elif _contiene(question, 'plaga', 'insecto', 'gusano', 'hongos', 'hongo', 'enfermedad en las plantas'):
        respuesta = (
            "Si tienes problemas de **plagas o enfermedades**, necesito un poco más de información:\n\n"
            "• ¿Qué cultivo es? (maíz, tomate, hortalizas, etc.)\n"
            "• ¿Qué síntomas ves? (manchas, hojas amarillas, agujeros, moho, etc.)\n\n"
            "Con eso puedo orientarte de forma general y sugerirte qué tipo de producto buscar."
        )

    return JsonResponse({'reply': respuesta})
