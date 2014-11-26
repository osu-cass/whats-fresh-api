.. _usage:

Usage
=====

The What's Fresh API web app is used to enter the data that is displayed in the What's Fresh Mobile app. It consists of a series of simple forms for each type of object that can be added to the database. Required fields are marked with a *, and any errors or missing items will be flagged when the form is saved. The data will not be saved until errors are corrected.

Objects
-------

There are six major objects in What's Fresh: Vendors, Products, Preparations, Stories, Videos and Images. When you log in to the application, the first screen you see is the Entry screen, which lists the objects. Clicking on one of the object buttons will bring you to a screen listing all of the objects already saved in the system.

For example, clicking Vendors will display a table listing all the Vendors currently in the system. On this screen you can add a new Vendor by clicking the yellow "New Vendor" button at the top of the list, or edit any of the existing Vendors by clicking on that Vendor.


Adding and Editing
------------------

The forms for editing and for adding new objects are the same, except that the edit form will already be filled out with the existing data. You can edit this data and save the changes using the "Save" button at the bottom of the form, or delete the entire record using the red "Delete" button on the top of the form.

Workflow
++++++++

The objects in What's Fresh sometimes depend on other objects. For example, Vendors need Products, so you can't add a new Vendor without adding Products first. We recommend the following work flows to add different objects:

**Products**

1.	Determine what Preparations are available for this Product (smoked, dried, fresh, etc).
2.	Create the Preparation objects if they don't already exist.
3.	If there is an Image for this Product, create an Image object (be sure to give the image a unique and descriptive name).
4.	If this Product has a Story, make sure that Story exists (for instance, the Salmon story will probably be shared by all varieties of Salmon).
5.	Create the Product object, selecting the correct Story and Image, and add each applicable preparation.

**Vendors**

1.	Make sure this Vendor's Products are added (see above).
2.	If the Vendor has a Story (rare), create the Story object.
3.	Create the Vendor object, adding the correct Products and selecting a Story, if applicable.

**Stories**

1.	If this Story includes Images, create the Images.
2.	If this Story includes Videos, create the Videos.
3.	Create the Story object, adding the correct Images and Videos, if applicable.

See below for details on adding these objects.

Vendors
+++++++

These are the records for businesses that sell products. Vendors are also specific to a location, so if Bob's Fish has two different locations where they sell their Products, each location will be a separate Vendor. These can be distinguished by name, for instance Bob's Fish Newport and Bob's Fish Waldport.

The address for a Vendor should be the actual location where they sell their Products, not an office or P.O. box.

**Pre-requisites**

Vendors sell Products, so in order to create a new Vendor, some Products must exist (ideally, the specific Products that Vendor sells). Before creating a new Vendor, it is a good idea to make sure their Products exist. The Vendor form *requires* at least one Product to be added to the Vendor. A Vendor's Product list can be changed later.

**Required Data**

Certain information is required to create a new Vendor, make sure you know these items before starting:

*Name*
	The name of the business.
*Hours*
	The typical hours of operation.
*Description*
	A brief description of the business.
*Address*
	The street address where the products are being sold.
		* Street Address
		* City
		* State
		* Zipcode
*Contact Name*
	The primary contact name for this Vendor.
*Products*
	(At least one product should be added).

.. note::

	When a Product is added, you must also select a Preparation for that product. A vendor may sell different preparations for the same Product, or only one of many possible preparations for a Product. For example, a Vendor may sell smoked, frozen and fresh salmon, and also may sell shrimp, but only frozen, not fresh. Every Product/Preparation combination the vendor sells should be added.

.. note::
	
	Street addresses are turned into GPS coordinates for display on a map in the Mobile app, so it is important to be accurate.


**Optional Data**

Additionally, there are several optional fields:

*Story*
	Select from an existing Story (see the entry on Story objects below)
*In Port*
	The current status of the Vendor, if they sell from a boat, or only when the boat is in port. (Not used currently).
*Location Description*
	Additional details about how to find the Vendor location (The red boat at the end of Dock 3, for example).
*Website*
	The Vendor's website.
*Email*
	The Vendor's primary email address.
*Phone*
	The Vendor's phone number..


Preparations
++++++++++++

