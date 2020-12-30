from django.views import View
from .models      import Book, Store
from django.http  import JsonResponse
from decorators   import query_debugger
from django.db.models    import Prefetch

class BooksWithAllMethodView(View):
    @query_debugger
    def get(self, request):
        print('Book에서 Publisher Instance에 접근하는 경우 <정참조>')
        queryset = Book.objects.all()
        books = []
        for book in queryset: 
            books.append({
                'id': book.id,
                'name': book.name,
                'publisher': book.publisher.name # book.publisher에 접근, 캐싱되지 않은 데이터이므로 query 발생
                }
            )
        return JsonResponse({'books_with_all_method' : books }, status=200)

class BooksWithSelectRelatedView(View):
    @query_debugger
    def get(self, request):
        print('Book에서 Publisher Instance에 접근하는 경우 <정참조>')
        queryset = Book.objects.select_related("publisher").all()
        books = []
        for book in queryset: 
            books.append({
                'id': book.id,
                'name': book.name,
                'publisher': book.publisher.name
                }
            )
        return JsonResponse({'books_with_all_method' : books }, status=200)


# Store(1) : Book(M)
# Store에서 Book Instance에 접근하는 경우 <역참조>
class StoresWithAllMethodView(View):
    @query_debugger
    def get(self, request):
        print(f'Store에서 Book Instance에 접근하는 경우 <역참조>')
        queryset = Store.objects.all()
        stores = []
        for store in queryset: 
            books = [book.name for book in store.books.all()] 
            stores.append({
                'id': store.id,
                'name': store.name,
                'books': books
                }
            )
        return JsonResponse({'stores_with_all_method' : stores }, status=200)

class StoresWithPrefetchRelatedView(View):
    @query_debugger
    def get(self, request):
        print(f'Store에서 Book Instance에 접근하는 경우 <역참조>')
        queryset = Store.objects.prefetch_related("books").all()
        stores = []
        for store in queryset:
            books = [book.name for book in store.books.all()]
            stores.append({'id': store.id, 'name': store.name, 'books': books})

        return JsonResponse({'stores_with_prefetch_related' : stores }, status=200)


class StoresWithPrefetchNoneObjectView(View):
    @query_debugger
    def get(self, request):
        print(f'Store에서 Book Instance에 접근하는 경우 <역참조>')
        queryset = Store.objects.prefetch_related("books").all()
        stores = []
        for store in queryset:
            books = [book.name for book in store.books.filter(name='Book1')]
            stores.append({'id': store.id, 'name': store.name, 'books': books})

        return JsonResponse({'stores_with_prefetch_related' : stores }, status=200)

class StoresWithPrefetchObjectView(View):
    @query_debugger
    def get(self, request):
        print(f'Store에서 Book Instance에 접근하는 경우 <역참조>')
        queryset = Store.objects.prefetch_related(Prefetch('books', queryset=Book.objects.filter(name='Book1')))
        stores = []
        for store in queryset:
            books = [book.name for book in store.books.all()]
            stores.append({'id': store.id, 'name': store.name, 'books': books})

        return JsonResponse({'stores_with_prefetch_related' : stores }, status=200)


class StoresWithPrefetchObjectView(View):
    @query_debugger
    def get(self, request):
        print(f'Store에서 Book Instance에 접근하는 경우 <역참조>')
        queryset = Store.objects.prefetch_related(Prefetch('books', queryset=Book.objects.filter(name='Book1'), to_attr='book1_list'))
        stores = []
        for store in queryset:
            books = [book.name for book in store.book1_list]
            stores.append({'id': store.id, 'name': store.name, 'books': books})

        return JsonResponse({'stores_with_prefetch_related' : stores }, status=200)

