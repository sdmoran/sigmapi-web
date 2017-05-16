
Sigma Pi, Gamma Iota Mafia API, version 0.1
===========================================

Data Specifications
-------------------

### Game
```javascript
{
    'name':            String,        // Name of the game
    'created':         Date,          // Date the game was created
    'creator':         User,          // User that created the game
    'moderators':      Array<User>,   // List of moderators for the game
    'players':         Array<Player>, // List of players signed up for the game
    'day_number':      Integer,       // Day number. 0 if game is accepting players
    'is_accepting':    Boolean,       // Whether the game is still accpeting players
    'user_has_joined': Boolean        // Whether the logged-in user is signed up for this game
}
```

### User

```javascript
{
  'username': Username,    // The user's username
  'name': String,          // The user's full name
}
```
