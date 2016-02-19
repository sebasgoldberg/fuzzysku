#!/bin/bash
pg_dump -U fuzzysku fuzzysku -f "backup/$(date +%Y-%m-%d).sql"
