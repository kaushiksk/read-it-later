# read-it-later
A news aggregator and read-it-later web app built using flask and mysql

## TODO

### DB Side
 - [x] MySQL procedure for validation of signup data
 - [x] Clearly define all tables, normalize, foreign keys etc.
 - [x] Procedure for entering new post/bookmark and performing all the checks
 - [ ] `NEXT`Archive bookmark (Mark as read)
 - [ ] Delete bookmark
 
### Backend 
 - [x] `USED WTFORMs`Check type of error and display it to user. Currently I am just posting a "Invalid
   Field" message. If usernames clash, display that as error message to user.
 - [x] Article parsing using newspaper

### Frontend
 - [x] Remove those random text boxes in index page. Add Bootstrap tiles or some
   boxes.
 - [x] Add SignIn page
 - [x] Revamp UI theme(FLAT-UI)
 - [x] Template for user and public dashboard
 - [x] Form for adding new bookmark
 - [ ] Form for custom query in dashboard
 - [ ] Additional features: archive, delete, like

## Additional
 - Tag Cloud. [JQCloud](http://primegap.net/2011/03/04/jqcloud-a-jquery-plugin-to-build-neat-word-clouds/),[help](https://stackoverflow.com/questions/37259740/passing-variables-from-flask-to-javascript)
