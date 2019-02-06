# Generated by Django 2.1.5 on 2019-02-06 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('ra', models.CharField(max_length=13, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=60)),
                ('email_contato', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('sigla', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitacaoAlteracao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acao', models.CharField(choices=[('R', 'Retirar Diciplina'), ('I', 'Incluir Disciplina')], max_length=1)),
                ('dp', models.BooleanField(default=False)),
                ('disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acomodacao.Disciplina')),
            ],
        ),
        migrations.CreateModel(
            name='Submissao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(auto_now_add=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acomodacao.Aluno')),
            ],
        ),
        migrations.AddField(
            model_name='solicitacaoalteracao',
            name='submissao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='acomodacao.Submissao'),
        ),
        migrations.AddField(
            model_name='curso',
            name='disciplinas',
            field=models.ManyToManyField(to='acomodacao.Disciplina'),
        ),
    ]
