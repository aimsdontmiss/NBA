from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _



# Create your models here.
# models.py:

def team_logo_path(instance, filename):
    filename = filename.replace(' ', '_')
    return f'teams/{instance.name}/{filename}'


class Team(models.Model):
    CONFERENCE = (
        ('East', 'east'),
        ('West', 'west')
    )

    id          = models.IntegerField(primary_key=True)
    city_name   = models.CharField(max_length=100, blank=True, null=True)
    team_name   = models.CharField(max_length=100, blank=True, null=True)
    slug_name   = models.SlugField(max_length=200, unique=True, blank=True)
    abbr        = models.CharField(max_length=10)
    conf        = models.CharField(max_length=50, null=True, blank=True, choices=CONFERENCE)
    arena       = models.CharField(max_length=120, blank=True, null=True)
    logo        = models.ImageField(_("Image"), upload_to=team_logo_path, null=True, blank=True)

    @property
    def name(self):
        return f"{self.city_name} {self.team_name}"

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.abbr



class Player(models.Model):
    id          = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=100)
    slug_name   = models.CharField(max_length=200, unique=True, blank=True)
    team        = models.ForeignKey(Team, on_delete=models.CASCADE)
    country     = models.CharField(max_length=120, blank=True, null=True)
    school      = models.CharField(max_length=120, blank=True, null=True)
    birthdate   = models.CharField(max_length=120, blank=True, null=True)
    height      = models.CharField(blank=True, null=True)
    weight      = models.IntegerField(blank=True, null=True)
    position    = models.CharField(max_length=50, null=True, blank=True)
    jersey      = models.IntegerField(null=True, blank=True)
    active      = models.BooleanField(blank=False, null=True)

    def __str__(self):
        return self.slug_name
    
    


class PlayerStat(models.Model):
    STAT_TYPES = [
        ("reg", "Regular Season"),
        ("post", "Postseason"),
        ("career", "Career"),
    ]

    # fk. associations
    season    = models.CharField(max_length=20)
    stat_type = models.CharField(max_length=10, choices=STAT_TYPES)
    player    = models.OneToOneField(Player, on_delete=models.CASCADE, primary_key=True)
    team      = models.ForeignKey(Team, on_delete=models.CASCADE)

    # volume
    gmp  = models.IntegerField()
    mins = models.IntegerField()
    pts  = models.IntegerField()

    # shooting
    fgm = models.IntegerField()
    fga = models.IntegerField()

    tpm = models.IntegerField()
    tpa = models.IntegerField()

    ftm = models.IntegerField()
    fta = models.IntegerField()

    # rebounding
    oreb = models.IntegerField()
    dreb = models.IntegerField()
    reb  = models.IntegerField()

    # playmaking / defense
    ast = models.IntegerField()
    stl = models.IntegerField()
    blk = models.IntegerField()
    tov = models.IntegerField()
    pf  = models.IntegerField()

    # adv. stats
    plus_minus     = models.FloatField(null=True, blank=True)
    fantasy_points = models.FloatField(null=True, blank=True)
    double_doubles = models.IntegerField(default=0, null=True, blank=True)
    triple_doubles = models.IntegerField(default=0, null=True, blank=True)

    # meta data
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("player", "season", "team", "stat_type")

    def __str__(self):
        return f"{self.player.slug_name}-{self.stat_type}-szn-{self.season}"

    def per_gm(self, stat):
        if self.gmp > 0:
            return round(getattr(self, stat) / self.gmp, 2)
        return 0.0
    
    @property
    def mpg(self):
        return self.per_gm('mins')
    
    @property
    def ppg(self):
        return self.per_gm('pts')
    
    @property
    def apg(self):
        return self.per_gm('ast')
    
    @property
    def rpg(self):
        return self.per_gm('reb')
    
    @property
    def stl_pg(self):
        return self.per_gm('stl')
    
    @property
    def blk_pg(self):
        return self.per_gm('blk')
    
    @property
    def tov_pg(self):
        return self.per_gm('tov')
    


class TeamStat(models.Model):
    STAT_TYPES = [
        ("reg", "Regular Season"),
        ("post", "Postseason"),
    ]

    team      = models.ForeignKey(Team, on_delete=models.CASCADE)
    season    = models.CharField(max_length=20)
    stat_type = models.CharField(max_length=10, choices=STAT_TYPES)
    coach     = models.CharField(max_length=120)

    # record
    wins      = models.IntegerField()
    losses    = models.IntegerField()
    rank      = models.IntegerField()

    # volume
    gmp       = models.IntegerField()
    mins      = models.FloatField()
    pts       = models.FloatField()

    # shooting

    fga = models.IntegerField()
    tpm = models.IntegerField()
    tpa = models.IntegerField()
    ftm = models.IntegerField()
    fta = models.IntegerField()

    # rebounding
    oreb = models.FloatField()
    dreb = models.FloatField()
    reb  = models.FloatField()

    # playmaking / defense
    ast = models.FloatField()
    stl = models.FloatField()
    blk = models.FloatField()
    tov = models.FloatField()
    pf  = models.FloatField()

    # adv. stats
    plus_minus = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ("season", "team", "stat_type")

    def record_slug(self):
        return f"{self.wins}-{self.losses}"
    
    def __str__(self):
        return f"{self.team.slug_name}-{self.stat_type}-szn-{self.season}"
    
    def per_gm(self, stat):
        if self.gmp > 0:
            return round(getattr(self, stat) / self.gmp, 2)
        return 0.0

    @property
    def ppg(self):
        return self.per_gm('pts')


