
Sigma Pi, Gamma Iota Mafia API, version 0.1
===========================================

Data Specifications
-------------------

### Game

Information about a Mafia game.

```javascript
{
    'name':            String,        // Name of the game
    'created':         Date,          // Date the game was created
    'creator':         User,          // User that created the game
    'moderators':      Array<User>,   // List of moderators for the game. Does not include
                                      //    the game's creator
    'players':         Array<Player>, // List of players signed up for the game
    'day_number':      Integer,       // Day number. 0 if game is accepting players
    'is_accepting':    Boolean,       // Whether the game is still accpeting players
    'user_has_joined': Boolean        // Whether the logged-in user is signed up for this game
}
```

### Player

A wrapper around User that contains Game-playing information.

```javascript
{
    'user':          User,            // User that this player is
    'status':        String,          // Either 'Alive', 'Lynched', or 'Died at Night'
    'revealed_role': Role,            // The player's role, as revealed, if it has been revealed;
                                      //    null otherwise
    'actual_role':   Role             // The player's true role if the logged-in user has
                                      //    moderator privelages; null otherwise.
    'secret_info':   SecretPlayerInfo // Further information about the player if the logged-in
                                      //     user is this player or has moderator privelages;
                                      //     null otherwise.
}
```

### Role

Information about a Mafia role.

```javascript
{
    'code': RoleCode, // ...
    'name': ...       // ...
}
```

## SecretPlayerInfo

Information about a player that is only available to the player themselves and
to those with moderator privelages.

```javascript
{
    ...
}
```

### User

Information about a user of the website.

```javascript
{
  'username': Username,    // The user's username
  'name': String,          // The user's first and last name. At most 61 characters
}
```

### Username

A String. See the [Django username documentation]
(https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User.username)
for details.

### Date

A String in the format yyyy-mm-dd.
