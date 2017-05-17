
Sigma Pi, Gamma Iota Mafia API, version 0.1
===========================================

Data Specifications
-------------------

### Game

Information about a Mafia game.

```javascript
{
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

### Player

A wrapper around User that contains Game-playing information.

```javascript
{
    'user':          User,             // User that this player is
    'status':        String,           // Either 'Alive', 'Lynched', or 'Died at Night'
    'revealed_role': Role,             // The player's role, as revealed, if it has been
                                       //     revealed; null otherwise
    'secret_info':   SecretPlayerInfo, // Further information about the player. Non-null if
                                       // the logged-in user is this player or has moderator
                                       // privelages; null otherwise
    'actual_role':   Role              // Player's true role. Non-null if the logged-in user
                                       //    has moderator privelages; null otherwise
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

A case-sensitive, two-character String that uniquely identifies a role. The first letter indicates the faction (V => Village, R => Rogue, M => Mafia).

## ActionUsability

Information about an ability to use an action.

```javascript
{
    'action': Action, // The action
    'uses':   Integer // Specification of how often and how many times action can be used.
                      //     -2           => usable every other night, unlimited uses
                      //     -1           => usable every night, unlimited uses
                      //     n, where n>0 => usable every night, n uses
}
```

### Action

Information about an action.

```javascript
{
    'code': ActionCode, // Code uniquely identifying this action
    'name': String      // Name of the action
}
```

### ActionCode

A case-sensitive, two-character String that uniquely identifies an action.

### SecretPlayerInfo

Information about a player that is only available to the player themselves and
to those with moderator privelages.

```javascript
{
    'apparant_role':       Role,    // Role that the player sees themselves as
    'old_apparant_role':   Role,    // Role that the player saw themselves as before they were
                                    //    corrupted/converted
    'older_apparant_role': Role,    // Role that the player saw themselves as before two or
                                    //    conversions
    'actions_availabilities':
              ActionAvailability[], // Actions available to the user this (coming) night
    'doused':              Boolean, // Whether the player has been doused by an Arsonist
    'executioner_target':  User     // If the player's role is Executioner, their target;
                                    //    otherwise null
}
```

### ActionAvailability

Information about the availability of an action to a player.

```javascript
{
    'action': Action,     // The action
    'uses_left': Integer, // Uses remaining for this action. -1 if unlimited
}
```

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
