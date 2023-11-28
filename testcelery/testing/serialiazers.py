from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import (Events, LiveOfEvents, EventId,
                     Tournament, HockeyLiveEvents, TournamentHockey,
                     EndedMatch, Scheduled, All, AllHockey, ScheduledHockey, EndedHockey)


class EventsSerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)
    start_time = serializers.IntegerField()
    start_utime = serializers.IntegerField()
    home_score_part_2 = serializers.CharField(allow_blank=True, required=False)
    away_score_part_2 = serializers.CharField(allow_blank=True, required=False)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()  # Явное обновление updated_at
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images = representation.get('home_images', [])
        home_images_string = ''.join(home_images)
        representation['home_images'] = home_images_string

        away_images = representation.get('away_images', [])
        away_images_string = ''.join(away_images)
        representation['away_images'] = away_images_string

        return representation

    class Meta:
        model = Events
        fields = '__all__'


class LiveOfEventsSerializer(serializers.ModelSerializer):
    # использование ранее созданного сериализатора для связанной модели
    events = EventsSerializer()

    class Meta:
        model = LiveOfEvents
        fields = '__all__'


class EventLiveIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventId
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    events = EventsSerializer(many=True)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_at = timezone.now()  # Явное обновление updated_at
        instance.save()
        return instance

    class Meta:
        model = Tournament
        fields = ['id', 'name', 'tournament_stage_type', 'tournament_imng',
                  'TOURNAMENT_TEMPLATE_ID', 'TOURNAMENT_IMAGE', 'events']


class HockeyLiveEventsSerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)
    home_score_part_3 = serializers.CharField(allow_blank=True, required=False)
    away_score_part_3 = serializers.CharField(allow_blank=True, required=False)
    home_score_part_2 = serializers.CharField(allow_blank=True, required=False)
    away_score_part_2 = serializers.CharField(allow_blank=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images = representation.get('home_images', [])
        home_images_string = ''.join(home_images)
        representation['home_images'] = home_images_string

        away_images = representation.get('away_images', [])
        away_images_string = ''.join(away_images)
        representation['away_images'] = away_images_string

        return representation

    class Meta:
        model = HockeyLiveEvents
        fields = '__all__'


class TournamentHockeySerializer(serializers.ModelSerializer):
    events = HockeyLiveEventsSerializer(many=True)

    class Meta:
        model = TournamentHockey
        fields = ['id', 'name', 'tournament_stage_type', 'tournament_imng',
                  'TOURNAMENT_TEMPLATE_ID', 'TOURNAMENT_IMAGE', 'events']


class EndedMatchSerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)
    away_score_part_2 = serializers.CharField(allow_null=True, required=False)
    home_score_part_2 = serializers.CharField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images_list = representation.get('home_images', [])
        if home_images_list is not None:
            home_images_string = ''.join(home_images_list)
            representation['home_images'] = home_images_string
        away_images_list = representation.get('away_images', [])
        if away_images_list is not None:
            away_images_string = ''.join(away_images_list)
            representation['away_images'] = away_images_string
        return representation

    class Meta:
        model = EndedMatch
        fields = '__all__'


class ScheduledSerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images_list = representation.get('home_images', [])
        if home_images_list is not None:
            home_images_string = ''.join(home_images_list)
            representation['home_images'] = home_images_string
        away_images_list = representation.get('away_images', [])
        if away_images_list is not None:
            away_images_string = ''.join(away_images_list)
            representation['away_images'] = away_images_string
        return representation

    class Meta:
        model = Scheduled
        fields = '__all__'


class AllSerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)
    away_score_part_2 = serializers.CharField(allow_null=True, required=False)
    home_score_part_2 = serializers.CharField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images_list = representation.get('home_images', [])
        if home_images_list is not None:
            home_images_string = ''.join(home_images_list)
            representation['home_images'] = home_images_string
        away_images_list = representation.get('away_images', [])
        if away_images_list is not None:
            away_images_string = ''.join(away_images_list)
            representation['away_images'] = away_images_string
        return representation

    class Meta:
        model = All
        fields = '__all__'


class AllHockeySerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)
    away_score_part_2 = serializers.CharField(allow_null=True, required=False)
    home_score_part_2 = serializers.CharField(allow_null=True, required=False)
    away_score_part_3 = serializers.CharField(allow_null=True, required=False)
    home_score_part_3 = serializers.CharField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images_list = representation.get('home_images', [])
        if home_images_list is not None:
            home_images_string = ''.join(home_images_list)
            representation['home_images'] = home_images_string
        away_images_list = representation.get('away_images', [])
        if away_images_list is not None:
            away_images_string = ''.join(away_images_list)
            representation['away_images'] = away_images_string
        return representation

    class Meta:
        model = AllHockey
        fields = '__all__'


class ScheduledHockeySerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images_list = representation.get('home_images', [])
        if home_images_list is not None:
            home_images_string = ''.join(home_images_list)
            representation['home_images'] = home_images_string
        away_images_list = representation.get('away_images', [])
        if away_images_list is not None:
            away_images_string = ''.join(away_images_list)
            representation['away_images'] = away_images_string
        return representation

    class Meta:
        model = ScheduledHockey
        fields = '__all__'


class EndedHockeySerializer(serializers.ModelSerializer):
    home_images = serializers.ListField(allow_null=True, required=False)
    away_images = serializers.ListField(allow_null=True, required=False)
    away_score_part_2 = serializers.CharField(allow_null=True, required=False)
    home_score_part_2 = serializers.CharField(allow_null=True, required=False)
    away_score_part_3 = serializers.CharField(allow_null=True, required=False)
    home_score_part_3 = serializers.CharField(allow_null=True, required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        home_images_list = representation.get('home_images', [])
        if home_images_list is not None:
            home_images_string = ''.join(home_images_list)
            representation['home_images'] = home_images_string
        away_images_list = representation.get('away_images', [])
        if away_images_list is not None:
            away_images_string = ''.join(away_images_list)
            representation['away_images'] = away_images_string
        return representation

    class Meta:
        model = EndedHockey
        fields = '__all__'
