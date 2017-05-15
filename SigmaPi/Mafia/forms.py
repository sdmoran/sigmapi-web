
from django.contrib.auth.models import User
from django.forms import CharField, ModelChoiceField, ChoiceField

from SigmaPi.forms import BootstrapForm
from .enums import MafiaRole
from .models import MafiaGame, MafiaPlayer, MAFIA_GAME_NAME_MAX_LENGTH

class MafiaAddGameForm(BootstrapForm):
    name = CharField(
        max_length=MAFIA_GAME_NAME_MAX_LENGTH,
        initial='Unnamed Mafia Game',
        label='Name'
    )

class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class MafiaAddUserToGameForm(BootstrapForm):
    user = UserModelChoiceField(queryset=User.objects.all(), label='')
    def __init__(self, game, *args, **kwargs):
        super(MafiaAddUserToGameForm, self).__init__(*args, **kwargs)
        if game:
            players = MafiaPlayer.objects.filter(game=game)
            usernames = [p.user.username for p in players]
            self.fields['user'].queryset = User.objects.exclude(
                username__in=usernames
            ).exclude(
                username=game.creator.username
            ).order_by(
                'first_name'
            )

class MafiaAssignRoleForm(BootstrapForm):
    user = UserModelChoiceField(queryset=User.objects.all())
    role = ChoiceField(choices=MafiaRole.get_choice_tuples())
    def __init__(self, game, *args, **kwargs):
        super(MafiaAssignRoleForm, self).__init__(*args, **kwargs)
        if game:
            players = MafiaPlayer.objects.filter(game=game)
            usernames = [p.user.username for p in players]
            self.fields['user'].queryset = User.objects.filter(
                username__in=usernames
            ).order_by(
                'first_name'
            )
