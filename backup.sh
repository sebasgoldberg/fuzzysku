#!/bin/bash
FILENAME="backup/$(date +%Y-%m-%d).sql"
pg_dump -U fuzzysku fuzzysku -f "$FILENAME"
tar -zcvf "$FILENAME.tar.gz" "$FILENAME"
rm "$FILENAME"
