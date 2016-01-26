# [SQLpie™](http://sqlpie.com)

## A sleek API platform for intelligence prototyping.
---

SQLpie™ is a simple, intuitive, and powerful API platform for prototyping projects that have data intelligence needs.

With SQLpie, you can store JSON objects in a SQL database and run a lot of information retrieval and machine learning tasks, covering areas such as: Text Classification, Text Summarization, Collaborative Filtering (item recommendation and similarity), Boolean/Vector Search, Document Matching, TagClouds, etc...

This project goes after a lot of big challenges, and although I do not advocate that it includes the best implementations to handle all of those tasks, I believe the combined effort can help people quickly prototype new ideas, and hopefully, new products. 

Bug reports, feature requests, and community contributions are welcome.

Stay tuned to <http://SQLpie.com> / [@SQLpie](https://twitter.com/SQLpie)


## Table of contents
---
* [About this Project](#about_this_project)
* [Getting Started](#getting_started)
* [SQLpie: Server, Client, and Shell](#server_client_shell)
* [Documentation and API Reference](#documentation)
* [Bugs, Feature Requests, and Contributing](#contributing)
* [Creator](#creator)
* [Trademarks](#trademarks)
* [Copyright and license](#copyright_and_license)

## [About this Project](id:about_this_project)
---

SQLpie is 100% written in Python and sits on top of a MySQL database.  It uses all sorts of SQL statements to creatively perform all kinds of computing tasks (thus, SQLpie). The codebase should be relatively easy to maintain (if necessary), and most (if not all) of the data processing heavy lifting is done in the database so scaling the database resources (in many cases)should help scale the software itself.


WHAT can this project really do for you?

* Store structured Documents and Observations in a relational database;
* Query the data using keywords, field, and boolean search operators;
* Transform Document contents and Observation relationships into interesting new findings by providing answers to the following type of questions:
  * What documents exist for query Q ?  (search)
  * What documents are located near location L ? (geosearch)
  * What top keyphrases and keywords relate to query Q? (tagcloud)
  * What are the key sentences and terms associated with document D? (summarization)
  * What documents are similar (or relate) to document D? (document matching)
  * Will user U like document D?  (classification)
  * How likely is user U to like document D?  (classification)
  * What documents is user U likely to love based on user data? (recommendation)
  * What other users have a document taste similar to user U? (similarity)


HOW can it help you?

* REST/JSON API;
* A cool and novel engine that stores and queries json objects in a structured database;
* Put/Get/Remove services for JSON Documents;
* Put/Get/Remove services for Observations (i.e. subjects-predicates-objects);
* Indexing and Search services;
* Geo Search and Tag Cloud services;
* Document Matching service;
* Classification service;
* Collaborative Filtering (recommendation and similarity) services;
* Text Summarization service;
* Caching Service;

WHY is this a good project?

* Comprehensive documentation;
* Good set of tests;
* Good framework for other similar projects to build upon;

And a few basic concepts to keep in mind:

* Documents are essentially any json objects you have (e.g. an employee, an article, etc.);
* Documents belong to Buckets (e.g. document M belongs to the employee Bucket.)
* Observations are associations between documents (e.g. employee M liked article Z);

And finally, two brief disclaimers: First, (a) in order to open source the code that was sitting idle for a while, some changes to the original design were made.  What that means is that the original performance and capacity metrics I had tested in the past will no longer apply, and new tests will eventually need to be put in place to account for those changes. Secondly, (b) having diverted a bit from my original codebase, it will likely take a few releases until any eventual new bugs are addressed, and performance/capacity improvements are made.


## [Getting Started](id:getting_started)
---

Once you install and start the SQLpie server, you can submit direct HTTP requests to its API, or you can use the included client Python library.

So, to get started, download the code, and install its requirements by running:

	$ pip install -r requirements.txt

Create an environment database: 

	$ python scripts/create_db.py

Start the server (see documentation to start the server on a different port):

	$ python application.py
	

Now just try the API, either by calling it directly:

	$ curl -i -H "Content-Type: application/json" -X POST -d '{"documents":[{"_id":"001", "text":"Hello World, Johnny Appleseed"}]}' http://localhost:5000/document/put

Or, by integrating the provided Python client file with your own code:

	import sqlpie_client
	sqlrc = sqlpie_client.SQLpieClient("http://localhost:5000")
	response = sqlrc.document_put({"documents":[{"_id":"001", "text":"Hello World, Johnny Appleseed"}]})

Note that the commands above will creaate a database in the development environment. In general, to create the database in a different environment, or to run the server in a different environment, use:

	$ sqlpie_env=production python scripts/create_db.py

## [SQLpie: Server, Client, and Shell](id:server_client_shell)
---

Besides the SQLpie Server that acts as a broker between your API Endpoints and the backend MySQL database, doing all the crazy stuff, this project also includes a pretty well documented Python client module you can import in your projects as briefly demonstrated above. 

Optionally, you can also play with the provided shell, which allows you to quickly interact with the API Endpoints. To get started on that, ensure the SQLpie Server is running, and execute the following command:

	$ python scripts/shell.py

This shell utility assumes you're running on the localhost and the port number is the one in the config file. Anything different than that you need to provide the proper API Server parameters. For example:

	$ python scripts/shell.py --hostname someotherdomain.net --port 3420


## [Documentation and API Reference](id:documentation)
---

This project is heavily documented.  The source of all API reference documentation are the Python docstrings in the `/sqlpie/clients/python/sqlpie_client.py` file, and a helper script, `scripts/update_docs.py`, was created and it's used to to generate updated doc files (stored in the `/docs/` directory) whenever the docstrings are updated.

To access the documentation, check the source files, or with the server running, go to:

	$ http://localhost:5000/docs

In addition to the `/docs/` material, the code in the `/tests/` directory is also a good reference in how to use the API. The `/examples/` directory is another place to look for how-to code references as well.

## [Bugs, Feature Requests, and Contributing](id:contributing)
---

Get involved!

If you come across any improvements, bugs or feature requests, please log your feedback on <https://github.com/lessaworld/sqlpie/issues>
 
If you want to dive into the project, the documentation and tests are the best place to start, of course. There's still a lot that can be done and/or documented... so keep an eye out for updates.

To run the test suite, just execute the following command:

	$ python scripts/run_tests.py

To contribute to this project using Github:

	1. Fork it
	2. Create your feature branch (git checkout -b my-new-feature)
	3. Commit your changes (git commit -am 'Add some feature')
	4. Push to the branch (git push origin my-new-feature)
	5. Create new Pull Request

By submitting a pull request or feature idea for this project, you agree to license 
 your contribution under the MIT license to this project.

And don't forget to stay tuned to <http://SQLpie.com> / [@SQLpie](https://twitter.com/SQLpie)


## [Creator](id:creator)
---
**Andre Lessa**

* <https://twitter.com/lessaworld>
* <https://github.com/lessaworld>

	I've been working with Python and SQL since the mid-to-late 90s.  In 2011, I started working on <strong>SQLpie</strong> when I had an idea to provide intelligence as a service. At that time, I conceptualized a simple API framework capable of managing information, and performing a lot of intelligent/information-retrieval/machine-learning tasks. With that idea in mind I spent a good part of that fall/winter and most of 2012 fully focused on the project. I pitched such API framework to a startup accelerator in the summer of '12 but didn't get in with that particular idea (I ended up getting in 6 months later with a more comprehensive, competitive intelligence, product in 2013, but that's another story). Fast forward to 2016, I am now open sourcing this codebase and sharing it with the world as I believe this framework has the potential to help others.


## [Trademarks](id:trademarks)

---
SQLpie™ is a trademark of André Lessa. 

The SQLpie logo is an original artwork created and trademarked by André Lessa.

The MIT license adopted by this project gives you the right to do just about anything with the code, but it doesn't relate or extend at all to the brand ("SQLpie", or the SQLpie logo). That way, the SQLpie creator, can ensure that other projects don't misrepresent the brand's identity and/or claim false brand endorsements or associations.

In other words, although you can use the SQLpie name and logo to refer to the brand, you can't use them in a way that's confusing as to whether there's an official sanctioning of a product you're offering. Unfortunately, the line between the two is often quite blurry and will be determined on a case-by-case basis. So, to be clear, if all you want is to use the source code, the MIT License below will suffice, but if you also want to use the SQLpie "brand" to commercially promote a product, you have to get permission first.


## [Copyright and License](id:copyright_and_license)

---
The SQLpie Source Code is published under the terms of the MIT License.   
  
SQLpie License (MIT License)

Copyright (c) 2011-2016 André Lessa, <http://sqlpie.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
