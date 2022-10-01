from django.shortcuts import render
from pymongo import MongoClient
from MongoBnB.models import Property


client = MongoClient("mongodb+srv://<user|pass>@cluster0.kp81sqx.mongodb.net/?retryWrites=true&w=majority")
db = client["sample_airbnb"]
# Create your views here.

def index(request):

    try:
        filter = request.GET['filter']

        if filter == 'under-100':
            data = db.listingsAndReviews.find({'$and':[{'cleaning_fee':{'$exists': True}},
                                                    {'price': {'$lt': 100}}]}, limit=15)
        elif filter == 'highly-rated':
            data = db.listingsAndReviews.find({'$and': [{'cleaning_fee': {'$exists': True}},
                                                    {'price': {'$lt': 100}},
                                                    {'review_scores.review_scores_rating': {'$gt': 90}}]},
                                                    limit=15)
        elif filter == 'surprise':
            data = db.listingsAndReviews.find({'cleaning_fee':{'$exists': True},'amenities':
                                                    {'$in': ["Pets allowed", "Patio or balcony", "Self check-in"]}},
                                                    limit=15)
    except KeyError:

        data = db.listingsAndReviews.find({'cleaning_fee': {'$exists': True}}, limit=15)
    response = []

    for doc in data:
        response.append(
            Property(
                doc['_id'],
                doc['name'],
                doc['summary'],
                doc['address']['street'],
                str(doc['price']),
                str(doc['cleaning_fee']),
                str(doc['accommodates']),
                doc['images']['picture_url'],
                doc['amenities']
            )
        )

    return render(request, 'MongoBnB/index.html', {'response': response})


def listing(request, id):
    doc = db.listingsAndReviews.find_one(
        {'_id': id}
    )

    response = Property(
        doc['_id'],
        doc['name'],
        doc['summary'],
        doc['address']['street'],
        str(doc['price']),
        str(doc['cleaning_fee']),
        str(doc['accommodates']),
        doc['images']['picture_url'],
        doc['amenities']
    )

    return render(request, 'MongoBnB/listing.html', {'property': response})

def confirmation(request, id):

    doc = db.bookings.insert_one({"property": id}).inserted_id

    return render(request, 'MongoBnB/confirmation.html', {'confirmation': doc, 'id': id} )
