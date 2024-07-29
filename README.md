# Blog API

## Endpoints

#### User Related

- `/api/user/register [POST]` : Register a new User
- `/api/user/login [POST]` : Gets Access & Refresh JWT tokens for the user.
- `/api/user/is-logged-in [GET]` : Check if the user is authenticated or not.

#### Post Related

- `/api/posts [GET]` : Lists all available posts, Supports filters : `author`, `published_on`, `search`
- `/api/posts/create/ [POST]` : Creates a new post 
- `/api/posts/<slug>/ [GET]` : Get individual post
- `/api/posts/<slug>/edit/ [PATCH]` : Edits a post
- `/api/posts/<slug>/delete/ [DELETE]` : Deletes a post