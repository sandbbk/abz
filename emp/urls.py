from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('', views.ftree, name='root'),
    path('make_emp', views.make_employee, name='make_emp'),
    path('all_table', views.all_table, name='all_table'),
    path('ajx', views.table_ajx, name='ajx'),
    path('ajx/del', views.del_emp, name='del'),
    path('descendants', views.get_descendants, name='descendants'),
    re_path(r'ajx/(?P<pk>[-a-z0-9]+)', views.emp_edit, name='ajx'),
    path('create', views.create_emp, name='create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
