from rest_framework import serializers

from .models import Profile, EnglishPremierLeague, ChampionLeague, AfconLeague, Baseball, Bundesliga, EuropaLeague, Formula1, Laliga, NBA, NFL, Worldcup




class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    Afcon = serializers.ImageField(source='Afcon.icon')
    Baseball = serializers.ImageField(source='Baseball.icon')
    Bundesliga = serializers.ImageField(source='Bundesliga.icon')
    Europa = serializers.ImageField(source='Europa.icon')
    Formula1 = serializers.ImageField(source='Formula1.icon')
    Laliga = serializers.ImageField(source='Laliga.icon')
    NBA = serializers.ImageField(source='NBA.icon')
    NFL = serializers.ImageField(source='NFL.icon')
    Worldcup = serializers.ImageField(source='Worldcup.icon')
    EnglishPremierLeague = serializers.ImageField(source='EnglishPremierLeague.icon')
    Team = serializers.ImageField(source='Team.icon')
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "id",
            "image",
            "EnglishPremierLeague",
            "Team",
            "Afcon",
            "Baseball",
            "Bundesliga",
            "Europa",
            "Formula1",
            "Laliga",
            "NBA",
            "NFL",
            "Worldcup",
            "clubimage",
            "bio",
            "location",
            "follower_count",
            "following_count",
            "is_following",
            "username",
        ]
    
    def get_is_following(self, obj):
        # request???
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
   
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_following_count(self, obj):
        return obj.user.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()