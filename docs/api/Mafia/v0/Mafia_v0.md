
Sigma Pi, Gamma Iota Mafia API, version 0.1
===========================================


Endpoint Notes
--------------

All endpoint URLs are prefixed with http://sigmapigammaiota.org/api/mafia/v0.

All endpoints other than About (`GET .../`) return 403s for unauthenticated users.

If multiple status code conditions are listed, the status code of the first satisfied condition will be returned.

If a status code is referenced but no Condition is listed for it, assume it is the default status code,
and is returned in the event of a successful request.

An example endpoint description is shown below:

### Example endpoint title

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `METHOD .../path/to/example/endpoint/<var_name:VarType>`                           |
| Query data format | If it is a POST, PUT, DELETE, or PATCH, the expected input data format             |                                                             |
| XXX Condition     | The condition upon which the XXX status code is returned                           |
| XXX Action        | If XXX is returned, how state is modified                                          |                                            |
| XXX Data          | If XXX is returned, a description of the returned data                             |
| XXX Data format   | If XXX is returned, the format of the returned data                                |                                                                             |
| XXX Headers       | If XXX is returned, what special headers are provided                              |


Endpoint Descriptions
---------------------

### About

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../`                                                                         |
| 200 Data          | A short description of the purpose of the API and a link to this documentation     |
| 200 Data format   | `{ 'about': String, 'documentation_url': String }`                                 |

### List roles

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../roles/`                                                                   |
| 200 Data          | Dict mapping RoleCodes to Roles all existing roles                                 |
| 200 Data format   | `{ ... RoleCode: Role ... }`                                                       |

### Get role

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../roles/<role_code:RoleCode>/`                                              |
| 404 Condition     | `role_code` is invalid                                                             |
| 200 Data          | Information about Role referred to by `role_code`                                  |
| 200 Data format   | `Role`                                                                             |

### List action types

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../actiontypes/`                                                             |
| 200 Condition     | None                                                                               |
| 200 Data          | Dict mapping ActionTypeCodes to ActionTypes all existing action types              |
| 200 Data format   | `{ ... ActionTypeCode: ActionType ... }`                                           |

### Get action type

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../actiontypes/<action_type_code:ActionTypeCode>/`                           |
| 404 Condition     | `action_type_code` is invalid                                                      |
| 200 Data          | Information about ActionType referred to by `action_type_code`                     |
| 200 Data format   | `ActionType`                                                                       |

### List games

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/`                                                                   |
| 200 Condition     | None                                                                               |
| 200 Data          | Dict mapping GameIDs to Games for all existing games                               |
| 200 Data format   | `{ ... GameID: Game ... }`                                                         |

### Create game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `POST .../games/`                                                                  |
| Query data format | `{ 'name': String }`                                                               |
| 400 Condition     | `name` is missing or empty                                                         |
| 200 Action        | Creates a new game                                                                 |
| 201 Data          | Information about the created game                                                 |
| 201 Data format   | `Game`                                                                             |
| 201 Headers       | Location: Path to the created game (`.../games/<game_id>`)                         |

### Get game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/`                                                  |
| 404 Condition     | `game_id` is invalid                                                               |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 200 Data          | Information about Game `game_id`                                                   |
| 200 Data format   | `Game`                                                                             |

### Delete game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `DELETE .../games/<game_id:GameID>/`                                               |
| 404 Condition     | `game_id` is invalid                                                               |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | Game `game_id` is finished                                                         |
| 204 Action        | Deletes the game with the ID `game_id`                                             |

### Get game status

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/status/`                                           |
| 404 Condition     | `game_id` is invalid                                                               |
| 200 Data          | Information about the status of Game`game_id`                                      |
| 200 Data format   | `GameStatus`                                                                       |

### Start/advance game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `PATCH .../games/<game_id:GameID>/status/`                                         |
| Query data format | `{ 'action': 'start_game'|'begin_day'|'end_day'|'begin_night'|'end_night' }`       |
| 404 Condition     | `game_id` is invalid                                                               |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | Action is invalid given current status. For example, `'begin_night'` during dawn.  |
| 200 Data          | Information about the newly-modified status of Game `game_id`                      |
| 200 Data format   | `GameStatus`                                                                       |

### List moderators for game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/moderators/`                                       |
| 404 Condition     | `game_id` is invalid                                                               |
| 200 Data          | List of the moderators for Game `game_id`                                          |
| 200 Data format   | `User[]`                                                                           |
| Notes             | Returned list does not include game creator                                        |

### Get moderator for game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/moderators/<username:Username>/`                   |
| 404 Condition     | `game_id` is invalid or User `username` is not a moderator in Game `game_id`       |
| 200 Data          | Information about the User `username` that moderates the Game `game_id`            |
| 200 Data format   | `User`                                                                             |

