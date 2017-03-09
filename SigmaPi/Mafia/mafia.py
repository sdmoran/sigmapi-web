
from .models import *

def _do_single_switch(switcher0, switcher1, target0, target1, switch_map, users_to_nights):
    temp = switch_map[target0]
    switch_map[target0] = switch_map[target1]
    switch_map[target1] = temp
    users_to_nights[target0].switched_with = target1
    users_to_nights[target1].switched_with = target0
    users_to_nights[target0].add_switched_by(switcher0)
    users_to_nights[target1].add_switched_by(switcher1)
    
def _do_double_switch(switcher0, switcher1, target, users_to_nights):
    users_to_nights[target].switched_with = target
    users_to_nights[target].add_switched_by(switcher0)
    users_to_nights[target].add_switched_by(switcher1)

def _do_overlapping_switch(switcher0, switcher1, target0, overlapped_target, target1, users_to_nights):
    _do_single_switch(switcher0, switcher1, target0, target1, users_to_nights)
    _do_double_switch(switcher0, switcher1, overlapped_target, users_to_nights)

def _do_controlling_and_switching(players, nights, users_to_nights):

    # Clear previous calculations
    for night in nights:
        night.clear_switch()
        night.clear_control()

    # Do controlling
    control_nights = nights.filter(action=MafiaAction.CONTROL.code)
    if len(control_nights) > 1:
        raise MafiaError("more than one control action in night")
    control_night = control_nights[0] if len(control_nights) >= 1 else None
    if control_night and (not control_night.seduced):
        controlled = (control_night.target0, control_night.target1)
        users_to_nights[control_night.target0].controlled_to_target = control_night.target1
    else:
        controlled = None

    # Do switching
    switched = {player.user: player.user for player in players}
    switch_nights = nights.filter(action=MafiaAction.SWITCH.code)
    if len(switch_nights) > 2:
        raise MafiaError("more than two switch actions in night")
    if len(switch_nights) >= 2:
        s0 = switch_nights[0].player.user
        s1 = switch_nights[1].player.user
        s0t0 = switch_nights[0].target0_after_control
        s0t1 = switch_nights[0].target1
        s1t0 = switch_nights[1].target0_after_control
        s1t1 = switch_nights[1].target1
        if switch_nights[0].seduced and switch_nights[1].seduced:
            pass
        elif switch_nights[0].seduced:
            _do_single_switch(s1, s1, s1t0, s1t1, users_to_nights)
        elif switch_nights[1].seduced:
            _do_single_switch(s0, s0, s0t0, s0t1, users_to_nights)
        elif (s0t0 == s1t0 and s0t1 == s1t1) or (s0t0 == s1t1 and s0t1 == s1t0):
            _do_double_switch(s0, s1, s0t0, users_to_nights)
            _do_double_switch(s0, s1, s0t1, users_to_nights)
        elif s0t0 == s1t0:
            _do_overlapping_switch(s0, s1, s0t1, s0t0, s1t1, users_to_nights)
        elif s0t0 == s1t1:
            _do_overlapping_switch(s0, s1, s0t1, s0t0, s1t0, users_to_nights)
        elif s0t1 == s1t0:
            _do_overlapping_switch(s0, s1, s0t0, s0t1, s1t1, users_to_nights)
        elif s0t1 == s1t1:
            _do_overlapping_switch(s0, s1, s0t0, s0t1, s1t0, users_to_nights)
        else:
            _do_single_switch(s0, s0, s0t0, s0t1, users_to_nights)
            _do_single_switch(s1, s1, s1t0, s1t1, users_to_nights)
    elif len(switch_nights) >= 1 and not switch_nights[0].seduced:
        s = switch_nights[0].player.user
        _do_single_switch(
            s, s,
            switch_nights[0].target0_after_control,
            switch_nights[0].target1,
            users_to_nights
        )

    # Return switch map
    return switched, controlled

