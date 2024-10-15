# 🦊 FablePictor development

## Architecture

The database for this project is managed as a [Microsoft Excel spreadsheet](https://uantwerpen.sharepoint.com/:x:/r/sites/Bijzondere_Collecties/Publiekswerking/Fablepictor/Fabeldierencatalogus_definitief.xlsx?d=w17dd901460b0479792ae101f70298659&csf=1&web=1&e=Kerrp2)

Fablepictor works on the basis of CSV data export of this file (`data/data.csv`). There is a build step executes a Python script, which takes the data from this CSV file and transforms it into a number of JSON files.

These JSON files then serve as the backend for the frontend application. They contain the descriptive metadata (`metadata.json`), a search index (`index.json`) and the IIIF identifiers (`identifiers.json`). These are handled and queried with `index.html` and `index.js`.

All frontend elements (favicon, Bootstrap CSS, etc.) are present in the git repository.

## Build

In order to build the website, go to the `data` directory and execute `make build`.

## Testing

In order to test the website, you can spin up a Go webserver (`server/server.go`) and use the website on localhost.

## Deployment

This website is deployed on GitHub Pages. The only necessary step is to push the new version to GitHub.
