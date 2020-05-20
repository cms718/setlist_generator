from django.contrib import admin
# Register your models here.

from .models import Band, BandMember, Song


class BandMemberInline(admin.StackedInline):
    model = BandMember
    extra = 0

class SongInline(admin.TabularInline):
    model = Song
    extra = 0

class BandAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Information',               {'fields': ['band_name']})
    ]
    inlines = [BandMemberInline, SongInline]


admin.site.register(Band, BandAdmin)
