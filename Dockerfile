FROM ckan/ckan

#upgrading base image to solve known issues with running CKAN with docker
#updates are done based on the following pull request:
#https://github.com/ckan/ckan/pull/5381/files

USER root
RUN ln -s $CKAN_VENV/bin/ckan /usr/local/bin/ckan
COPY ckan-entrypoint.sh /
CMD ["ckan","-c","etc/ckan/production.ini", "run", "--host", "0.0.0.0"]

#adding extension files to container
COPY . $CKAN_VENV/src/ckanext-tag_restriction/
#seting up the extension
RUN . $CKAN_VENV/bin/activate \
	&& cd $CKAN_VENV/src/ckanext-tag_restriction/ \
	&& python setup.py develop