def _do_seduction(players, nights, users_to_nights):
    seduce_map = {player.user: False for player in players}
    for seduce_night in nights.filter(action=MafiaAction.SEDUCE.code):
        users_to_nights[seduce_night.target0].add_seduced_by(seduce_night.player.user)
    return seduce_map

def _process_player_nights(players, nights):

    # Collect a map from users to nights
    users_to_nights = {player.user: nights.get(player=player) for player in players}
    
    # Repeat controlling/switching and seduction until we reach a stable state
    switched, controlled = _do_switching_and_controlling(
        players, nights, users_to_nights
    )
    seduced = _do_seduction(players, nights, users_to_nights)
    while True:
        new_switched, new_controlled = _do_controlling_and_switching(
            players, nights, users_to_nights
        )
        new_seduced = _do_seduction(players, nights, users_to_nights)
        stable = (
            new_controlled == controlled and 
            new_switched == switched and 
            new_seduced == seduced
        )
        controlled = new_controlled
        switched = new_switched
        seduced = new_seduced
        if stable:
            break

    # Mark framed targets
    for frame_night in MafiaAction.objects.filter(action=MafiaAction.FRAME.code):
        if frame_night.seduced:
            continue
        target_night = users_to_nights[switched[frame_night.target0_after_control]]
        target_night.framed = True
        target_night.add_other_targeted_by(frame_night.player.user)

    # Mark protected targets
    for protect_night in MafiaAction.objects.filter(action=MafiaAction.PROTECT.code):
        if protect_night.seduced:
            continue
        target_night = users_to_nights[switched[protect_night.target0_after_control]]
        target_night.protected = True
        target_night.add_other_targeted_by(protect_night.player.user)

    # Mark defended targets (but do not yet kill those who attack such targets)
    for defend_night in MafiaAction.objects.filter(action=MafiaAction.DEFEND.code):
        if defend_night.seduced:
            continue
        target_night = users_to_nights[switched[defend_night.target0_after_control]]
        target_night.defended = True
        target_night.add_other_targeted_by(defend_night.player.user)

    # Do corruption
    for corrupt_night in MafiaAction.objects.filter(action=MafiaAction.CORRUPT.code):
        if corrupt_night.seduced:
            continue
        target_night = users_to_nights[switched[corrupt_night.target0_after_control]]
        target_night.attempted_corrupted = True
        target_night.add_other_targeted_by(corrupt_night.player.user)
        if target_night.corrupted:
            control_night.player.user.died_for_other_reason = True

    # Do killing
    # TODO

    # Mark doused/un-doused players
    for douse_night in MafiaAction.objects.filter(action=MafiaAction.DOUSE.code):
        if douse_night.seduced:
            continue
        target_night = users_to_nights[switched[douse_night.target0_after_control]]
        target_night.doused = True
        target_night.add_other_targeted_by(douse_night.player.user)
    for un_douse_night in MafiaAction.objects.filter(action=MafiaAction.UN_DOUSE.code):
        if un_douse_night.seduced:
            continue
        target_night = users_to_nights[switched[un_douse_night.target0_after_control]]
        target_night.un_doused = True
        target_night.add_other_targeted_by(un_douse_night.player.user)

    # Mark disposed players
    for dispose_night in MafiaAction.objects.filter(action=MafiaAction.DISPOSE.code):
        if dispose_night.seduced:
            continue
        target_night = users_to_nights[switched[dispose_night.target0_after_control]]
        target_night.dispose_night = True
        target_night.add_other_targeted_by(dispose_night.player.user)
        if target_night.died:
            dispose_night.successfully_performed_dispose = True

def _apply_player_nights(players, nights):
    pass # TODO

def perform_night(night):
    players = MafiaPlayers.objects.filter(status=MafiaPlayerStatus.ALIVE)
    nights = MafiaPlayerNights.objects.filter(night=night)
    _process_player_nights(players, nights)
    _apply_player_nights(players, nights)
