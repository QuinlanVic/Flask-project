
1. Create Database
use db (if not created, it will create one)
show dbs (shows you which db you are wrking with)
Practical example:
use bs3awe (switches to a particular database)
show collections (shows "tables" in db)
use quinlansanlam (switches to a particular database)

add a bunch of movies = INSERT INTO MOVIES VALUES ("Vikram", "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg", 8.4, "Members of a black ops team must track and eliminate a gang of masked murderers.")
2. Create collection (table with rows)
```js
db.movies.insertMany(data, options)
db.movies.insertMany([
  {
    "name": "Vikram",
    "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
    "rating": 8.4,
    "summary": "Members of a black ops team must track and eliminate a gang of masked murderers."
  },
  {
    "name": "RRR",
    "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
    "rating": 8.8,
    "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments."
  },
  {
    "name": "Iron man 2",
    "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
    "rating": 7,
    "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy."
  },
  {
    "name": "No Country for Old Men",
    "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
    "rating": 8.1,
    "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money."
  },
  {
    "name": "Jai Bhim",
    "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
    "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
    "rating": 8.8
  },
  {
    "name": "The Avengers",
    "rating": 8,
    "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
    "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg"
  },
  {
    "name": "Interstellar",
    "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
    "rating": 8.6,
    "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans."
  },
  {
    "name": "Baahubali",
    "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
    "rating": 8,
    "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy."
  },
  {
    "name": "Ratatouille",
    "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
    "rating": 8,
    "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him."
  },
  {
    "name": "PS2",
    "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
    "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
    "rating": 8
  },
  {
    "name": "Thor: Ragnarok",
    "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
    "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
    "rating": 8.8
  }
]
)
```
3. Read the data
Find all movies = SELECT * FROM MOVIES
```js
db.movies.find()
```

4. Filter the data
find movies with id = 100 = SELECT * FROM MOVIES WHERE id = 100
```js
db.collection.find({
  "id": "100"
})
```
### Comparison operators
5. Movings with rating of 8
find movies with rating = 8 = SELECT * FROM MOVIES WHERE rating = 8
```js
db.collection.find({
  rating: 
    8
})
```
5.1 Negative of above 
```js
db.collection.find({
  rating: {
    $ne: 8
  }
})
```

### ALL OPERATORS START WITH A "$"

6. Find movies with rating greater than 8
```js
db.collection.find({
  rating: {
    $gt: 8
  }
})
```

7. Find movies with rating less than 8
```js
db.collection.find({
  rating: {
    $lt: 8
  }
})
```

8. Find movies with rating greater than or equal to 8
```js
db.collection.find({
  rating: {
    $gte: 8
  }
})
```

9. Find movies with rating less than or equal to 8
```js
db.collection.find({
  rating: {
    $lte: 8
  }
})
```

10. All movies with the rating of 8.4, 7, 8.1 = SELECT * FROM MOVIES WHERE rating in (8.4, 7, 8.1)
```js
db.collection.find({
  "$or": [
    {
      rating: 8.4
    },
    {
      rating: 7
    },
    {
      rating: 8.1
    }
  ]
})
```
OR

```js
db.collection.find({
  "rating": {
    $in: [
      8.1,
      7,
      8.4
    ]
  }
})
```
10.1 NEGATIVE OF ABOVE
```js
db.collection.find({
  "rating": {
    $nin: [
      8.1,
      7,
      8.4
    ]
  }
})
```

### Projections
SELECT name, rating FROM movie 
INCLUSION = 1
```js
db.movie.find({}, {name: 1, rating: 1})
```

SELECT * EXCEPT(summary, trailer) FROM Movie
EXCLUSION = 0
```js
db.movie.find({}, {summary: 0, trailer: 0})
```

SELECT name, rating FROM movie WHERE rating > 8.5 =
Movies with a rating greater than 5, only name and rating column (also exclude default _idx)
```js
db.movie.find({rating: {$gt: 8.5}}, {_id: 0, name: 1, rating: 1})
```

### Sorting
Ascending sort
```js
db.movie.find({}).sort({rating: 1})
```

Descending sort
```js
db.movie.find({}).sort({rating: -1})
```

Projection and sort desc rating
```js
db.movie.find({}, {_id: 0, name: 1, rating: 1}).sort({rating: -1})
```

Projection and sorting by 2 things (Compound sorting)
```js
db.movie.find({}, {_id: 0, name: 1, rating: 1}).sort({rating: -1, name: -1})
```

### Top 3 - Limit
```js
db.movie.find({}, {_id: 0, name: 1, rating: 1}).sort({rating: -1, name: -1}).limit(3)
```

### Skip - Skip (Equivalent to offset in SQL)
4, 5, 6
```js
db.movie.find({}, {_id: 0, name: 1, rating: 1}).sort({rating: -1, name: -1}).limit(3).skip(3)
```
# Steps to use
use quinsanlam (DATABASE)
## Now to create a collection with documents do below
```js
db.orders.insertMany(
[
{ _id: 0, productName: "Steel beam", status: "new", quantity: 10 },
{ _id: 1, productName: "Steel beam", status: "urgent", quantity: 20 },
{ _id: 2, productName: "Steel beam", status: "urgent", quantity: 30 },
{ _id: 3, productName: "Iron rod", status: "new", quantity: 15 },
{ _id: 4, productName: "Iron rod", status: "urgent", quantity: 50 },
{ _id: 5, productName: "Iron rod", status: "urgent", quantity: 10 }
]
)
```
#### Get product names and the total quanity that must be shipped urgently
#### Example output = [{ _id: "Steel Beam", totalQuantity: 50}, { _id: "Iron rod", totalQuantity: 60}]
SELECT productName as _id, SUM(quantity) AS totalQuantity FROM orders WHERE status = "urgent" GROUP BY productName

### Aggregate functions
```js
// multiple stages in the aggregate function
db.orders.aggregate([
  // stage 1 = only get docs that are urgent
  { $match: { status: "urgent"} }, 
  // stage 2
  { 
    $group: { _id: "$productName", totalUrgentQuantity: { $sum: "$quantity"}} 
    // group by productname but save the column name as "_id" and get total quantity but save the column name as "quanitity'" (have to use dollar signs before column names to access values inside of the columns)
  }
  // stage 3
])
```

-- Sub-Query
-- 1. Write a query to display all the orders from the orders table issued by the salesman 'Paul Adam'.
```js
SELECT * FROM salesorders WHERE salesorders.salesman_id = (SELECT salesman_id FROM salesman WHERE salesman.name = 'Paul Adam')
```

-- 2. Write a query to display all the orders which values are greater than the average order value for 10th October 2012.
```js
SELECT * FROM salesorders WHERE purch_amt > (SELECT AVG(purch_amt) FROM salesorders WHERE ord_date = '2012-10-10') 
```