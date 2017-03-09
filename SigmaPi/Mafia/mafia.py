
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
        raise MafiaError("more than two switch actions in single night")

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
    elif len(switch_nights) >= 1 and not switch_nights[0].seduced_or_died
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
        if MafiaNightStatus.TERMINATD.code in [target_night.status, killed_status]:
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

def _process_player_nights(nights):

    # Collect a map from users to nights
    users_to_nights = {night.player.user: night for night in nights}

    # Do control, killing those that try to control on-guard players
    control_nights = nights.filter(action=MafiaAction.CONTROL.code)
    if len(control_nights) > 1:
        raise MafiaError("more than one control action in single night")
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
        is_direct_offense = MafiaAction.get_instance(night.action).is_direct_offense
        if is_direct_offense:
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

    # Killing role: Bomb
    bomb_nights = MafiaPlayerNights.objects.filter(player__role=MafiaRole.BOMB.code)
    if len(bomb_nights) > 1:
        raise MafiaError("more than one bomb in game")
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

def _apply_player_nights(nights):
    pass # TODO

def perform_night(night):
    nights = MafiaPlayerNights.objects.filter(night=night)
    _process_player_nights(nights)
    _apply_player_nights(nights)
