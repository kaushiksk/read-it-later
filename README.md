# read-it-later
A news aggregator and read-it-later web app built using flask and mysql.
The idea is inspired from this
[post](https://github.com/shekhargulati/52-technologies-in-2016/tree/master/16-newspaper)

*This web app is live at: http://ec2-18-221-93-178.us-east-2.compute.amazonaws.com*

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

newspaper requires nltk==2.0.5. See [here](https://stackoverflow.com/questions/46977498/urllib2-httperror-http-error-403-ssl-is-required-when-installing-nltk-2-0-5) for instructions on how to install. 
Make sure you have mysql, [mysql-dev](https://stackoverflow.com/questions/14604228/mysql-h-file-cant-be-found#14604638), [libxmldev](https://stackoverflow.com/questions/15759150/src-lxml-etree-defs-h931-fatal-error-libxml-xmlversion-h-no-such-file-or-di#15761014) installed. 
`$ pip install -r requirements.txt --user`

Note that you will need to have gcc installed.

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
