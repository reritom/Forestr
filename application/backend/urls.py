from django.conf.urls import url, include
from backend.views.organisation import OrganisationView
from backend.views.organisation_single import SingleOrganisationView
from backend.views.survey import SurveyView
from backend.views.survey_single import SingleSurveyView
from backend.views.survey_item import SurveyItemView
from backend.views.survey_item_single import SingleSurveyItemView
from backend.views.profile import ProfileView
from backend.views.item import ItemView
from backend.views.item_single import SingleItemView
from backend.views.member import MemberView
from backend.views.member_single import SingleMemberView
from backend.views.contract import confirm_contract
from backend.views.ajax import ajax_dispatch
from backend.views.account import (
    login_user,
    logout_user,
    signup
)

app_name = 'backend'

urlpatterns = [
    url(r'profile', ProfileView.as_view(), name='profile'),
    url(r'account/signup$', signup, name='signup'),
    url(r'account/login$', login_user, name='login'),
    url(r'account/logout$', logout_user, name='logout'),
    url(r'survey/(?P<survey_id>[-\w]+)/item/(?P<survey_item_id>[-\w]+)', SingleSurveyItemView.as_view(), name='specific_survey_item'),
    url(r'survey/(?P<survey_id>[-\w]+)/item', SurveyItemView.as_view(), name='survey_item'),
    url(r'survey/(?P<survey_id>[-\w]+)', SingleSurveyView.as_view(), name='specific_survey'),
    url(r'survey', SurveyView.as_view(), name='survey'),
    url(r'member/(?P<member_id>[-\w]+)', SingleMemberView.as_view(), name='organisation'),
    url(r'member', MemberView.as_view(), name='organisation'),
    url(r'setting/(?P<setting_id>[-\w]+)', OrganisationView.as_view(), name='organisation'),
    url(r'setting', OrganisationView.as_view(), name='organisation'),
    url(r'organisation/(?P<organisation_id>[-\w]+)', SingleOrganisationView.as_view(), name='specific_organisation'),
    url(r'organisation', OrganisationView.as_view(), name='organisation'),
    url(r'item/(?P<item_id>[-\w]+)', SingleItemView.as_view(), name='specific_item'),
    url(r'item', ItemView.as_view(), name='item'),
    url(r'contract/(<P<contract_id>[-\w]+)/confirm', confirm_contract, name='confirm_contract'),
    url(r'ajax/(<P<resource>[-\w]+)/', ajax_dispatch, name='ajax_dispatch'),
]
