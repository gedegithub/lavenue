# Generated by Django 3.2.3 on 2021-07-17 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisations', '0002_memberrequests'),
        ('motions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motion',
            name='operative',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='operative clauses'),
        ),
        migrations.AlterField(
            model_name='motion',
            name='point',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organisations.point', verbose_name='point'),
        ),
        migrations.AlterField(
            model_name='motion',
            name='proposition',
            field=models.CharField(blank=True, choices=[('l.c', 'Close the session'), ('l.t', 'Fix a time to resume the session'), ('l.a', 'Adjourn'), ('l.s', 'Recess'), ('l.P', 'Point of privilege'), ('l.A', "Appeal the chair's decision"), ('l.e', 'Amend the approved agenda'), ('l.W', 'Withdraw motion'), ('l.c', 'Enter in camera'), ('l.T', 'Impose a time limit'), ('l.r', 'Read document'), ('l.w', 'Write motion'), ('l.d', 'Divide motion'), ('l.S', 'Suspend the rules'), ('l.v', 'Conduct a secret vote'), ('l.b', 'Table discussion'), ('l.V', 'Immediately vote'), ('l.P', 'Postpone discussion definitely'), ('l.C', 'Refer to a committee'), ('l.p', 'Postpone discussion indefinitely'), ('l.m', 'Sub-amendment'), ('l.M', 'Amendment'), ('l.R', 'Main motion'), ('l.E', 'Reconsideration of a question'), ('l.n', 'Nominate a member for a committee')], default=None, max_length=3, null=True, verbose_name='proposition'),
        ),
        migrations.AlterField(
            model_name='motion',
            name='supplants',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='motions.motion', verbose_name='supplants'),
        ),
    ]
