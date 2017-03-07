
 from .models import *


def resolve_night(night):

    actions = MafiaActions.objects.filter(night=night).order_by('action_type__ordering')
    players = MafiaPlayers.objects.filter(status=MafiaPlayerStatus.ALIVE)
    results = { player.user: PlayerResult(player) for player in players }

    for action in actions:

        if result[action.performer].killed or result[action.performer].seduced:
            continue

        results[action.performer].performed_action_type = action.action_type
        results[action.performer].targeted = []
        if action.action_type.num_targets >= 1:
            results[action.performer].targeted.append((target1, target1.killed))
        if action.action_type.num_targets >= 2:
            results[action.performer].targeted.append((target2, target2.killed))

        if action.action_type is MafiaActionType.SEDUCE:
            results[action.performer].targeted = [action.target1]
            results[action.target1].seduced = True

        if action.action_type is MafiaActionType.REMEMBER:
            remembered_from = MafiaPlayer.objects.get(player=action.target1)
            pp.previous_role = remembered_from.role
            pp.role = new_role
            pp.times_aciton_used = 0
            # TODO should amnesiac get random or old target?
            pp.executioner_target = remembered_from.executioner_target

        if at is MafiaActionType.ON_GUARD