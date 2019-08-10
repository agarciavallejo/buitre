from ...entities.tag import Tag
from ...utils.exceptions import ArgumentException


class UpdateUserTagsService:

    def __init__(self, tag_repository):
        self.tag_repository = tag_repository

    def call(self, args):
        if 'user_id' not in args or args['user_id'] is None:
            raise ArgumentException("'user_id' parameter is required")
        if 'tags' not in args or args['tags'] is None:
            raise ArgumentException("'tags' parameter is required")
        if not args['tags']:
            raise ArgumentException("tag list in 'tags' argument should not be empty")

        user_id = args['user_id']
        tag_names = args['tags']
        self.tag_repository.remove_from_user(user_id)

        for tag_name in tag_names:
            tag = self.tag_repository.get_by_name(tag_name)
            if tag is None:
                tag = self.tag_repository.persist(Tag(tag_name))

            self.tag_repository.add_to_user(tag, user_id)

        return self.tag_repository.get_by_user_id(user_id)
