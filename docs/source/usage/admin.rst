.. _admin:

Admin
=====

Adding New Users
----------------

Adding a new user is simple. First, log into /admin. Under Authentication and
Authorization there is Groups and Users. To the right of these are two buttons
that say Add and Change. Click on Add. Enter the user's username and password.
Click save in the bottom right hand corner. You will be taken to a Change User
page. Here you can edit the user's information. They have already been added to
the Data Entry Users group. This is to prevent an infinite loop when they log
in. Once you are done, click save at the bottom of the page. Congratulations,
you've just added a user!


Adding New Themes
-----------------

Adding a new theme is simple. First, log into /admin. Below Authentication and
Authorization there is Themes. To the right of these are two buttons
that say Add and Change. Click on Add. Enter the your theming preferences.
Click save in the bottom right hand corner. You will be taken to a Change User
page. Here you can edit your theme preferences. Once you are done, click save
at the bottom of the page. Congratulations, you've just added a new theme!


Themes
++++++

Themes are a set settings defined for User Interface preferences of the site. A variety of options are available to choose from such as changing the background color, site title, form labels etc..

.. warning::

	When a Theme is added, it will not be activated until the active field is set to Yes. Keep in mind that if you change the slug fields to something other than the default value you'll need to restart the server to see the corrsponding changes in URL bar to take place because URL's are loaded only on server load.

.. note::

	For activating a particular theme you need to set the Active field as Yes, only one theme can stay active at a time as a result only one of the themes will have this field set as Yes.

**Required Data**

Themes require the following fields to be filled out:

*Name*
	The name of this Theme.

**Optional Data**

These fields are optional:

*Background Color*
	The background color you want for the site (default is ``rgb(81, 114, 133)``).
*Foreground Color*
	The foreground color you want for the site (default is ``rgb(81, 114, 133)``).
*Header Color*
	The header color you want for the site (default is ``rgb(255, 255, 255)``).
*Font Color*
	The font color you want for the site (default is ``rgb(51, 51, 51)``).
*Logo*
	The logo you want for the site.
*slogan*
	The slogan for the site.
*Site Title*
	The title for the site (default is Oregon's Catch).
*vendors*
	The Vendors form label, you can change this to whatever you want (default is Vendors).
*vendors slug*
	The endpoint for vendors, ideally this should has the same value as vendors (default is vendors).
*products*
	The Products form label, you can change this to whatever you want (default is Products).
*products slug*
	The endpoint for products, ideally this should has the same value as products (default is products).
*preparations*
	The Preparations form label, you can change this to whatever you want (default is Vendors).
*preparations slug*
	The endpoint for preparations, ideally this should has the same value as preparations (default is preparations).
*stories*
	The Stories form label, you can change this to whatever you want (default is Stories).
*stories slug*
	The endpoint for stories, ideally this should has the same value as stories (default is stories).
*images*
	The Image form label, you can change this to whatever you want (default is Images).
*images slug*
	The endpoint for images, ideally this should has the same value as images (default is images).
*videos*
	The Videos form label, you can change this to whatever you want (default is Vidoes)
*vidoes slug*
	The endpoint for videos, ideally this should has the same value as videos (default is videos).
*active*
	This should be "Yes" for a particular theme to be activated (default is "No").
