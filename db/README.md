# Setting up the database

This folder consists of all the sql commands, procedures and triggers that were used to create the database required for this app. 

For the ease of migration the mysqldump of the database at a particular state has been saved and made available here as the `project.gz` file. To automatically load the database from the mysqldump with some preloaded entries, run the following commands from your terminal.

`$ mysqladmin -p create project`

The shell should now prompt you for the password to your mysql root. Enter the poassword and run the following command.

`$ gunzip < project.gz | mysql -u [root-username] -p project` 
(replace [root-username] with your actual root username for MySQL).

All the tables and triggers should now be created under the database `project`.

This does not load the procedures required for the app to run.

Inside your mysql shell, run the following.

`mysql> source register.sql`

`mysql> source add_bm.sql`

`mysql> source add_post.sql`

`mysql> source delete_bm_trigger.sql`

If you instead wish to start with empty tables, run the following first

`mysql> source create_tables.sql`
