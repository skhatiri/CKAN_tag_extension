# CKAN extension for tag restriction

A simple extension for [CKAN](https://ckan.org/)  to restrict dataset tags to be obtained from a source API

Overrides default tag autocomplete and validation behaviours of CKAN, making it mandatory for tags to be selected from a specific source.

the tag source is assumed to be available with public GET apis

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

1. This extension uses public GET APIs for tag autocomplete and search.

check [``tag_restriction.ini``](tag_restriction.ini) for details on their prerequisites

2. You should have Docker or a CKAN instance installed before using this extension

### Installing

1. Clone the repository
```
$ git clone https://github.com/skhatiri/CKAN_tag_extension.git
```

2. Edit tag_restriction configs from ``tag_restriction.ini``.

Provide your own apis for tag autocomplete and search (the default config uses [GFBio Terminology APIs](https://terminologies.gfbio.org/api/))

#### On Docker

3. Copy [``.env.template``](.env.template) to a new ``.env`` file and edit configurations if needed

4. Go to the root folder of the project and run it using ``docker-compose``
```
$ docker-compose up --build -d
```

5. Go to http://localhost:5000 

#### On your own CKAN instalation:

3. copy tag_restriction configs from [``tag_restriction.ini``](tag_restriction.ini) to the ``[app:main]`` section of the CKAN config file

4. Add ``"tag_restriction"`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/ckan.ini``).

5. Go to project's root, Activate your CKAN virtual environment, and run ``setup.py develop``
```
$ . /usr/lib/ckan/default/bin/activate
$ python setup.py develop    
```

6. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

```
$ sudo service apache2 reload
```

## Authors

* **Sajad Khatiri** - [s.khatiri](https://github.com/skhatiri)


## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details

