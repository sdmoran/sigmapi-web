# Written by Kyle McCormick

Sigma Pi, Gamma Iota Mafia API, version 0.1
===========================================


Endpoint Notes
--------------

All endpoint URLs are prefixed with http://sigmapigammaiota.org/api/mafia/v0.

All endpoints other than About (`GET .../`) return 403s for unauthenticated users.

If no condition is listed for a referenced status code, assume it is the default status code,
and is returned in the event of a successful request.

An example endpoint description is shown below:

### Endpoint title

`METHOD .../path/to/endpoint/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Action            | If it is a POST, PUT, DELETE, or PATCH, how the endpoint modifies state            |                                            |
| Query data format | If it is a POST, PUT, DELETE, or PATCH, the expected input data format             |                                                             |
| xxx: Condition    | A condition for the xxx status code to be returned                                 |
| xxx: Data         | If xxx is returned, a description of the returned data                             |
| xxx: Data format  | If xxx is returned, the format of the returned data                                |                                                                             |
| xxx: Headers      | If xxx is returned, what special headers are provided                              |


Endpoint Descriptions
---------------------

### About

`GET .../`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| 200: Data         | A short description of the purpose of the API and a link to this documentation.    |
| 200: Data format  | `{ 'about': String, 'documentation_url': String }`  

### List roles

`GET .../roles/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| 200: Data         | Dict mapping RoleCodes to Roles all existing roles.                                |
| 200: Data format  | `{ ... RoleCode: Role ... }`                                                       |

### List action types

`GET .../actiontypes/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| 200: Condition    | None                                                                               |
| 200: Data         | Dict mapping ActionTypeCodes to ActionTypes all existing action types.             |
| 200: Data format  | `{ ... ActionTypeCode: ActionType ... }`                                           |

### List games

`GET .../games/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| 200: Condition    | None                                                                               |
| 200: Data         | Dict mapping GameIDs to Games for all existing games.                              |
| 200: Data format  | `{ ... GameID: Game ... }`                                                         |

### Create game

`POST .../games/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Action            | Creates a new game.                                                                |
| Query data format | `{ 'name': String }`                                                               |
| 400: Condition    | `name` is missing or empty                                                         |
| 201: Condition    | No other errors                                                                    | 
| 201: Data         | The created game.                                                                  |
| 201: Data format  | `Game`                                                                             |
| 201: Headers      | Location: Path to the created game (`.../games/<game_id>`)                         |

### Get game

`GET .../games/\<game_id:GameID\>/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| 404: Condition    | `game_id` is invalid                                                               |
| 200: Data         | Information about the game with ID `game_id`.                                      |
| 200: Data format  | `Game`                                                                             |

### Delete game

`DELETE .../games/\<game_id:GameID\>/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Action            | Deletes the game with the ID `game_id`.                                            |
| 404: Condition    | `game_id` is invalid                                                               |
| 400: Condition    | Requesting user does not have moderator privelages or game is finished             |
| 204: Data         | None                                                                               |

### List moderators for game

`GET .../games/\<game_id:GameID\>/moderators/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| CHANGEME          | 404 if `game_id` is invalid; 200 otherwise                                         |
| 200: Data         | List of the moderators for the game with the ID `game_id`.                         |
| 200: Data format  | `User[]`                                                                           |
| Notes             | Returned list does not include game creator.                                       |

### Add moderator to game

`PUT .../games/\<game_id:GameID\>/players/\<username:Username\>/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Action            | Crowns the user with the given Username as a moderator of the game.                |
| Query data format | `{}`                                                                               |
| CHANGEME          | 404 if `game_id` is invalid; 400 if `username` does not refer to a User or refers to the creator or a player; 303 if user is already crowned as a moderator; 201 otherwise |
| 201: Data         | Information about the newly-crowned user.                                          |
| 201: Data format  | `Game`                                                                             |
| 201: Headers      | Location: Path to information on the newly-crowned moderator                       |
| 303: Headers      | Location: Path to information on the already-crowned moderator                     |

### Get players in game

`GET .../games/\<game_id:GameID\>/players/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| CHANGEME          | 404 if `game_id` is invalid; 200 otherwise                                         |
| 200: Data        | List of the players in the game with the ID `game_id`.                             |
| 200: Data format | `Player[]`                                                                         |

### Add player to game

`PUT .../games/\<game_id:GameID\>/players/\<username:Username\>/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Action            | Adds the user with the given Username to the game.                                 |
| Query data format | `{}`                                                                               |
| CHANGEME          | 404 if `game_id` is invalid; 400 if `username` does not refer to a User or refers to the creator or a moderator; 400 if game is not accepting players; 303 if user is already added to game; 201 otherwise |
| 201: Data        | Information about the newly-added player.                                          |
| 201: Data format | `Game`                                                                             |
| 201: Headers     | Location: Path to information on the newly-added player                            |
| 303: Headers     | Location: Path to information on the already-added player                          |

### Get player in game

`GET .../games/\<game_id:GameID\>/players/\<username:Username\>/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| CHANGEME          | 404 if `game_id` is invalid or `username` does not refer to a player; 200 otherwise|
| 200: Data        | Information about the player `username` in the game `game_id`                      |
| 200: Data format | `Player`                                                                           |

### Remove player from game

`REMOVE .../games/\<game_id:GameID\>/players/\<username:Username\>/`

| Property          | Value                                                                              |
| ----------------- | ---------------------------------------------------------------------------------- |
| Action            | Removes the player `username` from the game with the ID `game_id`.                 |
| CHANGEME          | 404 if `game_id` is invalid; 400 if requesting user does not have moderator privelages or game is finished; 204 (No Content) otherwise |


Data Specifications
-------------------

### Game

Information about a Mafia game.

```javascript
{
    'id':              GameID    // ID of the game
    'name':            String,   // Name of the game
    'created':         Date,     // Date the game was created
    'creator':         User,     // User that created the game
    'moderators':      User[],   // List of moderators for the game. Does not include the
                                 //     game's creator
    'players':         Player[], // List of players signed up for the game
    'day_number':      Integer,  // Day number. 0 if game is accepting players
    'is_accepting':    Boolean,  // Whether the game is still accpeting players
    'user_has_joined': Boolean   // Whether the logged-in user is signed up for this game
}
```

### GameID

A String uniquely identifying a game.

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

A case-sensitive, two-character String that uniquely identifies a role. The first letter
indicates the faction (V => Village, R => Rogue, M => Mafia).

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
    'executioner_target':       User      // If the player's role is Executioner, their target;
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

A case-sensitive, two-character String that uniquely identifies an action type.

### User

Information about a user of the website.

```javascript
{
    'username': Username, // The user's username
    'name': String,       // The user's first and last name. At most 61 characters
}
```

### Username

A String. See the [Django username documentation](https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User.username)
for details.

### Date

A String in the format `yyyy-mm-dd`.