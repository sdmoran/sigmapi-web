#!/bin/bash
echo 'Warning: This will overwrite any backups that have been already made today.'
echo 'Hit Ctrl-C at the password prompt to cancel.'
pg_dump -U sigmapi sigmapi_web -p 5432 -f ../db_backups/$(date +'%Y-%m-%d').sql

