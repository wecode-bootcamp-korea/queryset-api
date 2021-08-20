"""queryset_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from books.views import BooksWithAllMethodView, BooksWithSelectRelatedView, StoresWithAllMethodView, StoresWithPrefetchRelatedView, StoresWithPrefetchObjectView, StoresWithPrefetchNoneObjectView, LazyLoadingCheckView, CachingCheckView

urlpatterns = [
    path('check-cache', CachingCheckView.as_view()),
    path('check-lazy-loading', LazyLoadingCheckView.as_view()),
    path('books-with-all-method', BooksWithAllMethodView.as_view()),
    path('books-with-select-related', BooksWithSelectRelatedView.as_view()),
    path('stores-with-all-method', StoresWithAllMethodView.as_view()),
    path('stores-with-prefetch-related', StoresWithPrefetchRelatedView.as_view()),
    path('stores-with-prefetch-none-object', StoresWithPrefetchNoneObjectView.as_view()),
    path('stores-with-prefetch-object', StoresWithPrefetchObjectView.as_view()),
]

