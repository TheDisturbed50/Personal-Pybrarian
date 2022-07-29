# Personal Pybrarian
 
Inspired by my wife, who has a few books.

The goal was simple, make an easy-to-use CRUD program to store book data as a user adds the primary reference.
Well, then my wife started using an online database where she could scan her ISBN barcode and it would add them... How dare she!

So I want to make this experience better.

What I have so far:
Interface: CLI-only.
Primary References: ISBN number only.
Working Google Books API call and JSON parse.
SQLite3 DB, with Add, Edit, and Remove functions in place to manage data.
Export to CSV feature, with tk.messagebox directory selector (maybe a problem for a headless operation)
Bulk-importing works if you paste from an excel file.

See the Issues section for future plans under "Enhancement" tags.
More distant future plans: Implement a review system for the saved books.

License: GPL 3

Contributions: Teamwork makes the dream work. I'm not a seasoned coder, so I'm open to anyone's constructive input. 

Have ideas for this? Submit a new issue for it!
