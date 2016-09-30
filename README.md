# Kodi-Videoboard
A python flask app and a kodi script to interrupt playback for short clips

<a href="https://flax.systems/dank.gif">Proof of concept</a>

The server app expects kodi under KODI_URL and a sqlite3 Database (with a table as defined in clipdb.schema) under DB_PATH.
The type of a clip is either audio or video
