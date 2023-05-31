from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class CustomPagination(PageNumberPagination):
    page_size = 8 # in all pages only 8 wil displayed unless we customize
    page_query_param = 'page' # to display in url
    page_size_query_param = 'size' # in url we can pass ?size=10 to customize & display 10 elments
    max_page_size = 10 # maximum size we can customize in url
    # last_page_strings = 'end' # in default, word is last


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 8 # in all pages only 8 wil displayed unless we customize
    max_limit = 10 # maximum size we can customize in url
    limit_query_param = 'limit' # in url we can pass ?limit=10 to customize & display 10 elments
    offset_query_param = 'offset' # in url we can pass ?offset=10 to customize & display after first 10 elments
# limit & offser are default names


class CustomCursorPagination(CursorPagination):
    page_size = 8 # will not have page numbers only cursor for next or previous page
    cursor_query_param = 'cursor'
    ordering = 'created' # created attribute
# will be displayed based on - created time by default