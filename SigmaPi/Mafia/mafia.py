
from .models import *

def _do_single_switch(switcher0, switcher1, target0, target1, switch_map, users_to_nights):
    temp = switch_map[target0]
    switch_map[target0] = switch_map[target1]
    switch_map[target1] = temp
    users_to_nights[target0].switched_with = target1
    users_to_nights[target1].switched_with = target0
    users_to_nights[target0].add_switched_by(switcher0)
    users_to_nights[target1].add_switched_by(switcher1)
    switcher0.action_effective = True
    switcher1.action_effective = True

def _do_double_switch(switcher0, switcher1, target, users_to_nights):
    users_to_nights[target].switched_with = target
    users_to_nights[target].add_switched_by(switcher0)
    users_to_nights[target].add_switched_by(switcher1)
    switcher0.action_effective = True
    switcher1.action_effective = True

def _do_overlapping_switch(switcher0, switcher1, target0, overlapped_target, target1, users_to_nights):
    _do_single_switch(switcher0, switcher1, target0, target1, users_to_nights)
    _do_double_switch(switcher0, switcher1, overlapped_target, users_to_nights)

def _do_switching(nights, users_to_nights):

    # Clear previous calculations
    for night in nights:
        night.clear_switched_by()

    # Initialize switch map; collect switch action nights
    switched = {night.player.user: night.player.user for night in nights}
    switch_nights = nights.filter(action=MafiaAction.SWITCH.code)

    # Fail if more than two switches
    if len(switch_nights) > 2:
        raise MafiaError('more than two switch actions in single night')

    # Perform two switches
    if len(switch_nights) >= 2:

        # Assign helper variables for switchers and targets
        s0 = switch_nights[0].player.user
        s1 = switch_nights[1].player.user
        s0t0 = switch_nights[0].target0_after_control
        s0t1 = switch_nights[0].target1_after_control
        s1t0 = switch_nights[1].target0_after_control
        s1t1 = switch_nights[1].target1_after_control

        # If both seduced_or_died, do nothing
        if switch_nights[0].seduced_or_died and switch_nights[1].seduced_or_died:
            pass

        # If one seduced_or_died, do the other
        elif switch_nights[0].seduced_or_died:
            _do_single_switch(s1, s1, s1t0, s1t1, users_to_nights)
        elif switch_nights[1].seduced_or_died:
            _do_single_switch(s0, s0, s0t0, s0t1, users_to_nights)

        # Switches with the same two players
        elif (s0t0 == s1t0 and s0t1 == s1t1) or (s0t0 == s1t1 and s0t1 == s1t0):
            _do_double_switch(s0, s1, s0t0, users_to_nights)
            _do_double_switch(s0, s1, s0t1, users_to_nights)

        # Switches where one players is in both
        elif s0t0 == s1t0:
            _do_overlapping_switch(s0, s1, s0t1, s0t0, s1t1, users_to_nights)
        elif s0t0 == s1t1:
            _do_overlapping_switch(s0, s1, s0t1, s0t0, s1t0, users_to_nights)
        elif s0t1 == s1t0:
            _do_overlapping_switch(s0, s1, s0t0, s0t1, s1t1, users_to_nights)
        elif s0t1 == s1t1:
            _do_overlapping_switch(s0, s1, s0t0, s0t1, s1t0, users_to_nights)

        # Independent switches
        else:
            _do_single_switch(s0, s0, s0t0, s0t1, users_to_nights)
            _do_single_switch(s1, s1, s1t0, s1t1, users_to_nights)

    # Perform single switch
    elif len(switch_nights) >= 1 and not switch_nights[0].seduced_or_died:
        s = switch_nights[0].player.user
        _do_single_switch(
            s, s,
            switch_nights[0].target0_after_control,
            switch_nights[0].target1_after_control,
            users_to_nights
        )

    # Return switch map
    return switched

def _do_seduction(nights, users_to_nights):
    seduce_map = {night.player.user: False for night in nights}
    for seduce_night in nights.filter(action=MafiaAction.SEDUCE.code):
        if seduce_night.seduced_or_died:
            continue
        target_night = users_to_nights[seduce_night.target0]
        target_night.attempted_seduced = True
        target_night.add_targeted_by(seduce_night.player.user)
        seduce_night.action_effective = True
    return seduce_map

