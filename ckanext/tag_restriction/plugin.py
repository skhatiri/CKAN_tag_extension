import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import requests 
from urllib import quote_plus
import logging


log = logging.getLogger(__name__)

#autocomplete api-endpoint 
AUTOCOMPLETE_API = "https://terminologies.gfbio.org/api/terminologies/suggest?query={}&limit={}"

#minimum tag charachters for calling autocomplete api
AUTOCOMPLETE_MIN_CHARS = 4

class Tag_RestrictionPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IValidators)
    

    def get_validators(self):
        """adds the customized tag_name_validator to known validators"""
        log.info("Overriding default tag_name_validator")
        return {u'tag_name_validator':self.tag_name_validator}


    def get_actions(self):
        """adds the customized tag_autocomplete action to the action chain"""
        log.info("Overriding tag_autocomplte action")
        return {"tag_autocomplete":self.tag_autocomplete}


    @logic.side_effect_free
    @plugins.toolkit.chained_action    
    def tag_autocomplete(self, original_action, context, data_dict):
        """customized tag_autocomplete action, overrides default action"""
        logic.check_access('tag_autocomplete', context, data_dict)
        return self.autocomplete_from_GFBio(data_dict['q'],data_dict['limit'])

    def tag_name_validator(self,value,context):
        raise toolkit.Invalid("tag not in GFBio")
        

    def autocomplete_from_GFBio(self, tag, limit):
        """returns suggestions from GFBio terminologies for tags"""
        
        if len(tag)<AUTOCOMPLETE_MIN_CHARS:
            return []

        encoded_url = AUTOCOMPLETE_API.format(quote_plus(tag), limit)
        r = requests.get(encoded_url)
        response = r.json()
        if response['results']:
            return [result['label'] for result in response['results'] ]
        return []

