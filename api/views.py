from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, SpamSerializer, UserSerializer, UserContactSerializer
from .models import Spam
from django.db.utils import IntegrityError
from django.db.models import Q, F, Count
from .models import Contact, User, Spam


class LoginView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LoginSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="phone_number",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="phone_number",
                        description="Valid phone_number for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class RegisterView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RegisterSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="phone_number",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="phone_number",
                        description="Valid phone_number for registration",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for registration",
                    ),
                ),
                coreapi.Field(
                    name="email",
                    required=False,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for registration",
                    ),
                ),
                coreapi.Field(
                    name="name",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="name",
                        description="Valid name for registration",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class SpamView(APIView):
    def post(self, request, phone_number):
        if request.user.phone_number == phone_number.strip():
            return Response({"message": "Can't self report"}, status=400)
        try:
            spam = Spam.objects.create(
                user=request.user, reported_number=phone_number)
        except IntegrityError:
            return Response({"message": "Already Reported"}, status=400)
        serializer = SpamSerializer(spam)
        return Response(serializer.data, status=201)

    def delete(self, request, phone_number):
        Spam.objects.filter(user=request.user,
                            reported_number=phone_number).delete()
        return Response({'message': 'Spam entry deleted successfully'}, status=204)

    def get(self, request, phone_number):
        spam = Spam.objects.filter(
            user=request.user, reported_number=phone_number).first()
        if spam:
            serializer = SpamSerializer(spam)
            return Response(serializer.data, status=200)
        return Response({'message': 'Spam entry not found'}, status=404)


class ContactsView(APIView):
    def get(self, request):
        key = request.GET.get('searchBy', '')
        value = request.GET.get('value', '')
        if key != 'name' and key != 'phone_number':
            return Response(None, status=400)
        results = []
        if key == 'name':
            data = Contact.objects.filter(
                saved_name__istartswith=value) | Contact.objects.filter(saved_name__icontains=value)

            data_users = User.objects.filter(
                name__istartswith=value) | User.objects.filter(name__icontains=value)
            for item in data.values():
                phone_number = item['saved_contact']
                name = item['saved_name']
                count = Spam.objects.filter(
                    reported_number=phone_number).count()
                list.append(results, {
                    "id": item['id'],
                    "phone_number": phone_number,
                    "name": name,
                    "count": count
                })
            for item in data_users.values():
                phone_number = item['phone_number']
                name = item['name']
                count = Spam.objects.filter(
                    reported_number=phone_number).count()
                list.append(results, {
                    "id": phone_number,
                    "phone_number": phone_number,
                    "name": name,
                    "count": count
                })
            print(results)
            return Response({'items': results}, status=200)

        if key == 'phone_number':
            try:
                user = User.objects.get(phone_number=value)
                serializer = UserSerializer(user)
                return Response({'user': serializer.data}, status=200)
            except User.DoesNotExist:
                pass

            data = Contact.objects.filter(saved_contact=value).values()
            for item in data:
                phone_number = item['saved_contact']
                name = item['saved_name']
                count = Spam.objects.filter(
                    reported_number=phone_number).count()
                list.append(results, {
                    'id': item['id'],
                    "phone_number": phone_number,
                    "name": name,
                    "count": count
                })
            return Response({'items': results}, status=200)


class ProfileView(APIView):
    def get(self, request, id):
        try:
            user = User.objects.get(phone_number=id)
            count = Spam.objects.filter(
                reported_number=user.phone_number).count()
            isContact = Contact.objects.filter(
                user_id=request.user.phone_number, saved_contact=user.phone_number).exists()
            email = None
            if isContact:
                email = user.email

            return Response({'user': {
                "name": user.name,
                "phone_number": user.phone_number,
                "spam": count, "email": email}}, status=200)
        except User.DoesNotExist:
            try:
                user = Contact.objects.get(id=id)
                count = Spam.objects.filter(
                    reported_number=user.saved_contact).count()
                return Response({'user': {
                    "name": user.saved_name,
                    "phone_number": user.saved_contact,
                    "spam": count}}, status=200)
            except Contact.DoesNotExist:
                return Response(None, 400)
