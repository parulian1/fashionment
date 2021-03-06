from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
   url(r'^store/edit-store/$','store.views.edit_store',name='edit_store'),
   url(r'^store/add-store/$','store.views.add_store',name='add_store'),
   url(r'^store/$','store.views.view_store',name='view_store'),
   url(r'^find-by-store/$','store.views.list_store',name='list_store'),
   url(r'^find-by-designer/$','store.views.list_designer',name='list_designer'),
   url(r'^find-by-store/(?P<type>[-\w]+)/(?P<alphabet>[-\w]*)/*$','store.views.list_store',name='list_store2'),
   url(r'^find-by-item/$','store.views.list_item',name='list_item'),
   
   url(r'^store/remove-store/$','store.views.remove_store',name='remove_store'),
   url(r'^store/comment/(?P<slug>[-\w]*)/(?P<store_id>\d*)/$','store.views.view_comment',name='view_comment'),
   url(r'^store/remove_comment/(?P<comment_id>\d+)/$','store.views.remove_comment',name='remove_comment'),
   url(r'^store/(?P<user_id>\d+)/add/$','store.views.addicted',name='addicted'),
   url(r'^store/add-item/(?P<line_id>\d+)/$','store.views.item_add',name='item_add'),
   url(r'^store/(?P<item_id>\d+)/add-item-complete/$','store.views.add_item_complete',name='add_item_complete'),
   url(r'^store/view-item/(?P<line_id>\d+)/$','store.views.view_item',name='view_item'),
   url(r'^store/view-collection/(?P<line_name>[-\w]+)/$','store.views.view_same_collection',name='same_collection'),
   url(r'^store/edit-item/(?P<line_id>\d+)/$','store.views.edit_item',name='edit_item'),
   url(r'^store/detail-items/(?P<item_id>\d+)/$','store.views.redir_detail_item',name='detail_items'),
   url(r'^store/detail-items/(?P<item_id>\d+)/(?P<item_slug>[-\w]+)/$','store.views.detail_items',name='item_info'),
   url(r'^store/remove-line/(?P<item_id>\d+)/$','store.views.remove_item',name='remove_item'),
   url(r'^store/remove-item/(?P<item_id>\d+)/$','store.views.remove_item2',name='remove_item2'),
   url(r'^store/add-line/$','store.views.line_add',name='line_add'),
   url(r'^store/edit-line/(?P<line_id>\d+)/$','store.views.edit_line',name='edit_line'),
   url(r'^store/view-line/(?P<store_id>\d+)/$','store.views.view_line',name='view_line'),
   url(r'^store/view-my-addict/(?P<store_id>\d+)/$','store.views.view_my_addict',name='view_my_addict'),
   url(r'^store/view-addicts-to/$','store.views.addicts_to',name='addicts_to'),
   url(r'^store/remove-addicts-to/(?P<addict_id>\d+)/$','store.views.remove_addict',name='remove_addict'),
   url(r'^store/add-compare-item/(?P<item_id>\d+)/$','store.views.add_compare_item',name='compare_item'),
   url(r'^store/view-compare-list/$','store.views.view_compare_list',name='view_compare_list'),
   url(r'^store/view-compare-thumbnails/$','store.views.view_compare_thumbnails',name='view_compare_thumbnails'),
   url(r'^store/remove-compare-list/$','store.views.remove_compare_list',name='remove_compare_list'),
   url(r'^store/remove-compare-thumbnails/$','store.views.remove_compare_thumbnails',name='remove_compare_thumbnails'),
   url(r'^store/view-detail-compare/$','store.views.view_detail_compare',name='view_detail_compare'),
   url(r'^store/view-detail-compares/$','store.views.view_detail_compares',name='view_detail_compares'),
   url(r'^store/primary-picture/(?P<line_id>\d+)/$','store.views.primary_picture',name='primary_picture'),
   url(r'^most/(?P<choose_slug>[-\w]+)/(?P<slug>[-\w]+)/(?P<type>[-\w]*)/*$','store.views.view_most_all',name='view_most_all'),
   url(r'^store/most/(?P<store_type>[-\w]+)/(?P<store_slug>[-\w]+)/$','store.views.view_most_store',name='view_most_store'),
   url(r'^items/(?P<item_slug>[-\w]+)/$','store.views.view_most_item',name='view_most_item'),
   url(r'^store/rate-store/(?P<store_id>\d+)/$','store.views.rate_store',name='rate_store'),
   url(r'^store/rate-item/(?P<item_id>\d+)/$','store.views.rate_item',name='rate_item'),
   url(r'^store/message/(?P<item_id>\d+)/$','store.views.message_fashion_owner',name='message_fashion_owner'),
   url(r'^(?P<store_id>\d+)/store-notice/$','store.views.store_notice',name='notice_store'),
   url(r'^(?P<item_id>\d+)/item-notice/$','store.views.item_notice',name='notice_item'),
   url(r'^store/remove_line/$','store.views.delete_line',name='remove_line'),
   url(r'^store/view_remove_line/$','store.views.remove_line',name='view_remove_line'),
   url(r'^store/delete-item/(?P<item_id>\d+)/$','store.views.delete_item',name='delete_item'),
   url(r'^store/remove_picture/(?P<item_id>\d+)$','store.views.remove_picture',name='remove_picture'),
   url(r'^store/remove/(?P<slug>[-\w]+)/(?P<item_id>\d*)/*$','store.views.remove',name='remove_collection_or_item'),
   url(r'^store/item/detail_picture/(?P<item_id>\d+)/(?P<slug>[-\w]+)/$','store.views.view_detail_pic',name='view_detail_pic'),
   url(r'^store/invite-friend/by-email/$','store.views.invite_friend',name='by_email'),
   url(r'^store/confirm_remove/$','store.views.confirm_remove_store',name='confirm_rem_store'),
   url(r'^report/(?P<id>\d+)/(?P<slug>[-\w]+)/$','store.views.report_content',name='report'),
   url(r'^see_all/designer/(?P<slug>[-\w]*)/*$','store.views.view_all_designer',name='view_all_designer'),
   url(r'^index/(?P<type>[-\w]+)/(?P<alphabet>[-\w]*)/*$','store.views.indexing',name='indexing'),
   url(r'^store/(?P<slug>[-\w]*)/$','store.views.view_store',name='view_stores'),
   #url(r'^$','store.views.list',name='list'),
)