Preparations are the way in which a Product can be prepared for sale. This can include fresh, frozen, live, smoked, cooked, dried, and many more.

**Pre-requisites**

Preparations have no prerequisites.

**Required Data**

Preparations require the following fields to be filled out:

*Name*
	The name of this Preparation.

**Optional Data**

These fields are optional:

*Description*
	A more detailed description of the preparation. For instance 'Fermented' might require a little more explanation than 'Frozen'.
*Additional Information*
	Use this field to note additional things a user might need to know about buying Products with this Preparation. For example, fresh fish should be kept in a cooler for a long ride home.


Products
++++++++

Products are what Vendors sell, and the central Object in What's Fresh.

.. note::

	Different varieties of a particular product should be treated as separate products, if they are sold as such. For instance, different varieties of Salmon are sold with different prices, therefore Coho, Chinook and Sockeye salmon should be separate products. The 'Name' field of all these Products will be 'Salmon', and each will have a different value in the 'Variety' field.

**Pre-requisites**

Products require Preparations. Make sure all the possible preparations this Product can have are created first. If an Image or Story is going to be added, these objects should be created before adding the Product.

**Required Data**

Products require the following fields to be filled out:

*Name*
	The common name of this Product (i.e. Salmon).
*Description*
	A brief description of the product.
*Season*
	The typical season for this Product (ex. 'Sept. 20 - Dec 20', or 'Spring and Fall').
*Market Price*
	The current market price for this Product.
*Preparation*
	At least one preparation must be added.

**Optional Data**

These fields are optional:

*Variety*
	The variety of this product (ex. Coho, Sockeye, etc).
*Alternate Name*
	Other name(s) this product might be commonly called.
*Origin*
	The geographic origin of this Product.
*Available*
	Indicate if this product is currently being sold (ex. a fish is available even though its normal season is over).
*Link*
	A link to an official web site for this Product (ex. National Shrimp Council website).
*Image*
	A representative image of this Product.
*Story*
	The Story of this Product (see Stories below).


Stories
+++++++

Stories are collections of educational information about a Product or Vendor. Stories may be shared by many varieties of a particular Product - for instance the Salmon Story will likely apply to Coho, Chinook, and Sockeye salmon, which are all distinct Products.

**Pre-requisites**

If Images or Videos are going to be added to this Story, they should be created before the Story is created.

**Required Data**

Stories require the following fields to be filled out:

*Name*
	A name for this story. (This should be unique and easy to identify from the Story pull-down menu on the Product and Vendor forms.)

**Optional Data**

*Facts*
	A list of facts about the Product or Vendor.
*History*
	Text about the history and historical importance of the Product or Vendor.
*Buying*
	(Products only) What to know about buying this Product, (for example: how to select for freshness and quality).
*Preparing*
	(Products only) Ways to prepare this Product, recipes and other tips.
*Products*
	(Product only) Derivative Products made from this Product.
*Season*
	(Product only) Detailed information about the season for this Product.
*Images*
	One or more images related to this Product.
*Videos*
	One or more videos related to this Product.


Videos
++++++

Videos are external links to videos hosted on YouTube, Vimeo, or elsewhere. Any video that can be streamed can be used here.

**Pre-requisites**

Videos have no pre-requisites.

**Required Data**

Videos require the following fields to be filled out:

*Name*
	A name for this Video. (This should be unique and easy to identify from the Video pull-down menu on the Story form.)
*Link*
	The URL for this video (ex. https://www.youtube.com/watch?v=hl3wWwouOUE).
*Caption*
	A brief descriptive caption for this Video.

**Optional Data**

Videos have no optional fields.


Images
++++++

Images are uploaded image files. The Image upload form accepts .jpg, .png, and .gif image files. Images may be displayed as a single representative image for a Product in a Product view, or as part of a slideshow of images in a Story.

**Pre-requisites**

Images have no pre-requisites.

**Required Data**

Images require the following fields to be filled out:

*Image*
	Upload an image file.
*Name*
	A name for this Image. (This should be unique and easy to identify from the Image pull-down menu on the Story and Product forms.)
*Caption*
	A brief descriptive caption for this Image.

**Optional Data**

Images have no optional fields.