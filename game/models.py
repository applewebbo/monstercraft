from django.db import models

class Question(models.Model):
    CATEGORY_CHOICES = [
        ('MATH', 'Matematica'),
        ('GEO', 'Geografia'),
        ('ENG', 'Inglese'),
        ('CHEM', 'Chimica'),
        ('SCI', 'Scienze'),
        ('ITA', 'Italiano'),
        ('HIST', 'Storia'),
    ]
    
    DIFFICULTY_CHOICES = [
        (1, 'Facile'),
        (2, 'Medio'),
        (3, 'Difficile'),
    ]
    
    text = models.CharField(max_length=255, verbose_name="Testo della domanda")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='MATH')
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=1, verbose_name="Difficoltà")
    
    option_1 = models.CharField(max_length=100, verbose_name="Opzione 1")
    option_2 = models.CharField(max_length=100, verbose_name="Opzione 2")
    option_3 = models.CharField(max_length=100, verbose_name="Opzione 3")
    option_4 = models.CharField(max_length=100, verbose_name="Opzione 4", blank=True, null=True)
    
    correct_option = models.IntegerField(help_text="Inserisci il numero dell'opzione corretta (1, 2, 3 o 4)")

    class Meta:
        verbose_name = "Domanda"
        verbose_name_plural = "Domande"

    def __str__(self):
        return f"[{self.get_category_display()}] {self.text}"

class Score(models.Model):
    initials = models.CharField(max_length=3, verbose_name="Iniziali")
    score = models.IntegerField(verbose_name="Punteggio")
    level = models.IntegerField(verbose_name="Livello Raggiunto")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-level']
        verbose_name = "Punteggio"
        verbose_name_plural = "Punteggi"

    def __str__(self):
        return f"{self.initials} - {self.score} (Lvl {self.level})"
