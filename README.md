# django_stackoverflow_clone
Stack Overflow is a question and answer website for hobbyists, amateur and professional programmers.This is a basic clone of stack overflow

[![CircleCI](https://circleci.com/gh/grey-felipe/django_stackoverflow_clone/tree/develop.svg?style=svg)](https://circleci.com/gh/grey-felipe/django_stackoverflow_clone/tree/develop) [![Test Coverage](https://api.codeclimate.com/v1/badges/cd494befcd13b1539e81/test_coverage)](https://codeclimate.com/github/grey-felipe/django_stackoverflow_clone/test_coverage)

## Swagger Docs
[Swagger](stackoverflow-clone-aeus.herokuapp.com/docs/)

## Endpoints

#### Registration
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/auth/signup/` - `POST`

***JSON***
```
{ 
	"user":{
		"username":"user",
		"email":"user@gmail.com",
		"bio":"I am a code fanatic",
		"image":"https//image.com",
		"password":"password123",
		"isAdmin":true,
		"badge":""
	}
}
```

#### Login
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/auth/login/` - `POST`

***JSON***
```
{
	"user":{
		"email":"user@gmail.com",
		"password":"password123"
	}
}
```

#### Create Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/add/` - `POST`

***JSON***
```
{
	"question":{
		"title":"this is a question",
		"body":"hey this really is a question",
		"is_open":true,
		"is_resolved":false,
		"is_closed":false,
		"tags":["java","spring"]
	}
}
```

#### Update Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/update/<int:id>/` - `PUT`

***JSON***
```
{
	"question":{
		"title":"This is an updated title",
		"body":"Behold the updated body of the question"
	}
}
```

#### Close Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/close/<int:id>/` - `PUT`

***JSON***
```
{
	"question":{
		"is_closed":true
	}
}
```

#### Add a comment to a Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/comments/add/<int:id>/` - `POST`

***JSON***
```
{
	"comment":{
		"comment":"this is a good question"
	}
}
```

#### Update a comment to a Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/comments/update/<int:id>/` - `PUT`

***JSON***
```
{
	"comment":{
		"comment":"this question is lit beyond comprehesion"
	}
}
```

#### Delete a comment to a Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/comments/delete/<int:id>/` - `DELETE`

#### Up vote a Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/upvote/<int:id>/` - `POST`

***JSON***
```
{
	"vote":{
		"up_vote":true,
		"down_vote":false
	}
}
```

#### Down vote a Question
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/downvote/<int:id>/` - `POST`

***JSON***
```
{
	"vote":{
		"up_vote":true,
		"down_vote":false
	}
}
```

#### Post Answer
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/answers/add/<int:id>/` - `POST`

***JSON***
```
{
	"answer":{
		"body":"The answer to this is fairly straight forward"
	}
}
```

#### Update Answer
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/answers/update/<int:id>/` - `PUT`

***JSON***
```
{
	"answer":{
		"body":"The answer to this is fairly straight forward"
	}
}
```

#### Add Comment to an Answer
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/comments/answers/add/<int:id>/` - `POST`

***JSON***
```
{
	"comment":{
		"comment":"this answer is lit"
	}
}
```

#### Update Comment an an Answer
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/comments/answers/add/<int:id>/` - `PUT`

***JSON***
```
{
	"comment":{
		"comment":"this answer is lit ain't it?"
	}
}
```

#### Up vote Answer
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/answers/upvote/<int:id>/` - `POST`

***JSON***
```
{
	"vote":{
		"up_vote":true,
		"down_vote":false
	}
}
```

#### Get user profile
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/auth/profile/` - `GET`

#### Get recommendations
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/recommendations/` - `GET`

#### Filter questions
***URL*** - `stackoverflow-clone-aeus.herokuapp.com/api/v1/questions/search?topic=value` - `GET`