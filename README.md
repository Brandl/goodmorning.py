# goodmorning.py
Let's not overengineer this. - Me 05.12.2021

## Architecture

1) Parse config.yml
2) foreach datasource in config.yml
3) fetch data => cache to prevent going over limit
4) weed out JSON
5) render through JINJA Template
6) print
