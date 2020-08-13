import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic


class Tag_RestrictionPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    

    def get_actions(self):
        """adds the customized tag_autocomplete action to the action chain"""
        print("seting up action")
        return {"tag_autocomplete":self.tag_autocomplete}


    @logic.side_effect_free
    @plugins.toolkit.chained_action    
    def tag_autocomplete(self, original_action, context, data_dict):
        """customized tag_autocomplete action, overrides default action"""
        logic.check_access('tag_autocomplete', context, data_dict)
        return self.autocomplete_from_GFBio(data_dict)


    def autocomplete_from_GFBio(self, tag):
        """returns suggestions from GFBio terminologies for tags"""
        return ["test1","test2"]
