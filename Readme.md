# Paint batch optimizer service

## Purpose

This service provides solutions for the following problem.

Our users own paint factories. There are N different colors they can mix, and each color can be prepared "matte" or "glossy". So, you can make 2N different types of paint.

Each of their customers has a set of paint types they like, and customers will be satisfied if you have at least one of those types prepared. At most one of the types a customer likes will be a "matte".

Our user wants to make N batches of paint, so that:

There is exactly one batch for each color of paint, and it is either matte or glossy. For each customer, user makes at least one paint that they like. The minimum possible number of batches are matte (since matte is more expensive to make). This service finds whether it is possible to satisfy all customers given these constraints, and if it is, what paint types you should make. If it is possible to satisfy all your customers, there will be only one answer which minimizes the number of matte batches.

Input

Integer N, the number of paint colors,  integer M, the number of customers. A list of M lists, one for each customer, each containing: An integer T >= 1, the number of paint types the customer likes, followed by T pairs of integers "X Y", one for each type the customer likes, where X is the paint color between 1 and N inclusive, and Y is either 0 to indicate glossy, or 1 to indicated matte. Note that: No pair will occur more than once for a single customer. Each customer will have at least one color that they like (T >= 1). Each customer will like at most one matte color. (At most one pair for each customer has Y = 1). 

Output

The string "IMPOSSIBLE", if the customers' preferences cannot be satisfied; OR N space-separated integers, one for each color from 1 to N, which are 0 if the corresponding paint should be prepared glossy, and 1 if it should be matte.

## Production Deployment

Follow the steps below to boot service within a container. 

1. python manage.py makemigrations app
2. python manage.py migrate
3. python manage.py createsuperuser <follow steps to create your own admin user (admin.user) and whatever password you want>
4. python manage.py runserver 0.0.0.0:8000

## Swagger

Swagger has been included to allow for easy querying of the new service and maintaing strong documentation standards for API users

Example URL:

```
http://0.0.0.0:8000/docs/#/
```

![Screenshot](docs/swagger.PNG)

## User Authentication

To use the service you must be authenticated with the appropriate permissions.

### Create user

python manage.py createsuperuser --username aylien --email test@aylien.com

### Generate token

```
python manage.py drf_create_token aylien
```

Output:
```
Generated token 5d9aceeb46cf0245ddc10c16490b59ccb30b4359 for user aylien
```
### Request token 

```
http post http://0.0.0.0:8000/api-token-auth/ username=aylien password=Password12345
```
Output

```
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 52
Content-Type: application/json
Date: Mon, 14 Jan 2019 17:48:51 GMT
Server: WSGIServer/0.2 CPython/3.6.7
X-Frame-Options: SAMEORIGIN

{
    "token": "7222edb57cbf7557b8424b99b49809f58cf35ba0"
}
```

## Usage

The application has a primary endpoint at `/solve/`. When you make calls to this endpoint, you can send a JSON string as the argument "input". The JSON string contains three keys: colors, costumers and demands.


Examples:

```
http 'http://0.0.0.0:8000/solve/?input={%22colors%22:1,%22customers%22:2,%22demands%22:[[1,1,1],[1,1,0]]}' 'Authorization: Token 5d9aceeb46cf0245ddc10c16490b59ccb30b4359'

IMPOSSIBLE
```
```
http 'http://0.0.0.0:8000/solve/?input={%22colors%22:5,%22customers%22:3,%22demands%22:[[1,1,1],[2,1,0,2,0],[1,5,0]]} ' 'Authorization: Token 5d9aceeb46cf0245ddc10c16490b59ccb30b4359'

1 0 0 0 0
```
**Note:** If you have the incorrect token expect to see the following error:
```

HTTP/1.1 401 Unauthorized
Allow: GET, OPTIONS
Content-Length: 58
Content-Type: application/json
Date: Mon, 14 Jan 2019 17:55:57 GMT
Server: WSGIServer/0.2 CPython/3.6.7
Vary: Accept
WWW-Authenticate: Token
X-Frame-Options: SAMEORIGIN

{
    "detail": "Authentication credentials were not provided."
}
```

**OR**

```
HTTP/1.1 401 Unauthorized
Allow: GET, OPTIONS
Content-Length: 27
Content-Type: application/json
Date: Mon, 14 Jan 2019 17:55:47 GMT
Server: WSGIServer/0.2 CPython/3.6.7
Vary: Accept
WWW-Authenticate: Token
X-Frame-Options: SAMEORIGIN

{
    "detail": "Invalid token."
}
```

This can be resolved by identifying the token through the endpoint provided above (see "Request token" section).

## Limitations

None of our users produce more than 2000 different colors, or have more than 2000 customers. (1 <= N <= 2000 1 <= M <= 2000)
The sum of all the T values for the customers in a request will not exceed 3000.

