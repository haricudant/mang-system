"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
# from django.cong.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

]
# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include
from django.contrib import admin

# Use include() to add URLS from the catalog application and authentication system




urlpatterns += [
    path('catalog/', include('catalog.urls')),

]


# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
# urlpatterns += [
#     path('', RedirectView.as_view(url='/', permanent=True)),
#
# ]



# from catalog.views import loginView, logout_view, register_view
# #Add Django site authentication urls (for login, logout, password management)
# urlpatterns += [
# #
# #
#      path('accounts/login/', loginView),
#      path('accounts/register/', register_view),
#      path('accounts/logout/', logout_view),
#  ]

# urlpatterns = [
#   path('', include('social_django.urls', namespace='social')),
#   path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL},
#     name='logout')
# ]
from django.urls import path, include
from catalog import views
from catalog.views import loginView, logout_view, register_view


urlpatterns += [
    path('success/', views.emp),
    # path(r'^login/$', auth_views.login),
    # path('', views.emp, name="login"),
    # path('success/',views.author, name ="au"),

path('accounts/log/', loginView,name="logout"),
path('', register_view),
path('accounts/logout/', logout_view),
# path('accounts/',include('django.contrib.auth.urls')),
]
