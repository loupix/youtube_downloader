from django.urls import include, path, re_path

from . import views

urlpatterns = [
	path('videos/', views.videos, name='facial_videos'),
	path('videos/remove/', views.removeVideo, name='facial_removeVideo'),
	path('sequences/', views.sequences, name='facial_sequences'),
	path('sequences/remove/', views.removeSequence, name='facial_removeSequence'),

	path('tags/', views.tags, name='facial_tags'),
	path('tags/new/', views.newTags, name='facial_newTags'),
	path('tags/add/', views.addTags, name='facial_addTags'),
	path('tags/del/', views.delTags, name='facial_delTags'),
	path('tags/remove/', views.removeTags, name='facial_removeTags'),


	path('groups/', views.groups, name='facial_groups'),
	path('groups/new/', views.newGroups, name='facial_newGroups'),
	path('groups/add/', views.addGroups, name='facial_addGroups'),
	path('groups/del/', views.delGroups, name='facial_delGroups'),
	path('groups/remove/', views.removeGroups, name='facial_removeGroups'),
]