# read-it-later
A news aggregator and read-it-later web app built using flask and mysql.
The idea is inspired from this
[post](https://github.com/shekhargulati/52-technologies-in-2016/tree/master/16-newspaper)

## Directory Structure 
```
├── db
├── screenshots
├── static
│   ├── css
│   ├── fonts
│   ├── img
│   └── js
├── templates
│   └── includes
├── app.py
├── forms.py
├── LICENSE
├── posts.py
├── README.md
├── requirements.txt
└── utils.py

```

|folder|contents|
|-----|--------|
|db| queires, procedures and triggers|
|static| css, js, and other static files for the web app|
|screenshots| screenshots of various pages on the web app|
|templates| HTML templates used in the web app|

---
|script|contents|
|-----|--------|
|app.py| main server code with all the routes|
|forms.py| forms defined using WTForms|
|posts.py| article parsing code|
|utils.py| additional functions|

## Installation

`$ git clone git@github.com:kaushiksk/read-it-later.git && cd read-it-later`

`$ pip install -r requirements.txt`

Now run all the scripts in the `db/` folder.

Change the the `USERNAME`, `PASSWORD` variables in `app.py` to your mysql
username and password.

Start the server by running the following in your terminal: `$ python app.py`

## Development Notes

### DB Side
 - [x] MySQL procedure for validation of signup data
 - [x] Clearly define all tables, normalize, foreign keys etc.
 - [x] Procedure for entering new post/bookmark and performing all the checks
 - [x] Archive bookmark (Mark as read)
 - [x] Delete bookmark
 
### Backend 
 - [x] Setup flask server
 - [x] `USED WTFORMs`Check type of error and display it to user. Currently I am just posting a "Invalid
   Field" message. If usernames clash, display that as error message to user.
 - [x] Article parsing using newspaper
 - [x] Parse long text wrap at 150 characters but include last word.
 - [x] Multi line strings for queries using triple quotes

### Frontend
 - [x] Remove those random text boxes in index page. Add Bootstrap tiles or some
   boxes.
 - [x] Add SignIn page
 - [x] Revamp UI theme(FLAT-UI)
 - [x] Template for user and public dashboard
 - [x] Form for adding new bookmark
 - [x] Sidebar for choosing month, category
 - [x] Jquery-alert pugin for delete/archive confirmation
 - [x] Animate.css for fadeIn animations
 - [x] Font-Awesome icons
 - [x] Form for custom query in dashboard
 - [x] Archive Bookmark
 - [x] Delete Bookmark
 - [x] Add to my bookmarks in public dashboard
 - [x] Dynamically load content while retaining custom query form 
 - [x] Interactive charts with Chart.js

### Future
 - [ ] Tag Cloud. [JQCloud](http://primegap.net/2011/03/04/jqcloud-a-jquery-plugin-to-build-neat-word-clouds/)
