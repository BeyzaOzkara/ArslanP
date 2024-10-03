from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import RegisterView, ResetPasswordView

app_name = 'ArslanTakipApp'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view()),
    # path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view()),
    path('login_success/', views.login_success, name='login_success'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    # path('change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    # path('change-password/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/', views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password-change/done/', views.password_success, name='password_success'),
    path('register/', RegisterView.as_view(), name= "register"),
    path('notif/<str:id>', views.notif),
    path('notifications/', login_required(views.AllNotificationsView.as_view())),
    path('notifications/all', views.notifications_all),
    path('notifReadAll', views.notifReadAll),
    path('location/', views.location, name="location"),
    path('location/list/', views.location_list),
    path('location/kalip', views.location_kalip),
    path('location/hareket', views.location_hareket),
    path('hareket', login_required(views.HareketView.as_view())),
    path('kalip/', login_required(views.KalipView.as_view())),
    path('deneme/', views.DenemeView.as_view()),
    path('kalip/liste', views.kalip_liste),
    path('kalip/tum', views.kalip_tum),
    path('kalip/rapor', views.kalip_rapor),
    path('diesChat/<str:kNo>', views.comment_kalip, name="kalipChat"),
    path('kalip/getcomments/<str:kId>', views.kalip_getcomments, name='kalipComment'),
    path('view/comment/<str:cId>', views.view_comment, name='viewComment'),
    path('getviews/<str:cId>', views.get_viewed_users, name='getviewedusers'),
    path('kalip/postcomment', views.kalip_comments_post, name='kalipCommentPost'),
    path('kalip/editcomment', views.kalip_comments_edit, name='kalipCommentEdit'),
    path('kalip/deletecomment/<str:cId>', views.kalip_comments_delete, name='kalipCommentDelete'),
    path('qr/', views.qrKalite, name='qr'),
    path('qr/deneme', views.qrKalite_deneme, name='qrdeneme'),
    path('siparis2/', views.siparis2_list),
    path('siparis3/', login_required(views.Siparis2View.as_view())),
    path('siparis3/list', views.siparis3_list),
    path('siparis2/child', views.siparis2_child),
    path('siparis/', login_required(views.SiparisView.as_view())),
    path('siparis/list', views.siparis_list),
    path('siparis/max', views.siparis_max),
    path('siparis/child/<str:pNo>', views.siparis_child),
    path('siparis/ekle', views.siparis_ekle),
    path('eksiparis/', login_required(views.EkSiparisView.as_view())),
    path('eksiparis/uretim', views.eksiparis_uretim),
    path('eksiparis/uretimbitir', views.eksiparis_uretimbitir),
    path('eksiparis/selectgetir', views.eksiparis_selectgetir),
    path('siparis/presKodu/<str:pNo>', views.siparis_presKodu),
    path('eksiparis/list', views.eksiparis_list),
    path('eksiparis/acil', views.eksiparis_acil),
    path('eksiparis/hammadde', views.eksiparis_hammadde),
    path('eksiparis/yuzey', views.eksiparis_yuzey),
    path('eksiparis/timeline', views.eksiparis_timeline),
    path('kalipfirini/', login_required(views.KalipFirinView.as_view())),
    path('kalipfirini/meydan', views.kalipfirini_meydan),
#     path('kalipfirini/goz', views.kalipfirini_goz),
    path('baskigecmisi/', login_required(views.BaskiGecmisiView.as_view())),
    path('baskigecmisi/list', views.baskigecmisi_list),
    path('yuda/', login_required(views.YudaView.as_view())),
    path('yuda/<str:objId>', views.yuda),
    path('yudakaydet', views.yuda_kaydet),
    path('yudas', login_required(views.YudasView.as_view()), name='yudas'),
    path('yudas/list' ,views.yudas_list),
    path('yudaDetail/<str:yId>', views.yudaDetail, name='yudaDetail'),
    path('yudakalipno', views.yudaDetail_kalipno, name='yudaDetailKalipNo'),
    path('yudaDetail2/<str:yId>', views.yudaDetail2, name='yudaDetail2'),
    path('yudaDetailComment', views.yudaDetailComment),
    path('yudaDCDelete/<str:cId>', views.yudaDCDelete),
    path('yudaDCEdit', views.yudaDCEdit),
    path('yudaDetailAnket', views.yudaDetailAnket),
    path('yudaDetailSvg', views.yudaDetailSvg),
    path('yudaDelete/<str:yId>', views.yudaDelete, name='yudaDelete'),
    path('yudaEdit/<str:yId>', views.yudaEdit),
    path('yudachange/<str:yId>', views.yudachange),
    path('yudaCopy/<str:yId>', views.yudaCopy),
    path('deletedYudas', login_required(views.DeletedYudasView.as_view()), name='deletedYudas'),
    path('deletedYudas/list', views.deletedYudas_list),
    path('yudaDeleteCancel/<str:yId>', views.yudaDeleteCancel),
    path('uretimplanlama', views.UretimPlanlamaView.as_view()),
    path('get_data_by_press_code/', views.UretimPlanlamaView.as_view(), name='get_data_by_press_code'),
    path('eksiparisdeneme/', login_required(views.eksiparisDenemeView.as_view())),
    path('eksiparis_get_data/', views.eksiparis_get_data, name='eksiparis_get_data'),
    path('eksiparis_save_data/', views.eksiparis_save_data, name='eksiparis_save_data'),
    path('check_eksiparis/', views.check_eksiparis, name='check_eksiparis'),
    path('presuretimtakiplist/', login_required(views.PresUretimTakipView.as_view())),
    path('uretim_kalip_firin', views.uretim_kalip_firin, name='uretim_kalip_firin'),
    path('firin_kalip_list/<str:pNo>/', views.firin_kalip_list, name='firin_kalip_list'),
    path('presuretimbasla', views.presuretimbasla, name='presuretimbasla'),
    path('presuretimbitir', views.presuretimbitir, name='presuretimbitir'),
    path('uretim_get_locations', views.uretim_get_locations, name='uretimgetlocations'),
    path('presuretimtakip/<int:id>/', views.pres_uretim_takip, name='pres_uretim_takip'),

]