### Add moderator to game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `PUT .../games/<game_id:GameID>/moderators/<username:Username>/`                   |
| 404 Condition     | `game_id` is invalid                                                               |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | `username` does not refer to a User OR it refers to the creator or a player        |
| 303 Condition     | User `username` is already crowned as a moderator                                  |
| 303 Headers       | Location: Path to information on already-crowned moderator                         |
| 200 Action        | Crowns the user with the given Username as a moderator of the game                 |
| 200 Data          | Information about the newly-crowned user                                           |
| 200 Data format   | `User`                                                                             |

### Remove moderator from game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `DELETE .../games/<game_id:GameID>/moderators/<username:Username>/`                |
| 404 Condition     | `game_id` is invalid or User `username` is not a moderator for Game `game_id`      |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | Game is finished                                                                   |
| 204 Action        | Un-crowns the User `username` as a moderator the Game `game_id`                    |

### List players in game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/players/`                                          |
| 404 Condition     | `game_id` is invalid                                                               |
| 200 Data          | List of the players in the game with the ID `game_id`                              |
| 200 Data format   | `Player[]`                                                                         |

### Get player in game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/players/<username:Username>/`                      |
| 404 Condition     | `game_id` is invalid or User `username` is not a player in Game `game_id`          |
| 200 Data          | Information about the Player `username` in the Game `game_id`                      |
| 200 Data format   | `Player`                                                                           |

### Add player to game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `PUT .../games/<game_id:GameID>/players/<username:Username>/`                      |
| 404 Condition     | `game_id` is invalid                                                               |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | `username` does not refer to a User or refers to the creator or a moderator        |
| 400 Condition     | Game `game_id` game is not accepting players                                       |
| 303 Condition     | User `username` is already added to game                                           |
| 303 Headers       | Location: Path to information on the already-added player                          |
| 200 Action        | Adds the User with the given Username to the game                                  |
| 200 Data          | Information about the newly-added player                                           |
| 200 Data format   | `Player`                                                                           |

### Remove player from game

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `DELETE .../games/<game_id:GameID>/players/<username:Username>/`                   |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | Game is finished                                                                   |
| 204 Action        | Removes the Player `username` from the Game `game_id`                              |

### Get actual role of player

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/players/<username:Username>/role/`                 |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 200 Data          | Information about the role of Player `username` in Game `game_id`                  |
| 200 Data format   | `Role` if role assigned, `null` otherwise                                          |

### Assign player to role

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `PUT .../games/<game_id:GameID>/players/<username:Username>/role/`                 |
| Query data format | `{ 'role_code': RoleCode }`                                                        |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | Game `game_id` game is not accepting players                                       |
| 204 Action        | Sets the role of Player `username` in Game `game_id`                               |

### Unassign player from role

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `DELETE .../games/<game_id:GameID>/players/<username:Username>/role/`              |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 400 Condition     | Game `game_id` game is not accepting players                                       |
| 204 Action        | Sets the role of Player `username` in Game `game_id` to unassigned                 |

### Get lynch votes of a player

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/players/<username:Username>/votes/`                |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 200 Data          | List of all Player `username`'s lynch votes up to the current day                  |
| 200 Data format   | `LynchVote[]`                                                                      |

### Set lynch vote of a player for current day

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `POST .../games/<game_id:GameID>/players/<username:Username>/votes/`               |
| Query data format | `LynchVote`                                                                        |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user is not `username` and does not have moderator privelages           |
| 400 Condition     | Game `game_id` has not begun or has finished                                       |
| 204 Action        | Sets the lynch vote of Player `username` in Game `game_id` for the current day     |

### Get actions of a player

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/players/<username:Username>/actions/`              |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user is not `username` and does not have moderator privelages           |
| 200 Data          | List of all Player `username`'s  actions up to the current day                     |
| 200 Data format   | `Action[]`                                                                         |

### Set action of a player for current day

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `POST .../games/<game_id:GameID>/players/<username:Username>/actions/`             |
| Query data format | `Action`                                                                           |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user is not `username` and does not have moderator privelages           |
| 204 Action        | Sets the action of Player `username` in Game `game_id` for the current day         |

### Get night results for a player

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/players/<username:Username>/nightresults/`         |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 403 Condition     | Requesting user is not `username` and does not have moderator privelages           |
| 200 Data          | List of all Player `username`'s night results up to the current night              |
| 200 Data format   | `PlayerNightResult[]`                                                              |
| 200 Notes         | Returned array is indexed by night number. Because nights are 1-indexed, element 0 is null. |

