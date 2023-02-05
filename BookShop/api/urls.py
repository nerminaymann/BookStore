from django.urls import path,include
from .views import BookList,BookDetail,BooksAPIView,BookDetailAPIView,\
    Search_forBook,Search_getBookDetail,ReviewsAPIView,SignUpAPI, SignInAPI
from knox import views as knox_views

urlpatterns = [
    path('api/auth/', include('knox.urls')),
    # path('book/',BookList),
    path('book/',BooksAPIView.as_view()),
    # path('book/<int:pk>',BookDetail)
    path('book/<int:pk>',BookDetailAPIView.as_view()),
    path('book/review/<int:pk>',ReviewsAPIView.as_view()),
    # path('search/<title_pk>',Search_BookAPIView.as_view()),
    # path('search/<title_pk>/bookDetail',Search_BookAPIView.as_view())
    path('search/<title>',Search_forBook),
    path('search/<int:pk>/bookDetail',Search_getBookDetail),
    path('register/', SignUpAPI.as_view(), name='register'),
    path('login/', SignInAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),

]