def _kill_cancelled(killer_night, killed_set):
    return (
        (not killer_night.seduced) or
        (killer_night.died and not killer_night.player.user in killed_set)
    )

def _kill_if_alive(killer_night, target_night, killed_status, killed_set, users_to_nights):
    if target_night.died and target_night.player.user not in killed_set:
        killer_night.action_effective = True
        return
    target_night.status = (
        MafiaNightStatus.TERMINATED
        if MafiaNightStatus.TERMINATD.code in [target_night.status, killed_status]
        else MafiaNightStatus.ATTACKED
    )
    if target_night.died:
        killer_night.action_effective = True
        killed_set.add(target_night.user)
    else:
        for protector in target_night.get_protected_by():
            users_to_nights[protector].action_effective = True
        if target_night.action == MafiaAction.BULLETPROOF_VEST.code:
            target_night.action_effective = True

def _process_actions(nights, users_to_nights):

    # Do control, killing those that try to control on-guard players
    control_nights = nights.filter(action=MafiaAction.CONTROL.code)
    if len(control_nights) > 1:
        raise MafiaError('more than one control action in single night')
    if control_nights:
        target0_night = users_to_nights[control_nights[0].target0]
        if target0_night.on_guard:
            control0_nights[0].attacked_status = MafiaNightStatus.TERMINATED.code
            target0_night.action_effective = True
        else:
            target0_night.controlled_to_target = control_nights[0].target1

    # Kill players targeting on-guard players
    for night in nights:
        action = MafiaPlayerNight.get_instance(night.action)
        if action.is_covert:
            continue
        if action.num_targets == 2:
            t1_night = users_to_nights[switch_night.target1_after_control.user]
            if t1_night.on_guard:
                night.attacked_status = MafiaNightStatus.TERMINATED.code
                t1_night.action_effective = True
        if action.num_targets >= 1:
            t0_night = users_to_nights[switch_night.target1_after_control.user]
            if t0_night.on_guard:
                night.attacked_status = MafiaNightStatus.TERMINATED.code
                t0_night.action_effective = True
        if action.is_direct_offense:
            t0_night.attacked_status = MafiaNightStatus.ATTACKED.code

    # Repeat switching and seduction until we reach a stable state
    switched, seduced = None, None
    while True:
        new_switched = _do_switching(nights, users_to_nights)
        new_seduced = _do_seduction(nights, users_to_nights)
        stable = (new_switched == switched and new_seduced == seduced)
        switched = new_switched
        seduced = new_seduced
        if stable:
            break

    # Mark framed player nights
    for frame_night in MafiaPlayerNight.objects.filter(action=MafiaAction.FRAME.code):
        if frame_night.seduced_or_died:
            continue
        target_night = users_to_nights[switched[frame_night.target0_after_control]]
        target_night.framed = True
        target_night.add_targeted_by(frame_night.player.user)

    # Mark protected player nights
    for protect_night in MafiaPlayerNight.objects.filter(action=MafiaAction.PROTECT.code):
        if protect_night.seduced_or_died:
            continue
        target_night = users_to_nights[switched[protect_night.target0_after_control]]
        target_night.add_protected_by(protect_night.player.user)

    # Mark defended player nights; kill those that tried to slay such players
    for defend_night in MafiaPlayerNight.objects.filter(action=MafiaAction.DEFEND.code):
        if defend_night.seduced_or_died:
            continue
        target_night = users_to_nights[switched[defend_night.target0_after_control]]
        target_night.defended = True
        target_night.add_targeted_by(defend_night.player.user)
    for night in nights:
        if night.died:
            continue
        action = MafiaAction.get_instance(night.action)
        if action.is_direct_offense and not action.is_covert:
            for defender in target_night.get_defended_by():
                night.status = MafiaNightStatus.TERMINATED
                users_to_nights[defender].status = MafiaNightStatus.TERMINATED
                users_to_nights[defender].action_effective = True

    # Mark corrupted player nights; kill corrupter if successful
    for corrupt_night in MafiaPlayerNight.objects.filter(action=MafiaAction.CORRUPT.code):
        if corrupt_night.seduced_or_died:
            continue
        target_night = users_to_nights[switched[corrupt_night.target0_after_control]]
        target_night.attempted_corrupted = True
        target_night.add_targeted_by(corrupt_night.player.user)
        if target_night.corrupted:
            control_night.player.user.died_for_other_reason = True

    # Perform all remaining killing actions and roles with same priority
    died_from_killing = set()

    # Killing action: Slay
    for slay_night in MafiaPlayerNight.objects.filter(action=MafiaAction.SLAY.code):
        if _kill_cancelled(slay_night, died_from_killing):
            continue
        target_night = users_to_nights[switched[slay_night.target0_after_control]]
        _kill_if_alive(
            slay_night, night, MafiaNightStatus.ATTACKED,
            died_from_killing, users_to_nights
        )
        target_night.add_targeted_by(snipe_night.player.user)

    # Killing action: Ambush
    for ambush_night in MafiaPlayerNight.objects.filter(action=MafiaAction.AMBUSH.code):
        if _kill_cancelled(ambush_night, died_from_killing):
            continue
        for night in nights:
            # The player dies in the ambush if:
            died_in_ambush = (
                # They aren't the ambusher, and either (a), (b), or (c)
                night.player.user != night.performer and (
                    # (a) Their first target is ambushed
                    night.target0 == ambush_night.target0 or
                    # (b) Their second target is ambushed and their action wasn't Control
                    (
                        night.target1 == ambush_night.target0 and
                        night.action != MafiaAction.CONTROL.code
                    # (c) They're the ambushee and they didn't target anyone else
                    ) or (
                        night.player.user == ambush_night.target0 and
                        night.target0 == None
                    )
                )
            )
            if died_in_ambush:
                _kill_if_alive(
                    ambush_night, night, MafiaNightStatus.ATTACKED,
                    died_from_killing, users_to_nights
                )

    # Killing action: Snipe
    for snipe_night in MafiaPlayerNight.objects.filter(action=MafiaAction.SNIPE.code):
        if _kill_cancelled(snipe_night, died_from_killing):
            continue
        target_night = users_to_nights[snipe_night.target0] # NOT SWITCHED OR CONTROLLED
        _kill_if_alive(
            snipe_night, target_night, MafiaNightStatus.TERMINATED,
            died_from_killing, users_to_nights
        )
        target_night.add_targeted_by(snipe_night.player.user)

    # Killing action: Ignite
    for ignite_night in MafiaPlayerNight.objects.filter(action=MafiaAction.IGNITE.code):
        if _kill_cancelled(ignite_night, died_from_killing):
            continue
        for night in nights:
            if night.player.doused:
                _kill_if_alive(
                    ignite_night, night, MafiaNightStatus.TERMINATED,
                    died_from_killing, users_to_nights
                )
        break # Only need to do ignite once


    # Killing role: Bomb
    bomb_nights = MafiaPlayerNights.objects.filter(player__role=MafiaRole.BOMB.code)
    if len(bomb_nights) > 1:
        raise MafiaError('more than one bomb in game')
    if len(bomb_nights) >= 1 and not _kill_cancelled(bomb_nights[0], died_from_killing):
        for night in nights:
            is_direct_offense = MafiaAction.get_instance(night.action).is_direct_offense
            if is_direct_offense:
                _kill_if_alive(
                    bomb_nights[0], night, MafiaNightStatus.TERMINATED,
                    died_from_killing, users_to_nights
                )

    # Killing role: Saboteur
    # TODO

    # Killing role: Jester
    # TODO

    # Mark doused/un-doused player nights
    for douse_night in MafiaPlayerNight.objects.filter(action=MafiaAction.DOUSE.code):
        if douse_night.seduced_or_died:
            continue
        target_night = users_to_nights[switched[douse_night.target0_after_control]]
        target_night.doused = True
        target_night.add_targeted_by(douse_night.player.user)
    for un_douse_night in MafiaAction.objects.filter(action=MafiaAction.UN_DOUSE.code):
        if un_douse_night.seduced_or_died:
            continue
        target_night = users_to_nights[switched[un_douse_night.target0_after_control]]
        target_night.un_doused = True
        target_night.add_targeted_by(un_douse_night.player.user)

    # Mark disposed player nights
    for dispose_night in MafiaPlayerNight.objects.filter(action=MafiaAction.DISPOSE.code):
        if dispose_night.seduced_or_died:
            continue
        target_night = users_to_nights[switched[dispose_night.target0_after_control]]
        target_night.disposed = True
        target_night.add_targeted_by(dispose_night.player.user)
        if target_night.died:
            dispose_night.action_effective = True

    # Mark remembered player nights
    for remember_night in MafiaPlayerNights.objects.filter(action=MafiaAction.REMEMBER.code):
        if remember_night.seduced_or_died:
            continue
        remember_night.remembered = remember_night.target0_after_control
        remember_night.action_effective = True

