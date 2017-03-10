
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from mafia import start_game, advance_game
from .models import *

class MafiaTestCase(TestCase):

    def create_player(self, role, index, executioner_target=None):
        FIRST_NAMES = ['Joe', 'Bob', 'Greg']
        if index > 2:
            raise ValueError('index must be at least 3')
        username = (FIRST_NAMES[index][0] + role.name.replace(' ', '')).lower()
        user = User.objects.create_user(username, username + '@test.com', '123456')
        user.first_name = FIRST_NAMES[index]
        user.last_name = role.name 
        user.save()
        player = MafiaPlayer(
            game=self.game, user=user, role=role.code, executioner_target=executioner_target
        )
        player.save()
        return player

    def setUp(self):
        self.u_mod = User.objects.create_user('mod', 'mod@test.com', '123456')
        self.u_mod.first_name = 'Joe'
        self.u_mod.last_name = 'Moderator'

        self.game = MafiaGame(created=datetime.datetime.now(), created_by=self.u_mod)
        self.game.save()
        self.mod = MafiaModerator(game=self.game, user=self.u_mod)
        self.mod.save()
        self.mayor = self.create_player(MafiaRole.MAYOR, 0)

        mayor_action = MafiaAction(
            performer=self.mayor, night_number=1,
            action_type=MafiaActionType.NO_ACTION.code
        )
        mayor_action.save()

        start_game(self.game)

    def test_mafia(self):
        
        self.assertTrue(advance_game(self.game))
        self.assertTrue(advance_game(self.game))

        self.assertEqual(self.game.day_number, 2)
        self.assertEqual(self.game.time, MafiaGameTime.DAY.code)
        self.assertEqual(self.mayor.status, MafiaPlayerStatus.ALIVE.code)

        mayor_result = MafiaNightResult.objects.get(action__performer=self.mayor)
        self.assertTrue(mayor_result.contains_report_line('You did not perform an action.'))
