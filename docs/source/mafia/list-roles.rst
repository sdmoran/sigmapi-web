
List roles
=================================================


Request
--------------------

GET /api/mafia/v0/roles/


Responses
--------------------

200 OK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returned in the event of a successful request.

Response Values
^^^^^^^^^^^^^^^

- roles (Dictionary): Mapping from role codes (2-digit, case-sensitive, unique identifiers of roles) to information about that role. The information includes:
    - code (String): The 2-digit role code
    - name (String): Name of the role
    - ... TODO document all fields ...

403 Permission Denied
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returned if the API user is not authenticated.
