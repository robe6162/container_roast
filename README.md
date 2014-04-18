ContainersRoast
================================
<pre>
 (----) (----)--)
  (--(----)  (----) --)
(----) (--(----) (----)
-----------------------
\                     /
 \                   /
  \_________________/
     )\ `   `(` `
     ( ) ` )' )  \_
    (   )  _)  \   )
  ) )   (_  )   ,  (
  (  ,  )   (   (
    (  (    )    )
  === ContainersRoast ===
= A CloudCAFE Test Repository =
</pre>

ContainersRoast is a rich, full bodied blend of premium roasted automated test cases. ContainersRoast tests are based on the expanded unittest driver in the
[Open CAFE Core](https://github.com/stackforge) and built using the [CloudCAFE Framework](https://github.com/stackforge) and the ContainersCAFE Framework.

ContainersRoast tests support smoke, functional, integration, scenario and reliability based test cases for ContainersCAFE. It is meant to be highly flexible
and leave the logic of the testing in the hands of the test case developer while leaving the interactions with OpenStack, various resources and
support infrastructure to CloudCAFE.

Installation
------------
ContainersRoast can be [installed with pip](https://pypi.python.org/pypi/pip) from the git repository after it is cloned to a local machine.

* First follow the README instructions to install the [CloudCAFE Framework](https://github.com/stackforge)
* Clone this repository to your local machine
* CD to the root directory in your cloned repository.
* Run "[sudo] pip install . --upgrade" and pip will auto install all other dependencies.

Configuration
--------------
ContainersRoast runs on the [CloudCAFE Framework](https://github.com/stackforge) using the cafe-runner. It relies on the configurations installed to:
<USER_HOME>/.opencafe/configs/<PRODUCT> by CloudCAFE.

At this stage you will have the Open CAFE Core engine, the CloudCAFE Framework implementation and the Open Source automated test cases. You are now
ready to:
1) Execute the test cases against a deployed Open Stack.
                       or
2) Write entirely new tests in this repository using the CloudCAFE Framework.

Logging
-------
If tests are executed with the built-in cafe-runner, runtime logs will be output to
<USER_HOME>/.opencafe/logs/<PRODUCT>/<CONFIGURATION>/<TIME_STAMP>.

In addition, tests built from the built-in CAFE unittest driver will generate
csv statistics files in <USER_HOME>/.opencafe/logs/<PRODUCT>/<CONFIGURATION>/statistics for each and ever execution of each and every test case that
provides metrics of execution over time for elapsed time, pass/fail rates, etc...

Basic ContainersRoast Package Anatomy
-------------------------------
Below is a short description of the top level ContainersRoast Packages.

##containersroast
This is the root package for all automated tests. This is namespace is currently **required** by the cafe-runner for any Test Repository plug-in.

