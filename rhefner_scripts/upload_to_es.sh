#!/usr/bin/env bash

csv2es --index-name messages --doc-type message --import-file data/patched_messages.csv --mapping-file es_mapping.json --delimiter ',' --delete-index
