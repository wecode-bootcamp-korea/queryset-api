from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Prefetch, Count
from django.db.models.query import QuerySet

from .models      import Book, Store, Publisher
from decorators   import query_debugger

#################################
# Lazy Loading (지연 로딩)
#################################
class LazyLoadingCheckView(View):
    @query_debugger
    def get(self, request):
        queryset = Publisher.objects.get(id=10)

        return JsonResponse({'message' : 'SUCCESS' }, status=200)


#############################
# Caching
#############################
class CachingCheckView(View):
    @query_debugger
    def get(self, request):
        # queryset1, queryset2, queryset3는 즉시 호출(Eager Loading)되지 않음.
        queryset = Publisher.objects.filter(id=20).exclude(id=2).annotate(count=Count('book'))
        
        # Lazy Loading시 쿼리는 어디에 저장되어 있는가?
        print("queryset.query에 저장된 SQL문 :: ", queryset.query)

        # queryset이 평가될 때, 값을 QuerySet._result_cache에 저장한다.
        print("before queryset._result_cache :: ", queryset._result_cache)
#        queryset[0]
        print("after queryset._result_cache :: ", queryset._result_cache)
        list(queryset)
        print("final after queryset._result_cache :: ", queryset._result_cache)
##
#        queryset[0]
#        queryset[0]
#        queryset[0]
#        list(queryset)
#        
        return JsonResponse({'message' : 'SUCCESS' }, status=200)


#############################
# N + 1 Problems
#############################
class BooksWithAllMethodView(View):
    @query_debugger
    def get(self, request):
        print('Book에서 Publisher Instance에 접근하는 경우 <정참조>')
        queryset = Book.objects.all()
        books    = []

        # QuerySet이 평가(Evaluation)될 때, N + 1 Problems 발생
        # 모든 book을 조회하는 SQL 1번 실행 
        # book 하나당 publisher를 매번 조회하는 SQL N번 실행
        for book in queryset: 
            books.append({
                'id': book.id,
                'name': book.name,
                'publisher': book.publisher.name # book.publisher에 접근, 캐싱되지 않은 데이터이므로 query 발생
                }
            )

        return JsonResponse({'books_with_all_method' : books }, status=200)


########################################
# Eager Loading (select_related)
#######################################
class BooksWithSelectRelatedView(View):
    @query_debugger
    def get(self, request):
        queryset = Book.objects.all().select_related("publisher")
        print("queryset.query에 저장된 SQL문 :: ", queryset.query)

        books = []

        for book in queryset: 
            books.append({
                'id': book.id,
                'name': book.name,
                'publisher': book.publisher.name
                }
            )

        return JsonResponse({'books_with_all_method' : books }, status=200)


#############################
# N + 1 Problems
#############################
class StoresWithAllMethodView(View):
    @query_debugger
    def get(self, request):
        print(f'Store에서 Book Instance에 접근하는 경우 <역참조>')
        queryset = Store.objects.all()
        stores   = []

        for store in queryset: 
            books = [book.name for book in store.books.all()] 
            stores.append({
                'id': store.id,
                'name': store.name,
                'books': books
                }
            )

        return JsonResponse({'stores_with_all_method' : stores }, status=200)



########################################
# Eager Loading (prefetch_related)
#######################################
class StoresWithPrefetchRelatedView(View):
    @query_debugger
    def get(self, request):
        queryset = Store.objects.all().prefetch_related("books")
        print("queryset.query에 저장된 SQL문 :: ", queryset.query)
        print("final after queryset._result_cache :: ", queryset._result_cache)
        print("final after queryset._prefetch_related_lookups :: ", queryset._prefetch_related_lookups)
        stores = []

        for store in queryset:
            books = [book.name for book in store.books.all()]
            stores.append({'id': store.id, 'name': store.name, 'books': books})

        print("!!!! result_cache :: ", queryset._result_cache)

#        stores2 = []
#
#        for store in queryset:
#            books = [book.name for book in store.books.all()]
#            stores2.append({'id': store.id, 'name': store.name, 'books': books})
#
        return JsonResponse({'stores_with_prefetch_related' : stores }, status=200)


##################################################
# Eager Loading (prefetch_related ) when filtering
##################################################
class StoresWithPrefetchNoneObjectView(View):
    @query_debugger
    def get(self, request):
        queryset = Store.objects.all().prefetch_related("books")

        stores = []
        for store in queryset:
            total_books    = [book.name for book in store.books.all()]
            filtered_books = [book.name for book in store.books.filter(name='Book9991')]
            stores.append({
                'id'          : store.id,
                'name'        : store.name,
                'total_books' : total_books,
                'filterd_books' : filtered_books
            })

        return JsonResponse({'stores_with_prefetch_related' : stores }, status=200)



##################################################
# Eager Loading (prefetch_related ) when filtering
##################################################
class StoresWithPrefetchObjectView(View):
    @query_debugger
    def get(self, request):
        queryset = Store.objects.all().prefetch_related("books")
        queryset = Store.objects.prefetch_related(Prefetch('books', queryset=Book.objects.all()))

        print("queryset.query에 저장된 SQL문 :: ", queryset.query)
        print("final after queryset._result_cache :: ", queryset._result_cache)
        print("final after queryset._prefetch_related_lookups :: ", queryset._prefetch_related_lookups)

        stores = []

        for store in queryset:
#            total_books    = [book.name for book in store.books.all()]
#            filtered_books = [book.name for book in store.books.filter(name='Book9991')]

            total_books    = [book.name for book in store.total_books]
            filtered_books = [book.name for book in store.filtered_books]
            stores.append({
                'id'          : store.id,
                'name'        : store.name,
                'total_books' : total_books,
                'filterd_books' : filtered_books
            })

        return JsonResponse({'stores_with_prefetch_related' : stores }, status=200)
