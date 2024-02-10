# Project 1

ENGO 551
This is the ENGO551 Lab1 Book search and review website created by Chunsheng Xiao.

The first page of the website is a sign-in/register page. You can sign in or register if you don't have an account.

By clicking on the register link, you will get to the register page. Here you can write down your user id and password. These information are stored in the users table in postgres local database. If you try to register with a existing account, it will tell you to register again. Otherwise, the system will tells you your account is registered.

Once you are signed in, you will get to the main page for searching. You can search on ISBN, title, or author's name here. The query enables similar matching. For example, if you search "The Dark is" in title, the engine will give you the book named "The Dark is Rising".

From the link of the books, you can get to the detail page of the book. The ISBN, title, author, and the publish date are shown here. On the left upper corner is the sign out button. On the right upper corner is the back to Searching page option.