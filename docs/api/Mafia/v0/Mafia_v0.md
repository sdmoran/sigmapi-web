Sigma Pi, Gamma Iota Mafia API, version 0.1
===========================================

Endpoints
---------

All endpoint URLs are prefixed with http://sigmapigammaiota.org/api/mafia/v0/.

### GET games/

**Response status code** | 200
**Response data** | Dict mapping game IDs to games for all existing games.
**Return data type** | ```{GameID: Game}```

### POST games/

- Creates a new game
- **Data format:** `{ 'name': String }`
- **Returns:** The created game
- **Return type:** `Game`
- **Notes:** An ID for the game will be generated, and the created game will be stored at
             games/<id>

### GET games/\<GameID\>/players/

- **Returns:** All list of the players in the game with the given GameID
- **Return type:** `Player[]`

### PUT games/\<GameID\>/players/\<Username\>/

- Adds the player with the given Username to the game
- **Argument format:** `{}`
- **Returns:** Information about the newly added player
- **Return type:** `Player`
- **Notes:** Adding a player who is already added is a no-op, and will still return the Player

### GET games/\<GameID\>/moderators/

- **Returns:** All the moderators for the game with the given ID
- **Return type:** ```User[]```
- **Notes:** Returned list does not include game creator



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