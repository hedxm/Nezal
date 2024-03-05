from rest_framework.response import Response
from rest_framework.views import APIView
from .pusher import pusher_client

# Create your views here.

class MessageAPIView(APIView):
    
    def get(self, request):
        # Extracting data from the request
        username = request.data.get('username')
        message = request.data.get('message')

        # Triggering the 'message' event on the 'chat' channel
        pusher_client.trigger('chat', 'message', {
            'username': username,
            'message': message,
        })
        
        # Responding with an empty response
        return Response({})
        
    # def post(self, request):
    #     messageReceived = request.data.get('message')
        
    #     messages = [
    #         {'username': 'Gepeto', 'message': "Soy Gepeto"},
    #         {'username': 'Usuario', 'message': messageReceived},
    #     ]
        
    #     return Response(messages)
    def post(self, request):
        # Buscar la forma de pasar el mensaje recibido a string
        messageReceived = request.data.get('message')
        messageReceivedStr = str(messageReceived)
        
        messages = [
            {'username': 'Gepeto', 'message': "Soy Gepeto"},
            {'username': 'Usuario', 'message': "Recibido: "+messageReceivedStr},
        ]
        
        return Response(messages)


