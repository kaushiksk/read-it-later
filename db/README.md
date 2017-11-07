# Setting up the database

This folder consists of all the sql commands, procedures and triggers that were used to create the database required for this app. 

`$ mysql -u user -p create project`

The shell should now prompt you for the password to your mysql root. Enter the poassword and run the following command.

Inside your mysql shell, run the following.

`mysql> source create_tables.sql`

`mysql> source register.sql`

`mysql> source add_bm.sql`

`mysql> source add_post.sql`

`mysql> source delete_bm_trigger.sql`
