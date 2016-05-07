from collections import Counter
from inventory.models import Object


class CloudFactory(object):

    def __init__(self, chosen_tags):
        templates, tags = self.determine_templates(chosen_tags)

        self._templates = templates
        self._tags = tags

    @property
    def templates(self):
        return self._templates

    @property
    def tags(self):
        return self._tags

    def determine_templates(self, list_of_tags):
        templates = Object.objects.all().values_list('tags__value', 'unique_identifier')

        considered_templates = []
        for template in templates:
            if len(set(list_of_tags).intersection(set(template.tags.all().values_list('value', flat=True)))) == len(
                    list_of_tags):  # or template.loading_name == 'blank':
                considered_templates.append(template)

        # Find common tags amongst ALL considered template and remove them in the end
        tags_to_skip = set()
        if len(considered_templates) > 1:
            set_stuff = [set(t.tags.all().values_list('value', flat=True)) for t in considered_templates]
            start = set_stuff[0]
            for i in range(1, len(set_stuff)):
                start = start.intersection(set_stuff[i])

            keep = set()
            for s in set_stuff:
                if len(s - start) == 0:
                    keep = keep.union(s)

            tags_to_skip = start - keep

        tags_to_skip = tags_to_skip.union(list_of_tags)

        all_tags = [item for sublist in considered_templates for item in sublist.tags.all().values_list('value', flat=True)]
        c = Counter(all_tags)
        tags = {}

        for key, value in c.items():
            if key not in tags_to_skip:
                tags[key] = value

        return considered_templates, tags

