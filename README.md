# Recipes API for TK exercise
## Author
Chris Howell

## About

This API is a CRUD API for managing recipes. You can:
- Add Recipes
- Delete Recipes
- List Recipes
- Fetch a Recipe
- Search Recipes
- Add ingredients to a Recipe

## Setup

To clone the GIT repo
```sh
$ git clone https://github.com/clicktravel-chris/django-exercise.git
$ cd django-exercise
```

Then you can run the docker image:


```sh
$ docker-compose up
```

The available endpoints you can hit are the following:

- List recipes
    - **GET** /recipes/
- Filter recipes by name
    - **GET** /recipes/?name=`<query>`/
- Get a recipe by id
    - **GET** /recipes/`<id>`/
- Create a new recipe
    - **POST** /recipes/
- Update a recipe
    - **PATCH** /recipes/`<id>`/
- Delete a recipe
    - **DELETE** /recipes/`<id>`/

### Example: Create a new Recipe

POST /recipes/

Request body:

    {
        'name': 'Cheese on toast',
        'description': 'Simply put cheese on bread and toast it.',
        'ingredients': [
            {'name': 'Cheese'},
            {'name': 'Bread'},
        ]
    }


## Tests

To run the tests:
```sh
docker-compose run --rm app sh -c "python manage.py test"
```
