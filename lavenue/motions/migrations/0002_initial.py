# Generated by Django 3.2.3 on 2021-06-29 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('motions', '0001_initial'),
        ('speakers', '0001_initial'),
        ('organisations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='requester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='speakers.participant', verbose_name='requester'),
        ),
        migrations.AddField(
            model_name='motion',
            name='point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisations.point', verbose_name='point'),
        ),
        migrations.AddField(
            model_name='motion',
            name='proposer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='proposed_set', to='speakers.participant', verbose_name='proposer'),
        ),
        migrations.AddField(
            model_name='motion',
            name='seconder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='seconded_set', to='speakers.participant', verbose_name='seconder'),
        ),
        migrations.AddField(
            model_name='motion',
            name='supplants',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motions.motion', verbose_name='supplants'),
        ),
        migrations.AddField(
            model_name='ballot',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='speakers.participant', verbose_name='proposer'),
        ),
        migrations.AddField(
            model_name='ballot',
            name='vote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='motions.vote', verbose_name='vote'),
        ),
        migrations.AlterUniqueTogether(
            name='ballot',
            unique_together={('participant', 'vote')},
        ),
    ]