### Get night result for a player for a specific night

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/players/<username:Username>/nightresults/<night_number:Integer>/` |
| 404 Condition     | `game_id` is invalid or User `username` is not a Player in Game `game_id`          |
| 404 Condition     | Night `night_number` is less than 1 or greater than Game `game_id`'s day number    |
| 403 Condition     | Requesting user is not `username` and does not have moderator privelages           |
| 200 Data          | Player `username`'s night results for night `night_number`                         |
| 200 Data format   | `PlayerNightResult`                                                                |        

### Get town night results

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/nightresults/`                                     |
| 404 Condition     | `game_id` is invalid                                                               |
| 200 Data          | List of all town night results for every night up to the current one               |
| 200 Data format   | `TownNightResult`                                                                  |
| 200 Notes         | Returned array is indexed by day number. Because nights are `1-indexed, element 0 is null. |

### Get town night result for specific night

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/nightresults/<night_number:Integer>/`              |
| 404 Condition     | `game_id` is invalid                                                               |
| 404 Condition     | `night_number` is less than 1 or greater than Game `game_id`'s day number          |
| 200 Data          | Town night results for night `night_number`                                        |
| 200 Data format   | `TownNightResult`                                                                  |        

### Set town night result for specific night

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `PUT .../games/<game_id:GameID>/nightresults/<night_number:Integer>/`              |
| Query data format | `{ 'town_night_result': TownNightResult }`                                         |
| 404 Condition     | `game_id` is invalid                                                               |
| 404 Condition     | `night_number` is less than 1 or greater than Game `game_id`'s night number        |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 204 Action        | Sets the night result of Game `game_id` for night `night_number` to `town_night_result` |

### Reset town night result for specific night to default

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `DELETE .../games/<game_id:GameID>/nightresults/<night_number:Integer>/`           |
| 404 Condition     | `game_id` is invalid                                                               |
| 404 Condition     | `night_number` is less than 1 or greater than Game `game_id`'s night number        |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 204 Action        | Resets the night result of Game `game_id` for night `night_number` to the automatically generated default. |