def _get_name(user):
    return user.first_name + ' ' + user.last_name

def _list_users(users):
    num_users = len(users)
    if num_users == 0:
        return 'nobody'
    elif num_users == 1:
        return _get_name(users[0])
    elif num_users >= 2:
        return ', '.join(
            _get_name(user) for user in users[:-1]
        ) + ', and ' + _get_name(users[-1])

def _investigate(investigator_night, target_night):
    target_role = MafiaRole.get_instance(target_night.role)
    guilty = (
        (target_role.faction == MafiaFaction.MAFIA and target_role != MafiaRole.GODFATHER) or
        (target_role == MafiaRole.MILLER) or
        target_night.framed
    )
    appears_guilty = (
        not guilty
        if investigator_night.action == MafiaAction.INSANE_INVESTIGATE.code
        else guilty
    )
    return 'GUILTY' if appears_guilty else 'INNOCENT'

def _scrutinize(target_night):
    role = MafiaRole.get_instance(target_night.role)
    return len(0 for action in role.actions if action.is_lethal) >= 1

def _follow(target_night, users_to_nights):
    return '' # TODO
    #    _get_name(target_night.target0_after_control)
    #    if target_night.tar

def _watch(watcher_night, target_night):
    return '' # TODO
    #return _list_users(list(
    #    set(target_night.get_targeted_by()) - set([follower_night.player.user])
    #))

