
from django.forms import CharField

from SigmaPi.forms import BootstrapForm
from .models import MafiaGame, MAFIA_GAME_NAME_MAX_LENGTH

class MafiaAddGameForm(BootstrapForm):
    name = CharField(
        max_length=MAFIA_GAME_NAME_MAX_LENGTH,
        initial='Unnamed Mafia Game',
        label='Name'
    )
