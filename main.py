from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision

@app.route('/')
def homepage():
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    # Use the Cloud Datastore client to fetch information from Datastore about
    # each photo.
    query = datastore_client.query(kind='Faces')
    image_entities = list(query.fetch())

    # Return a Jinja2 HTML template and pass in image_entities as a parameter.
    return render_template('homepage.html', image_entities=image_entities)

    # # Create a Cloud Datastore client.
    # datastore_client = datastore.Client()
    #
    # # Fetch the current date / time.
    # current_datetime = datetime.now()
    #
    # # The kind for the new entity.
    # kind = 'Faces'
    #
    # # The name/ID for the new entity.
    # name = blob.name
    #
    # # Create the Cloud Datastore key for the new entity.
    # key = datastore_client.key(kind, name)
    #
    # # Construct the new entity using the key. Set dictionary values for entity
    # # keys blob_name, storage_public_url, timestamp, and joy.
    # entity = datastore.Entity(key)
    # entity['blob_name'] = blob.name
    # entity['image_public_url'] = blob.public_url
    # entity['timestamp'] = current_datetime
    # entity['joy'] = face_joy
    #
    # # Save the new entity to Datastore.
    # datastore_client.put(entity)
