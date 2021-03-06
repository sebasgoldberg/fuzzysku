#encoding=utf8
from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from default.models import Material, Secao
from django.db.utils import IntegrityError
from django.contrib.auth.models import User, Group

USERNAME = 0
EMAIL = 1
FIRST_NAME = 2
LAST_NAME = 3

class Command(BaseCommand):
    help = 'Carrega usuarios desde arquivo separado por tabuladores.'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+')

    def handle(self, *args, **options):

        grupo, creado = Group.objects.get_or_create(
            name=u'Asignador Familias'
        )

        if creado:
            grupo.permissions = list(
                Permission.objects.filter(
                    codename__in=['change_familia', 'change_material']
                )
            )
            grupo.save()

        with open('loaduser.err', 'a+') as ferr:
            for filepath in options['filepath']:
                with open(filepath, 'r') as f:
                    header = True
                    for line in f:
                        if header:
                            header = False
                            continue
                        line = line.strip()
                        register = line.split('\t')
                        for i in range(len(register)):
                            register[i] = register[i].strip()

                        try:

                            username = register[USERNAME].lower()
                            
                            try:
                                user = User.objects.get(username=username)
                                self.stdout.write(self.style.WARNING(u'Usuario "%s" ja existe.' % user))
                            except User.DoesNotExist:

                                user = User.objects.create_user(
                                    username=username,
                                    email=register[EMAIL],
                                    first_name=register[FIRST_NAME],
                                    last_name=register[LAST_NAME],
                                    is_staff=True,
                                    password=u'familia123'
                                    )

                                user.groups=[grupo]
                                user.save()
                                self.stdout.write(self.style.SUCCESS(u'Usuario "%s" criado com sucesso.' % user))

                        except IntegrityError:

                            self.stdout.write(self.style.ERROR(u'Usuario "%s" não criado: %s' % (username, register)))
                            print(line,file=ferr)

