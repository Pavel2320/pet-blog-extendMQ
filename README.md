# Pet Blog

Pet blog is a typical test project.

1. Each user has his own blog, but he cannot create a new one.
2. The user can subscribe (unsubscribe) to blogs of other users.
3. The user has his news feed with posts of other users.
4. The user can mark posts in the feed as read.
5. When a new post is added, each user subscribed to the author receives an email.

## For manual testing

There are four users in the database with the names User1, User2, User3, User4 with passwords "pass".

### clone

`git clone git@github.com:theshortman/pet-blog.git && cd pet-blog`

### make file .env.dev and add some options

`touch .env.dev`<br />
`echo "DEBUG=1" > .env.dev`<br />
`echo "SECRET_KEY=secret_key" >> .env.dev`<br />
`echo "ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0" >> .env.dev`

### build and up

`docker-compose up --build`
