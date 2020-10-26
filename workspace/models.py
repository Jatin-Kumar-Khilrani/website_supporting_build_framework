from django.db import models

class tool_list(models.Model):
    toolname = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100)

    class Meta:
        app_label = 'workspace'
#         db_table = "workspace_release_list"

    def __unicode__(self):
        return self.release

class release_list(models.Model):
    release = models.CharField(max_length=100)
    svn_url = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100)

    class Meta:
        app_label = 'workspace'
#         db_table = "workspace_release_list"

    def __unicode__(self):
        return self.release
    
class user_workspace(models.Model):
    ws_name = models.CharField(max_length=100)
    release = models.ForeignKey(release_list, on_delete=models.CASCADE)
    svn_url = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100)
    add_date = models.DateField()
    ws_path = models.CharField(max_length=100,null=True)
    
    class Meta:
        app_label = 'workspace'

    def __unicode__(self):
        return self.ws_name
   