### Get town day results

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/dayresults/`                                       |
| 404 Condition     | `game_id` is invalid                                                               |
| 200 Data          | List of all town day results for every day up to the current one                   |
| 200 Data format   | `TownDayResult`                                                                    |
| 200 Notes         | Returned array is indexed by day number. Because days are 1-indexed, element 0 is null. |

### Get town day result for specific day

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `GET .../games/<game_id:GameID>/dayresults/<day_number:Integer>/`                  |
| 404 Condition     | `game_id` is invalid                                                               |
| 404 Condition     | `day_number` is less than 1 or greater than Game `game_id`'s day number            |
| 200 Data          | Town day results for day `day_number`                                              |
| 200 Data format   | `TownDayResult`                                                                    |        

### Set town day result for specific day

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `PUT .../games/<game_id:GameID>/dayresults/<day_number:Integer>/`                  |
| Query data format | `{ 'town_day_result': TownDayResult }`                                             |
| 404 Condition     | `game_id` is invalid                                                               |
| 404 Condition     | `day_number` is less than 1 or greater than Game `game_id`'s day number            |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 204 Action        | Sets the day result of Game `game_id` for day `day_number` to `town_day_result`    |

### Reset town day result for specific day to default

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Query             | `DELETE .../games/<game_id:GameID>/dayresults/<day_number:Integer>/`               |
| 404 Condition     | `game_id` is invalid                                                               |
| 404 Condition     | `day_number` is less than 1 or greater than Game `game_id`'s day number            |
| 403 Condition     | Requesting user does not have moderator privelages for Game `game_id`              |
| 204 Action        | Resets the day result of Game `game_id` for day `day_number` to the automatically generated default. |

Data Specifications
-------------------

### Game

Information about a Mafia game.

```javascript
{
    'id':              GameID     // ID of the game
    'name':            String,    // Name of the game
    'created':         Date,      // Date the game was created
    'creator':         User,      // User that created the game
    'moderators':      User[],    // List of moderators for the game. Does not include the
                                  //     game's creator
    'players':         Player[],  // List of players signed up for the game
    'status':          GameStatus // Status of the game
    'user_has_joined': Boolean    // Whether the logged-in user is signed up for this game
}
```

### GameID

An alphanumeric String that uniquely identifies a game.

### GameStatus

Information about the status of gameplay in a game.

```javascript
{
    'day_number':      Integer,   // Day number. 0 if game is still accepting players
    'time':            String,    // Either 'dawn', 'day', 'dusk', or 'night'
    'is_accepting':    Boolean,   // Whether the game is still accepting players
    'is_finished':     Boolean    // Whether the game has finished
    'winners':         Username   // List of the players who won. Null if game is not finished
}
```

### Player

A wrapper around User that contains Game-playing information.

```javascript
{
    'user':               User,             // User that this player is
    'status':             String,           // Either 'Alive', 'Lynched', or 'Died at Night'
    'revealed_role_code': RoleCode          // Code for he player's role, as revealed, if it
                                            //     has been revealed; null otherwise
    'secret_info':        SecretPlayerInfo, // Further information about the player. Non-null
                                            //     if and only if the logged-in user is this
                                            //     player, the loggin-in user has moderator
                                            //     privelages, or the game is finished
    'actual_role_code':   RoleCode          // Code for player's true role. Non-null if and
                                            //     only if:
                                            //       - The logged-in user has moderator 
                                            //         privelages or the game is finished, AND
                                            //       - The role has been assigned
}
```

### Role

Information about a Mafia role.

```javascript
{
    'code': RoleCode,                        // Code uniquely identifying this role
    'name': String,                          // Name of the role
    'action_usabilities': ActionUsability[], // Actions that the role can perform and how
                                             //     often they can can use them
    'night_immune': Boolean,                 // Whether this role is immune to attack and
                                             //     conversion at night
    'immune_to_seduction': Boolean,          // Whether this role is immune to seduction by
                                             //     Escorts and Hookers
}
```

### RoleCode

A case-sensitive, two-character alphanumeric String that uniquely identifies a role.
The first letter indicates the faction (V => Village, R => Rogue, M => Mafia).

### ActionUsability

Information about an ability to use an action.

```javascript
{
    'action_type_code': ActionTypeCode, // Code for the type of the usable action
    'uses':             Integer         // How often and how many times action can be used.
                                        //     -2 => usable every other night, unlimited uses
                                        //     -1 => usable every night, unlimited uses
                                        //     n, where n> 0 => usable every night, n uses
}
```

### SecretPlayerInfo

Information about a player that is only available to the player themselves and
to those with moderator privelages.

```javascript
{
    'apparant_role_code':       RoleCode, // Code for role that the player sees themselves as
    'old_apparant_role_code':   RoleCode, // Code for role that the player saw themselves as
                                          //     before they were corrupted/converted
    'older_apparant_role_code': RoleCode, // Code for role that the player saw themselves as
                                          //      before two corruptions and/or conversions
    'actions_availabilities':
              ActionAvailability[],       // Actions available to the user this (coming) night
    'doused':                   Boolean,  // Whether the player has been doused by an Arsonist
    'executioner_target':       Username  // If the player's role is Executioner, their target;
                                          //    otherwise null
}
```

### ActionAvailability

Information about the availability of an action to a player.

```javascript
{
    'action_type_code': ActionTypeCode, // Code for type of the available action
    'uses_left':        Integer,        // Uses remaining for this action. -1 if unlimited
}
```

### Action

Information about an action that was performed by a player. An action is an
association between an action type and targets.

```javascript
{
    'action_type_code': ActionTypeCode // Code for the action type
    'target0_username': Username       // Username of the first target
    'target1_username': Username       // Username of the second target
}
```

### ActionType

Information about an action type. Action types include slay, investigate,
seduce, etc.

```javascript
{
    'code':                ActionTypeCode, // Code uniquely identifying this action type
    'name':                String          // Name of the action as it appears to the user.
                                           //     Not a unique identifier
    'num_targets':         Integer,        // Number of targets this action takes. 0, 1, or 2
    'targets_can_be_self': Boolean[],      // Array of Booleans, each signifying whether the
                                           //     target at that position can be the action
                                           //     performer themselves. For example,
                                           //     [True, False] would indicate that the 1st
                                           //     target can be the performer but the 2nd can't
    'targets_dead':        Boolean         // Whether targets are selected from all dead
                                           //     players instead of the live ones
}
```

### ActionTypeCode

A case-sensitive, two-character alphanumeric String that uniquely identifies an action type.

### User

Information about a user of the website.

```javascript
{
    'username': Username, // The user's username
    'name': String,       // The user's first and last name. At most 61 characters
}
```

### LynchVote

`null` for an abstain, an empty String for a "No Lynch" vote, or a Username for a vote to lynch.

### Username

A String. See the [Django username documentation](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User.username)
for details.

### Date

A String in the format `yyyy-mm-dd`.

### PlayerNightResult

An array of Strings, where each String describes something that the Player did or had happen to
them that night. Automatically generated.

### TownNightResult

A String describing what happened in the town on a specific night.
Automatically generated, but can be overridden by those with moderator privelages.

### TownDayResult

A String describing what happened in the town on a specific day. 
Automatically generated, but can be overridden by those with moderator privelages.

Other Notes
-----------

A user has 'Moderator privelages' over a game if any of the following are true:
1. They created the game
2. They were crowned a moderator of the game
3. They have global moderator permissions
