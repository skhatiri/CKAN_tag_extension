import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
from ckan.common import config
import requests 
from urllib import quote_plus
import logging

log = logging.getLogger(__name__)

#autocomplete api-endpoint
AUTOCOMPLETE_API = config.get('ckan.tag_restriction.autocomplete_api',
                               'https://terminologies.gfbio.org/api/terminologies/suggest?query={}&limit={}')

#search api-endpoint
SEARCH_API = config.get('ckan.tag_restriction.search_api',
                        'https://terminologies.gfbio.org/api/terminologies/search?query={}')

#minimum tag charachters for calling autocomplete api
AUTOCOMPLETE_MIN_CHARS = toolkit.asint(config.get('ckan.tag_restriction.autocomplete_min_chars',
                                   4))

#autocomplete results filed in api response
AUTOCOMPLETE_RESULT_FIELD = config.get('ckan.tag_restriction.autocomplete_results_field',
                                       'results')

#autocomplete tag label filed in api response
AUTOCOMPLETE_LABEL_FIELD = config.get('ckan.tag_restriction.autocomplete_label_field',
                                      'label')

#search results filed in api response
SEARCH_RESULT_FIELD = config.get('ckan.tag_restriction.search_results_field',
                                 'results')


class Tag_RestrictionPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)
    

    def get_validators(self):
        """adds the customized tag_name_validator to known validators"""
        log.info('Overriding default tag_name_validator')
        return {u'tag_name_validator':self.tag_name_validator}


    def get_actions(self):
        """adds the customized tag_autocomplete action to the action chain"""
        log.info('Overriding tag_autocomplte action')
        return {'tag_autocomplete':self.tag_autocomplete}


    @logic.side_effect_free
    @plugins.toolkit.chained_action    
    def tag_autocomplete(self, original_action, context, data_dict):
        """customized tag_autocomplete action, overrides default action"""
        logic.check_access('tag_autocomplete', context, data_dict)
        return self.autocomplete_from_API(data_dict['q'],data_dict['limit'])

    def tag_name_validator(self,value,context):
        """customized tag_name_validator, overrides default validator"""
        
        #calling default validator
        value = logic.validators.tag_name_validator(value,context)

        try:
            if not self.is_in_tag_API(value):
                raise toolkit.Invalid('\"{}\" is not in valid tags resource'.format(value))
        except:
            raise toolkit.Invalid('error while checking tag validity, contact website administrator')
        return value

        
    def autocomplete_from_API(self, tag, limit):
        """returns suggestions from provided api for tags"""
        
        if len(tag) < AUTOCOMPLETE_MIN_CHARS:
            return []

        encoded_url = AUTOCOMPLETE_API.format(quote_plus(tag), limit)
        try:
            r = requests.get(encoded_url)
            response = r.json()
            if response[AUTOCOMPLETE_RESULT_FIELD]:
                return [result[AUTOCOMPLETE_LABEL_FIELD] for result in response[AUTOCOMPLETE_RESULT_FIELD] ]
        except requests.exceptions.RequestException as e:
            log.error('exception when calling tag autocomplete api')
            log.error(e)
            return ['sugestions not available']
        return []

    
    def is_in_tag_API(self, tag):
        """checks whether the tag exists provided api terminologies"""

        encoded_url = SEARCH_API.format(quote_plus(tag))
        try:
            r = requests.get(encoded_url)
            response = r.json()
            if response[SEARCH_RESULT_FIELD] and len(response[SEARCH_RESULT_FIELD]) > 0 :
                return True
            return False
        except requests.exception.requestException as e:
            log.error('exception when calling tag search api')
            log.error(e)
            raise e

