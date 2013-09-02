from feedly.activity import Activity
from feedly.storage.cassandraCQL import models
from feedly.verbs import get_verb_by_id
import pickle
from feedly.serializers.base import BaseSerializer


class CassandraActivitySerializer(BaseSerializer):

    def dumps(self, activity):
        return models.Activity(
            activity_id=long(activity.serialization_id),
            actor=activity.actor_id,
            time=activity.time,
            verb=activity.verb.id,
            object=activity.object_id,
            target=activity.target_id,
            entity_id=activity.extra_context.get('entity_id'),
            extra_context=pickle.dumps(activity.extra_context)
        )

    def loads(self, serialized_activity):
        # TODO: convert cqlengine model to feedly Activity using public API
        activity_kwargs = {k:getattr(serialized_activity, k) for k in serialized_activity.__dict__['_values'].keys()}
        activity_kwargs.pop('activity_id')
        activity_kwargs.pop('entity_id')
        activity_kwargs.pop('user_id')
        activity_kwargs['verb'] = get_verb_by_id(int(serialized_activity.verb))
        activity_kwargs['extra_context'] = pickle.loads(
            activity_kwargs['extra_context']
        )
        return Activity(**activity_kwargs)
