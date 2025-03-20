from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *
from .yasg import urlpatterns as api_doc_urls

urlpatterns = [
    # Cooking
    path('', Index.as_view(), name='index'),
    path('add_post/', PostAdd.as_view(), name='add_post'),
    path('post/<int:pk>/update/', PostUpdate.as_view(), name='update_post'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='delete_post'),
    path('search/', SearchResults.as_view(), name='search'),
    path('change_password/', UserChangePassword.as_view(), name='change_password'),

    # API
    path('categories/api/', CookingCategoriesAPI.as_view(), name='CookingCategoriesAPI'),
    path('categories/api/<int:pk>', CookingCategoryAPIDetail.as_view(), name='CookingCategoryAPIDetail'),
    path('posts/api/', CookingPostsAPI.as_view(), name='CookingPostsAPI'),
    path('posts/api/<int:pk>', CookingPostAPIDetail.as_view(), name='CookingPostAPIDetail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Cooking
    path('category/<int:pk>/', get_category_list, name='category_list'),
    path('post/<int:pk>', get_post_detail, name='post_detail'),
    path('signup/', sign_up, name='sign_up'),
    path('login/', user_login, name='log_in'),
    path('logout/', user_logout, name='log_out'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
    path('profile/<int:user_id>', get_profile, name='profile'),
]

urlpatterns += api_doc_urls
