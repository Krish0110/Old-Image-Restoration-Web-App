from django.urls import path
from . import views

urlpatterns = [
  path('detect-damage/', views.detect_damage, name = 'detect_damage'),
  path('inpaint-image/', views.inpaint_image, name = 'inpaint_image'),
  path('add-color/', views.add_color, name='add_color'),
  path('improve-reso/', views.use_gfp, name = "use_gfp"),
]