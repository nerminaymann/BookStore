from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.templatetags.rest_framework import data

from .models import Book,Review
from .serializers import BookSerializer, Search_BookSerializer,ReviewSerializer, UserSerializer, RegisterSerializer, LoginSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
#from rest_framework.response import responses
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, serializers, status
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib import auth
from django.contrib.auth.models import User




# Create your views here.

#-------------------------------LOGIN AND REGISTRATION-------------------------------------

class SignUpAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return JsonResponse({
            "users": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        })


class SignInAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return JsonResponse({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return JsonResponse({
#         "user": UserSerializer(user, context=self.get_serializer_context()).data,
#         "token": AuthToken.objects.create(user)[1]
#         })
#
# # Login API
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginAPI, self).post(request, format=None)

#-------------------------------NEW AND TRENDING BOOKS-------------------------------------

class BooksAPIView(APIView):

    # IT MEANS LOGIN IS REQUIRED TO MAKE ANY API OPERATIONS
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = BookSerializer

    def get(self,request):
        books=Book.objects.all()
        serializer=BookSerializer(books,many=True)
        return JsonResponse(serializer.data,safe=False)

    def post(self,request):
        data=request.data
        serializer=BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)


class BookDetailAPIView(APIView):

    # IT MEANS LOGIN IS REQUIRED TO MAKE ANY API OPERATIONS
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = BookSerializer

    # RETURN THE RECORD TO AVOID REPEATING TRY EXCEPTION IN EVERY METHOD
    def get_object(self,pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return JsonResponse({"mseeage":"this book does not exist! "})


    def get(self,request,pk):
        # try:
        #     book = Book.objects.get(pk=pk)
        # except Book.DoesNotExist:
        #     return JsonResponse({"mseeage":"this record does not exist! "})
        book=self.get_object(pk)
        serializer=BookSerializer(book)
        return JsonResponse(serializer.data,status=201)

    def put(self,request,pk):
        # try:
        #     book = Book.objects.get(pk=pk)
        # except Book.DoesNotExist:
        #     return JsonResponse({"mseeage":"this record does not exist! "})
        book = self.get_object(pk)
        data=request.data
        serializer=BookSerializer(book,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

    def delete(self,request,pk):
        # try:
        #     book = Book.objects.get(pk=pk)
        # except Book.DoesNotExist:
        #     return JsonResponse({"mseeage":"this record does not exist! "})
        book = self.get_object(pk)
        book.delete()
        return JsonResponse({"message": "the book is deleted successfully"})


#-------------------------------METHODS-------------------------------------

# @csrf_exempt
@api_view(['GET','POST'])
def BookList(request):
    if request.method=='GET':
        books=Book.objects.all()
        serializer=BookSerializer(books,many=True)
        # if serializer is None:
        #     return HttpResponse({"message":"there is no books yet"})
        return JsonResponse(serializer.data,safe=False)

    elif request.method=='POST':
        # data=JSONParser().parse(request)
        data=request.data
        serializer=BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        JsonResponse(serializer.errors,status=400)

# @csrf_exempt
@api_view(['GET','PUT','DELETE'])
def BookDetail(request,pk):
    try:
      book=Book.objects.get(pk=pk)

    except Book.DoesNotExist:
        return JsonResponse({"message":"this book does not exist"},status=404)

    if request.method=='GET':
        serializer=BookSerializer(book)
        return JsonResponse(serializer.data)

    elif request.method=='PUT':
        # data = JSONParser().parse(request)
        data=request.data
        serializer = BookSerializer(book,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        JsonResponse(serializer.errors, status=400)

    elif request.method=='DELETE':
        book.delete()
        return JsonResponse({"message":"the record is deleted successfully"})


# ----------------------------------SEARCH FOR BOOKS-------------------------------

@api_view(['GET'])
# @authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def Search_forBook(request,title):
    try:
      book=Book.objects.get(title=title)
    except Book.DoesNotExist:
      return JsonResponse({"message":"this book does not exist"},status=404)
    serializer = Search_BookSerializer(book)
    return JsonResponse(serializer.data, status=201)


@api_view(['GET'])
# @authentication_classes([SessionAuthentication,BasicAuthentication])
@permission_classes([permissions.IsAuthenticated])
def Search_getBookDetail(request,pk):
    try:
      book=Book.objects.get(pk=pk)
    except Book.DoesNotExist:
      return JsonResponse({"message":"this book does not exist"},status=404)
    serializer = BookSerializer(book)
    return JsonResponse(serializer.data)

# ----------------------------------GIVING A REVIEW ON A BOOK-------------------------------

class ReviewsAPIView(APIView):

    # IT MEANS LOGIN IS REQUIRED TO MAKE ANY API OPERATIONS
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ReviewSerializer

    def get(self,request,pk):
        try:
            reviews = Review.objects.filter(pk=pk).all()
        except Review.DoesNotExist:
            return JsonResponse({"message": "there's no reviews yet"}, status=404)
        serializer = ReviewSerializer(reviews, many=True)
        return JsonResponse(serializer.data, safe=False)



    def post(self,request,pk):
        book=Book.objects.get(pk=pk)
        # print(book.pk)
        # current_user=request.user
        # user_id=current_user.pk
        # print(user_id)
        # self.request.session.create()
        # serializer=self.serializer_class(data=request.data)
        # serializer = ReviewSerializer(data=request.data)
        #
        # if serializer.is_valid():
        # #     # reviewer_id=user_id
        # #     # book_id=book.id
        #     reviewContent=request.POST['reviewContent']
        #     review=Review.objects.create(user_id=user_id,book_id=book.pk,reviewContent=reviewContent)
        #     review.save()
        #
        #     return JsonResponse(serializer.data,status=201)

        reviewContent = request.POST['reviewContent']
        user=request.user
        book_id=book

        review = Review.objects.create(user_id_id=user,book_id_id=book_id, reviewContent=reviewContent)
        # review.save()
        serializer = ReviewSerializer(data=review)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message":"the review is created successfully"}, status=201)
        return JsonResponse({"message":" error "},status=400)

        # data = request.data
        # serializer = ReviewSerializer(data=data)
        # if serializer.is_valid():
        #     new_review= serializer.save()
        #     new_review.user_id_id=request.user
        #     new_review.book_id_id=book
        #     new_review.save()
        #
        #     # context= {
        #     #     'review':
        #     # }
        #
        #     return JsonResponse(serializer.data, status=201)
        # return JsonResponse(serializer.errors, status=400)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #     # serializer.save(book_id=self.request.book)

