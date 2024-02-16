# Cyber security base project 1

This is a simple web application with 5 common security flaws.

## Installation

Clone the repository and go to /blogapp. Then run

```
python manage.py loaddata data.json
```

to initialize the database. Start the application with

```
python manage.py runserver
```

### Credentials

The application has the following username-password pairs for testing:

* bloglover00: bloglover123
* Maija Meikäläinen: Maija123
* admin: Admin123

## Security vulnerabilities

### FLAW 1: INJECTION

[Link to flaw 1](https://github.com/EeviLuukkonen/cyber-security-project1/blob/99912fcd8b924f918474053c59db99bb7cfa69c9/blogapp/blogs/views.py#L26)

This code uses an SQL query for saving user input data to database. Concatenating user inputs without checking if it’s malicious makes the form vulnerable for SQL injection, that can lead to e.a. data loss in the database.

Here is an example on how to fix the code:

```
new_blog = Blog(name=name, author=author, year=timezone.now(), url=url, user=request.user)
new_blog.save()
```

This fixed code uses Django's ORM (Object-Relational Mapping) instead of direct SQL. It creates a new Blog instance with the user inputs and saves it to the database. This approach treats user input as data rather than executable code, which mitigates the risk of SQL injection. ORM uses a higher level of abstraction for interacting with the database. There are many other ways to fix this problem as well, like parameterzied queries and Djangos built-in forms.


### FLAW 2: SECURITY MISCONFIGURATION

[Link to flaw 2](https://github.com/EeviLuukkonen/cyber-security-project1/blob/99912fcd8b924f918474053c59db99bb7cfa69c9/blogapp/mysite/settings.py#L26)

In Django, there is a feature called debug mode. When enabled, it provides precise and sensitive information to the user if an error occurs. It is valuable while in development but dangerous when in production. Having debug mode on can lead to sensitive information leaking, for example in the form of error messages. It can also give an attacker details of how the page is constructed and thus make it easier to attack.

To fix the vulnerability, when in production, the debug mode should always be set as false in settings.py.


### FLAW 3: CSRF

[Link to flaw 3](https://github.com/EeviLuukkonen/cyber-security-project1/blob/2b1f1af3f72e7f6ac9ce55ab129200ada16d7b93/blogapp/blogs/views.py#L19)

Cross-Site Request Forgery is a security flaw that can lead to a user unknowingly sending requests to other web applications. User can e.g. make unwanted financial transactions or send their private information to an attacker.

Django automatically prevents CSRF from happening. It checks that all form submissions come from the same site that rendered the form. The programmer only has to make sure that a form has CSRF-token present.

That is why this flaw is implemented by adding @csrf_exempt to create_blog. This disables the automatic protection, making blog creation vulnerable for CSRF attack. To fix this flaw, remove the @csrf_exempt and use token in the form. This could also be achieved by manually checking that the user token and form token match, but Django's automation makes the fix easy.


### FLAW 4: BROKEN ACCESS CONTROL
[Link to flaw 4](https://github.com/EeviLuukkonen/cyber-security-project1/blob/99912fcd8b924f918474053c59db99bb7cfa69c9/blogapp/blogs/views.py#L45)

Access control are rules for preventing users from doing what they are not supposed to do. In this app, when deleting a blog, the code does not make sure that the user is an admin user, even though the frontend only allows admin users to see the delete blog button. This leads to a broken access control flaw. A malicious user could easily delete blogs even though they are not an admin.

To fix the problem, the deletion should be implemented the same way as comment deletion is. Not only the frontend template code, but also backend code should make sure that the current user has admin rights. In django this can be done inside the “if request.user.is_superuser” -block.

### FLAW 5: CROSS SITE SCRIPTING

[Link to flaw 5](https://github.com/EeviLuukkonen/cyber-security-project1/blob/99912fcd8b924f918474053c59db99bb7cfa69c9/blogapp/blogs/templates/blogs/detail.html#L15)

Django templates automatically prevent XSS attacks. However, to demonstrate how a XSS attack happens I have used the command |save in the template. This allows the raw HTML content to be included on the page and allows scripts also. With this flaw, if a user writes for example 

```
<script>alert("XSS Attack!");</script>
```
as a comment, the XSS attack happens.
Fixing this issue in Django is easy, as it automatically validates and sanitizes the user inputs. By removing the |save command, the XSS attack does not happen and scripts are drawn on the page as normal HTML.

