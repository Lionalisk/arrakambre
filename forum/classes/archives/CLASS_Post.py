from django.db import models
from django.utils import timezone

class Post(models.Model):
	perso = models.ForeignKey(Perso, on_delete=models.CASCADE)
	lieu = models.ForeignKey(Lieu, on_delete=models.CASCADE)
	#titre = models.CharField(max_length=200)
	texte = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.lieu.nom+'-'+self.perso.nom+' - '