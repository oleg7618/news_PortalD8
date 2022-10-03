#from django.contrib.auth.models import Group
#from allauth.account.forms import SignupForm


#class BaseSignupForm(SignupForm):

#    def save(self, request):
#        user = super(BaseSignupForm, self).save(request)
#        basic_group = Group.objects.get(name='common')
#        basic_group.user_set.add(user)
#        return user