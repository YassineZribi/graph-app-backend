from bson.objectid import ObjectId

# Utility function to convert ObjectId to string
def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj