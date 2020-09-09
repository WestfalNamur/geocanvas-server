# Gempy REST service (POC).

## Architecture

Each Gempy model will be a Flask app. The core engine is an instance of the Gempy container class
that constitutes a GemPy model. This instance referred to as "geo_model". The geo_model is wrapped
by "gmodel" which is responsible for processing incoming and outgoing data. The final layer is the
API layer which provides REST capabilities provided by Flask-RESTful.

### Data
No reordering of Series or Surfaces to avoide complexity an possbile errors that might crash the
app.

## Todos

Status codes, Fixtures, No-Data error handle for API,