def _generate_reports(nights, users_to_nights):
    for night in nights:
        name0 = _get_name(night.target0)
        name1 = _get_name(night.target1)
        if night.died:
            night.add_report_line('YOU DIED!')
            continue
        if night.action == MafiaAction.NO_ACTION.code:
            night.add_report_line(
                'You did not perform an action.'
            )
            if night.seduced:
                night.add_report_line(
                    'You were seduced.'
                )
        elif night.seduced:
            night.add_report_line(
                'You were seduced and forgot to perform your action.'
            )
        elif night.action == MafiaAction.CONTROL.code:
            night.add_report_line(
                'You controlled ' + name0 +
                ' to target ' + name1 + '.'
            )
        elif night.action == MafiaAction.ON_GUARD.code:
            night.add_report_line(
                'You went on guard' + (
                    ', killing at least one player.' if night.action_effective
                    else '.'
                )
            )
        elif night.action == MafiaAction.SEDUCE.code:
            night.add_report_line(
                'You may have seduced ' + name0 + '.'
            )
        elif night.action == MafiaAction.SWITCH.code:
            night.add_report_line(
                'You switched ' + name0 + ' and ' +
                _get_name(night.target1) + '.'
            )
        elif night.action == MafiaAction.FRAME.code:
            night.add_report_line(
                'You framed ' + name0 + '.'
            )
        elif night.action in [MafiaAction.INVESTIGATE.code, MafiaAction.INSANE_INVESTIGATE.code]:
            night.add_report_line(
                'You investigated ' + name0 +
                ', and concluded that they are ' +
                _investigate(
                    night,
                    users_to_nights[users_to_nights[night.target0].switched_with]
                ) + '.'
            )
        elif night.action == MafiaAction.SCRUTINIZE.code:
            night.add_report_line(
                'You scrutinized ' + name0 +
                ', and concluded that they are ' +
                _scrutinize(users_to_nights[users_to_nights[night.target0].switched_with]) +
                '.'
            )
        elif night.action == MafiaAction.PROTECT.code:
            protect_target = users_to_nights[night.target0]
            if protect_target.status == MafiaNightStatus.SAFE.code:
                night.add_report_line(
                    'You protected ' + name + ', but they were not attacked.'
                )
            elif protect_target.status == MafiaNightStatus.ATTACKED.code:
                night.add_report_line(
                    'You successfully protected ' + name0 +
                    ' from an attack.'
                )
            elif protect_target.status == MafiaNightStatus.TERMINATED.code:
                night.add_report_line(
                    'You protected ' + name0 + ', but they died anyway.'
                )
        elif night.action == MafiaAction.DEFEND.code:
            defend_target = users_to_nights[night.target0]
            if defend_target.status == MafiaNightStatus.SAFE.code:
                night.add_report_line(
                    'You defended ' + name + ', but they were not attacked.'
                )
            elif defend_target.status == MafiaNightStatus.ATTACKED.code:
                raise MafiaError("defended target was attacked but defender is alive")
            elif defend_target.status == MafiaNightStatus.TERMINATED.code:
                night.add_report_line(
                    'You defended ' + name0 + ', but they died anyway.'
                )
        elif night.action == MafiaAction.BULLETPROOF_VEST.code:
            night.add_report_line("You used bulletproof vest.")
        elif night.action == MafiaAction.CORRUPT.code:
            corrupt_target = users_to_nights[night.target0]
            if corrupt_target.corrupted:
                raise MafiaError('Player corrrupted but corrupter not dead')
            else:
                night.add_report_line(
                    'You attempted to corrupt ' + name0 +
                    ', but they resisted or were protected.'
                )
        elif night.action == MafiaAction.SLAY.code:
            slay_target = users_to_nights[night.target0]
            if slay_target.status == MafiaNightStatus.SAFE:
                night.add_report_line(
                    'You attempted to slay ' + name + ', but they survived.'
                )
            else:
                night.add_report_line('You slayed ' + name + '.')
        elif night.action == MafiaAction.AMBUSH:
            night.add_report_line(
                'You ambushed ' + name + (
                    ', killing at leaset one player.'
                    if night.action_effective
                    else ', but did not kill anyone.'
                )
            )
        elif night.action == MafiaAction.SNIPE.code:
            night.add_report_line('You sniped ' + name + '.')
        elif night.action == MafiaAction.IGNITE.code:
            night.add_report_line('You ignited.')
        elif night.action == MafiaAction.SABOTAGE:
            pass # TODO
        elif night.action == MafiaAction.DOUSE.code:
            night.add_report_line('You doused ' + name +'.')
        elif night.action == MafiaAction.UN_DOUSE.code:
            night.add_report_line('You un-doused ' + name +'.')
        elif night.action == MafiaAction.DISPOSE.code:
            role_name = MafiaRole.get_instance(users_to_nights[night.target0].role).name
            night.add_report_line(
                'You disposed ' + name + '. Their actual role is ' + role_name + '.'
                if night.action_effective
                else 'You attempted to dispose ' + name  + ', but they did not die.'
            )
        elif night.action == MafiaAction.REVEAL.code:
            night.add_report_line('You revealed youself as Mayor.')
        elif night.action == MafiaAction.FOLLOW.code:
            night.add_report_line(
                'You followed ' + name + ', and determined that they targeted ' +
                _follow(users_to_nights[night.target]) + '.'
            )
        elif night.action == MafiaAction.WATCH.code:
            night.add_report_line(
                'You watched ' + name + ', and determined that they were targeted by ' +
                _watch(users_to_nights[night.target]) + '.'
            )
        elif night.action == MafiaAction.REMEMBER.code:
            new_role = MafiaPlayer.objects.get(user=night.target0).role
            night.add_report_line(
                'You have remembered yourself as ' + _get_name(night.target0) + '. ' +
                'You are now a ' + MafiaRole.get_instance(new_role).name + '!'
            )

    # TODO: received action reporting

def _apply_action_results(nights, users_to_nights):
    pass # TODO

def advance_game(game):

    if game.time == MafiaGameTime.DAWN.code:
        # TODO
        game.time = MafiaGameTime.DUSK.code

    elif game.time == MafiaGameTime.DUSK.code:
        nights = MafiaPlayerNights.objects.filter(night_number=game.day_number)
        users_to_nights = {night.player.user: night for night in nights}
        _process_actions(nights, users_to_nights)
        _generate_reports(nights, users_to_nights)
        _apply_action_results(nights, users_to_nights)
        game.day_number += 1
        game.time = MafiaGameTime.DAWN.code

    else:
        raise ValueError("invalid value of game.time: " + `game.time`)
