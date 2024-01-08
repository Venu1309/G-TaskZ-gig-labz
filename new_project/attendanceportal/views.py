from django.shortcuts import render
from attendanceportal.models import CustomUser, OTP
from django.conf import settings
import random
from django.utils import timezone
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models.signals import post_save
from rest_framework import viewsets
from django.dispatch import receiver
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated



#@api_view(['POST'])
# Create your views here.
# def index(request):
#     if request.method== 'POST':
#         username=request.POST.get("user_name")
#         password=request.POST.get("pass_word")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             print("before login",request.user)
#             login(request,user)
#             print("after login",request.user)
#             return Response({'message': 'Logged in successfully'}, status=status.HTTP_201_CREATED)
#         else:
#             pass

#@permission_classes([IsAuthenticated])
@api_view(['POST'])
def index(request):
    if request.method == 'POST':
        email = request.data.get("email")
        user = CustomUser.objects.get(email=email)
        if user:  
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
            otp_instance = OTP.objects.create(otp=otp, user=user)  # Create OTP instance and associate it with the user
            print(otp_instance)
            send_mail(
                'Your OTP for Login',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'OTP sent to email'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_otp(request):
    if request.method == 'POST':
        otp_entered = request.data.get("otp")
        email = request.data.get('email')
        if not otp_entered or not email:
            return Response({'message': 'Please provide OTP and email'}, status=status.HTTP_400_BAD_REQUEST)
        userid=CustomUser.objects.get(email=email)
        user_otp = OTP.objects.filter(user=userid).last()  # Fetch OTP instance associated with the email
        if user_otp != 0:
            if otp_entered == user_otp.otp:
            # Delete OTP instance upon successful verification
                token=Token.objects.get_or_create(user=userid)
                print(token[0].__dict__)
                user_otp.delete()
    # Perform login or return success message
                return Response({
                    'message': 'Logged in successfully',
                    'user_id': userid.id,
                    'username': userid.username,
                    'email': userid.email,
        # Include other user details as needed
                }, status=status.HTTP_200_OK)        
            else:
    # Handle invalid OTP scenario
                return Response({'error': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Please provide OTP and email'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_view(request):
    email=request.data.get('email')
    try:
        user_profile = CustomUser.objects.get(email=email)

    except CustomUser.DoesNotExist:
        user_profile = None

    user_data = {
        'id': user_profile.id,
        'username': user_profile.username,
        'email': user_profile.email,
        'first_name': user_profile.first_name,
        'last_name': user_profile.last_name,
        'phone_number': user_profile.phonenumber if user_profile else None,
    }
    return Response(user_data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def update_view(request):
    #user=request.user
    id=request.data.get('id')
    try:
        user_profile = CustomUser.objects.get(id=id)  # Fetch user profile data
    except CustomUser.DoesNotExist:
        user_profile = None

    if not user_profile:
        # Create a user profile if it doesn't exist
        user_profile = CustomUser(id=id)
    #user_data = request.data.get('user', {})
    user_profile.first_name = request.data.get('first_name', user_profile.first_name)
    user_profile.last_name = request.data.get('last_name', user_profile.last_name)
    user_profile.email = request.data.get('email', user_profile.email)
    user_profile.date_joined = timezone.now()
    user_profile.phonenumber = request.data.get('phonenumber', user_profile.phonenumber)
    user_profile.image = request.data.get('image', user_profile.image)
    # Update other profile details
    user_profile.save()

    return Response({'message': 'User data updated successfully'}, status=status.HTTP_200_OK)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)
#         print(Token.key)

# class AttendanceView(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     permission_classes = [IsAuthenticated]
